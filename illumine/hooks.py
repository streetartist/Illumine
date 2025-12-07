from typing import Callable, Dict, List, Any

class HookManager:
    def __init__(self):
        self.hooks: Dict[str, List[Callable]] = {}

    def register(self, event_name: str, callback: Callable):
        """
        Register a callback for a specific event.
        """
        if event_name not in self.hooks:
            self.hooks[event_name] = []
        self.hooks[event_name].append(callback)
        print(f"Hook registered: {event_name} -> {callback.__name__}")

    def dispatch(self, event_name: str, *args, **kwargs) -> List[Any]:
        """
        Dispatch an event and return results from all registered callbacks.
        """
        results = []
        if event_name in self.hooks:
            for callback in self.hooks[event_name]:
                try:
                    result = callback(*args, **kwargs)
                    if result is not None:
                        results.append(result)
                except Exception as e:
                    print(f"Error in hook '{event_name}': {e}")
        return results

    def filter(self, event_name: str, value: Any, *args, **kwargs) -> Any:
        """
        Pass a value through a chain of filters (hooks).
        """
        if event_name in self.hooks:
            for callback in self.hooks[event_name]:
                try:
                    value = callback(value, *args, **kwargs)
                except Exception as e:
                    print(f"Error in filter '{event_name}': {e}")
        return value
