"""loguru utility methode."""

# decorator for calculating execution time of functions
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import TypeVar

from loguru import logger

F = TypeVar("F", bound=Callable)


def log_execution_time(func: F) -> F:
    """Decorator to log the execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        logger.info(f"Execution time of {func.__name__}: {execution_time:.4f} seconds")
        return result

    return wrapper  # type: ignore
