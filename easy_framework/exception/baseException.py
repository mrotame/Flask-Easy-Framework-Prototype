import typing as t
from abc import abstractmethod


class BaseException(Exception):
    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    @property
    @abstractmethod
    def message(self) -> str | t.Dict[str, any]:
        pass

    @classmethod
    def getExceptionFunction(self, e: BaseException):
        return self.dispatch_exception(e)

    def dispatch_exception(self) -> t.Tuple[str | t.Dict[str, any], int]:
        return self.message, self.status_code
