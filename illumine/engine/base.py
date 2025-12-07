from abc import ABC, abstractmethod
from typing import Callable, Any, List, Optional

class BaseEngine(ABC):
    """
    Abstract base class for web framework engines.
    """

    def __init__(self, static_folder: str = "static"):
        self.static_folder = static_folder
        self.routes = []

    @abstractmethod
    def add_route(self, path: str, handler: Callable, methods: List[str] = ["GET"]):
        """
        Register a route with the underlying framework.
        """
        pass

    @abstractmethod
    def register_static(self, url_prefix: str, directory: str):
        """
        Register a static file directory at a specific URL prefix.
        e.g. register_static("/static/plugin/foo", "/path/to/plugin/foo/static")
        """
        pass

    @abstractmethod
    def run(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
        """
        Start the web server.
        """
        pass
