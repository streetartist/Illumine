import importlib
import os
import sys
from typing import List, Any, Dict

class PluginManager:
    def __init__(self, plugin_dir: str = "plugin"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, Any] = {}

    def discover_plugins(self):
        """
        Discover plugins in the plugin directory.
        Assumes plugins are directories with an __init__.py file.
        """
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            return

        # Add plugin directory to sys.path to allow importing
        if os.path.abspath(self.plugin_dir) not in sys.path:
            sys.path.append(os.path.abspath(self.plugin_dir))

        for item in os.listdir(self.plugin_dir):
            plugin_path = os.path.join(self.plugin_dir, item)
            if os.path.isdir(plugin_path) and os.path.exists(os.path.join(plugin_path, "__init__.py")):
                self.load_plugin(item)

    def load_plugin(self, plugin_name: str):
        """
        Load a specific plugin by name.
        """
        try:
            # Import the plugin module
            # Since we added plugin_dir to sys.path, we can import directly
            # Or we can use importlib.util for more isolation, but simple import is easier for now.
            # If the plugin is in 'plugin/myplugin', and 'plugin' is in sys.path, we import 'myplugin'
            
            # Note: If 'plugin' is a package (has __init__.py), we should import 'plugin.myplugin'.
            # The top-level 'plugin' folder I created has an __init__.py, so it is a package.
            # But here we are treating it as a dynamic directory.
            
            # Let's assume the user installs plugins into the 'plugin' folder which is a namespace package or just a folder.
            # If I stick to 'plugin.myplugin' style:
            module = importlib.import_module(f"plugin.{plugin_name}")
            
            if hasattr(module, "init_plugin"):
                self.plugins[plugin_name] = module
                print(f"Plugin '{plugin_name}' loaded successfully.")
            else:
                print(f"Plugin '{plugin_name}' skipped: No 'init_plugin' function found.")
                
        except Exception as e:
            print(f"Failed to load plugin '{plugin_name}': {e}")

    def initialize_plugins(self, app_instance):
        """
        Run the init_plugin function for all loaded plugins.
        """
        for name, module in self.plugins.items():
            try:
                module.init_plugin(app_instance)
                print(f"Plugin '{name}' initialized.")
            except Exception as e:
                print(f"Error initializing plugin '{name}': {e}")
