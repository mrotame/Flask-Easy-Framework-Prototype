from typing import Callable
from abc import ABC, abstractmethod

class BaseValidator(ABC):
    func: Callable

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def __call__(self, function: Callable, *args, **kwargs) -> Callable:
        self.function = function
        def wrapped(cls=None, *args, **kwargs):
            # breakpoint()
            self.cls = cls
            self.validate(*self.args, **self.kwargs)

            if self.cls is not None:
                return function(self.cls, *args, **kwargs)
            return function(*args, **kwargs)
            
        return wrapped

    @abstractmethod
    def validate(self, *args, **kwargs) -> None:
        pass