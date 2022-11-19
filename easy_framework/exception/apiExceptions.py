import typing as t

from . import BaseException


class ValidationError(BaseException):
    message: str
    status_code: int
    def __init__(self, message: str | dict[str, any], status_code: int) -> None:
        self.message = message
        self.status_code = status_code


class AuthMissingError(BaseException):
    message = 'Authorization Header is Missing'
    status_code = 403

    
class InvalidCredentials(BaseException):
    message: str = None
    status_code: int = 401

    def __init__(self, message: str | dict[str, any]) -> None:
        self.message = message


class MissingAuthToken(BaseException):
    status_code = 403
    message = 'Required authorization token not found'

class ApiExceptions():
    exceptions: t.List[BaseException] = [
        ValidationError,
        AuthMissingError,
        InvalidCredentials
    ]
