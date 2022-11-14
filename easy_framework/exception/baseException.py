from abc import abstractmethod


class BaseException(Exception):

    @classmethod
    def getExceptionFunction(self, e: BaseException):
        return self.dispatch_exception(e)

    @abstractmethod
    def dispatch_exception(self):
        pass