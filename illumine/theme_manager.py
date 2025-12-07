import os
from typing import List
from jinja2 import Environment, FileSystemLoader, ChoiceLoader, select_autoescape

class ThemeManager:
    def __init__(self, theme_dir: str = "theme", active_theme: str = "default"):
        self.theme_dir = theme_dir
        self.active_theme = active_theme
        self.template_paths: List[str] = []
        self._update_template_paths()
        self.env = self._create_env()

    def _update_template_paths(self):
        """
        Update the list of paths to search for templates.
        Priority:
        1. Active Theme Directory's 'templates' subdirectory
        2. Registered Battery/Plugin Template Paths (Fallbacks)
        """
        # Change: look in 'templates' subdir of the theme
        main_theme_path = os.path.join(self.theme_dir, self.active_theme, "templates")
        if not os.path.exists(main_theme_path):
            os.makedirs(main_theme_path, exist_ok=True)
            
        # Main theme is always first priority
        self.paths = [main_theme_path] + self.template_paths

    def add_template_path(self, path: str):
        """
        Register a new template path (e.g. from a battery).
        """
        if path not in self.template_paths and os.path.exists(path):
            self.template_paths.append(path)
            self._update_template_paths()
            self.env = self._create_env() # Re-create env with new paths

    def _create_env(self):
        # Use ChoiceLoader or just FileSystemLoader with a list of paths
        # FileSystemLoader accepts a list of paths and searches in order.
        loader = FileSystemLoader(self.paths)
        return Environment(
            loader=loader,
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render(self, template_name: str, **context):
        template = self.env.get_template(template_name)
        return template.render(**context)

    def set_theme(self, theme_name: str):
        self.active_theme = theme_name
        self._update_template_paths()
        self.env = self._create_env()
