from typing import Callable, Any, TypeVar
from functools import wraps
from inspect import signature

T = TypeVar('T', bound=Callable)

class StrictTypeError(TypeError):
    """Исключение для ошибок проверки типов декоратора strict."""
    pass

class Strict:
    """
    Класс-декоратор для строгой проверки типов аргументов функции.
    """
    def __init__(self, func: T) -> None:
        self.func = func
        self.sig = signature(func)
        self.annotations = func.__annotations__
        wraps(func)(self)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        bound = self.sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, value in bound.arguments.items():
            if name in self.annotations:
                expected_type = self.annotations[name]
                if not isinstance(value, expected_type):
                    raise StrictTypeError(f"Argument '{name}' must be {expected_type.__name__}, got {type(value).__name__}")
        return self.func(*args, **kwargs)

strict = Strict

# Пример использования
@strict
def sum_two(a: int, b: int) -> int:
    return a + b 