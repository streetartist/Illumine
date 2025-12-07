from typing import Callable, List
from flask import Flask, send_from_directory
from .base import BaseEngine
import os

class FlaskEngine(BaseEngine):
    def __init__(self, name: str = __name__, static_folder: str = "static"):
        super().__init__(static_folder=static_folder)
        if not os.path.isabs(static_folder):
            static_folder = os.path.abspath(static_folder)
            
        self.app = Flask(name, static_folder=static_folder)

    def add_route(self, path: str, handler: Callable, methods: List[str] = ["GET"]):
        """
        Register a route with Flask.
        """
        self.app.add_url_rule(path, view_func=handler, methods=methods)

    def register_static(self, url_prefix: str, directory: str):
        """
        Register a static file directory with Flask.
        We can achieve this by adding a route that serves files from that directory.
        """
        if not os.path.exists(directory):
            print(f"Warning: Static directory does not exist: {directory}")
            return

        # Ensure directory is absolute
        directory = os.path.abspath(directory)
        
        # Define endpoint name to avoid collision
        endpoint = f"static_{url_prefix.replace('/', '_').strip('_')}"

        def serve_static(filename):
            return send_from_directory(directory, filename)

        # Add rule: /url_prefix/<path:filename>
        rule = f"{url_prefix}/<path:filename>"
        self.app.add_url_rule(rule, endpoint=endpoint, view_func=serve_static)
        print(f"Registered static route: {url_prefix} -> {directory}")

    def run(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
        """
        Start the Flask development server.
        """
        self.app.run(host=host, port=port, debug=debug)
