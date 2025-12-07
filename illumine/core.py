from typing import Optional, Callable, List
from .engine import BaseEngine, FlaskEngine, FastAPIEngine
from .plugins import PluginManager
from .theme_manager import ThemeManager
from .hooks import HookManager
from .admin import init_admin
import os
import importlib

class Illumine:
    def __init__(self, engine_type: str = "flask", plugin_dir: str = "plugin", static_folder: Optional[str] = None):
        """
        Initialize the Illumine application.
        
        :param engine_type: 'flask' or 'fastapi'
        :param plugin_dir: Directory where plugins are stored
        :param static_folder: Directory for global static files (optional).
                              If None, we try to use the active theme's static folder.
        """
        self.theme_manager = ThemeManager()
        self.hooks = HookManager()
        self.config = {}
        self.plugin_manager = PluginManager(plugin_dir=plugin_dir)

        # Determine static folder
        # If user didn't provide one, check if active theme has one
        if static_folder is None:
            # Note: active_theme is 'default' by default in ThemeManager
            theme_static = os.path.join(self.theme_manager.theme_dir, self.theme_manager.active_theme, "static")
            if os.path.exists(theme_static):
                static_folder = theme_static
            else:
                # Fallback to current directory 'static' if it exists, or None
                if os.path.exists("static"):
                    static_folder = "static"

        self.static_folder = static_folder
        self.engine: BaseEngine = self._create_engine(engine_type, static_folder)
        
        # Initialize Core Components
        self._init_core_components()
        
        # Register active theme's static folder explicitly if it wasn't the main static folder
        # We generally want /static/theme to point to the active theme's static
        self._register_theme_static()

    def _create_engine(self, engine_type: str, static_folder: Optional[str]) -> BaseEngine:
        # Engines should handle None static_folder gracefully (usually by not serving root static)
        # We need to make sure FlaskEngine/FastAPIEngine supports None or we pass a dummy if strict.
        # But let's assume we updated them or they can handle it.
        # Flask defaults static_folder to 'static' if None is passed to constructor? No, usually relative to root.
        
        if engine_type.lower() == "flask":
            # If static_folder is None, Flask might default. Let's pass it only if not None?
            # Or better, let's update FlaskEngine to handle it.
            return FlaskEngine(static_folder=static_folder if static_folder else "static") 
        elif engine_type.lower() == "fastapi":
            return FastAPIEngine(static_folder=static_folder if static_folder else "static")
        else:
            raise ValueError(f"Unsupported engine type: {engine_type}")
            
    def _register_theme_static(self):
        theme_static = os.path.join(self.theme_manager.theme_dir, self.theme_manager.active_theme, "static")
        if os.path.exists(theme_static):
            # Map /static/theme to the active theme's static folder
            self.engine.register_static("/static/theme", theme_static)
            print(f"Registered static route: /static/theme -> {theme_static}")

    def _init_core_components(self):
        # Initialize Admin
        init_admin(self)

    def route(self, path: str, methods: List[str] = ["GET"]):
        """
        Decorator to register a route.
        """
        def decorator(handler: Callable):
            self.engine.add_route(path, handler, methods)
            return handler
        return decorator

    def load_plugins(self):
        """
        Discover and initialize plugins.
        """
        self.plugin_manager.discover_plugins()
        self.plugin_manager.initialize_plugins(self)
        
        # After initialization, register static/templates for plugins
        for name, module in self.plugin_manager.plugins.items():
            plugin_path = os.path.dirname(module.__file__)
            
            # Register templates
            templates_path = os.path.join(plugin_path, "templates")
            if os.path.exists(templates_path):
                self.theme_manager.add_template_path(templates_path)
                print(f"Registered templates for plugin '{name}'")
                
            # Register static
            static_path = os.path.join(plugin_path, "static")
            if os.path.exists(static_path):
                url_prefix = f"/static/plugin/{name}"
                self.engine.register_static(url_prefix, static_path)

    def load_battery(self, battery_name: str):
        """
        Load a battery module.
        """
        try:
            # Assumes battery is in the 'battery' package (which we need to make importable or added to path)
            # Since 'battery' is a top-level folder, let's ensure it's in path or importable.
            # Ideally, 'battery' should be a python package.
            module = importlib.import_module(f"battery.{battery_name}")
            if hasattr(module, "init_battery"):
                module.init_battery(self)
                print(f"Battery '{battery_name}' loaded.")
                
                battery_path = os.path.dirname(module.__file__)
                
                # Register battery templates if they exist
                battery_templates = os.path.join(battery_path, "templates")
                if os.path.exists(battery_templates):
                    self.theme_manager.add_template_path(battery_templates)
                    
                # Register battery static if exists
                battery_static = os.path.join(battery_path, "static")
                if os.path.exists(battery_static):
                    url_prefix = f"/static/battery/{battery_name}"
                    self.engine.register_static(url_prefix, battery_static)
            else:
                print(f"Battery '{battery_name}' skipped: No 'init_battery' function.")
        except Exception as e:
            print(f"Failed to load battery '{battery_name}': {e}")
            
    def load_website_resources(self, website_package: str = "website"):
        """
        Load static and templates for the main website package.
        """
        try:
            module = importlib.import_module(website_package)
            website_path = os.path.dirname(module.__file__)
            
            # Register templates
            templates_path = os.path.join(website_path, "templates")
            if os.path.exists(templates_path):
                self.theme_manager.add_template_path(templates_path)
                print(f"Registered templates for {website_package}")
                
            # Register static
            static_path = os.path.join(website_path, "static")
            if os.path.exists(static_path):
                url_prefix = f"/static/{website_package}"
                self.engine.register_static(url_prefix, static_path)
                
        except ImportError:
            print(f"Website package '{website_package}' not found.")

    def run(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
        """
        Start the application.
        """
        print(f"Starting Illumine with {type(self.engine).__name__}...")
        self.load_plugins()
        self.engine.run(host=host, port=port, debug=debug)
