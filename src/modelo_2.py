from typing import Callable, Any


def with_callback(x: float, y: float, callback: Callable[..., Any]) -> float:
    result = x + y
    callback(f"{result = }")
    return x + 1


with_callback(1, 2, print)
