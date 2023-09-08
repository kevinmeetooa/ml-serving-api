"""Logging module."""
import logging
from datetime import timedelta
from time import time
from typing import Any, Callable

from flask import current_app


def log_execution_time() -> Callable[..., Any]:
    """Decorate a function to log the execution time."""
    def _decorate(func: Callable[..., Any]) -> Callable[..., Any]:
        def _call(*args: Any, **kwargs: Any) -> Any:
            start = time()
            result = func(*args, **kwargs)
            end = time()
            current_app.logger.info('Executed %s from %s in %s',
                                    func.__name__, func.__module__,
                                    timedelta(seconds=end - start))
            return result
        return _call
    return _decorate
