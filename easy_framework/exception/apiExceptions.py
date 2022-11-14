import typing as t

from . import BaseException


class ValidationError(BaseException):
    def __init__(self, message:str|dict[str,any], status_code:int) -> None:
        self.message = message
        self.status_code = status_code
    
    def dispatch_exception(self):
        return self.message, self.status_code


class AuthMissingError(BaseException):
    message = 'Authorization Header is Missing'
    status_code = 403

    def dispatch_exception(self):
        return self.message, self.status_code
        

class ApiExceptions():
    exceptions: t.List[BaseException] = [
        ValidationError,
        AuthMissingError
    ]