from typing import Callable, Dict, Any

TOOLS: Dict[str, Callable[[dict], dict]] = {}


def register_tool(name: str, func: Callable[[dict], dict]) -> None:
    TOOLS[name] = func


def get_tool(name: str) -> Callable[[dict], dict]:
    if name not in TOOLS:
        raise KeyError(f"Tool '{name}' is not registered")
    return TOOLS[name]
