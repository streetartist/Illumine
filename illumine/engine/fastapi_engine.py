from typing import Callable, List
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .base import BaseEngine
import os

class FastAPIEngine(BaseEngine):
    def __init__(self, static_folder: str = "static"):
        super().__init__(static_folder=static_folder)
        self.app = FastAPI()
        
        if not os.path.exists(static_folder):
             os.makedirs(static_folder, exist_ok=True)
             
        self.app.mount("/static", StaticFiles(directory=static_folder), name="static")

    def add_route(self, path: str, handler: Callable, methods: List[str] = ["GET"]):
        """
        Register a route with FastAPI.
        """
        self.app.add_api_route(path, handler, methods=methods)

    def register_static(self, url_prefix: str, directory: str):
        """
        Register a static file directory with FastAPI.
        """
        if not os.path.exists(directory):
            print(f"Warning: Static directory does not exist: {directory}")
            return
            
        # Ensure name is unique and valid
        name = f"static_{url_prefix.replace('/', '_').strip('_')}"
        
        self.app.mount(url_prefix, StaticFiles(directory=directory), name=name)
        print(f"Registered static route: {url_prefix} -> {directory}")

    def run(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
        """
        Start the FastAPI server using Uvicorn.
        """
        uvicorn.run(self.app, host=host, port=port, reload=debug)
