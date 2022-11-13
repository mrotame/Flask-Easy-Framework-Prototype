import typing as t
from flask import Flask
from .exception.apiExceptions import ApiExceptions

class EasyFramework():
    exceptionList: t.List[BaseException] =  ApiExceptions.exceptions
    def __init__(self, app:Flask)-> None:
        self.app = app

        self.exceptions_register()

    def exceptions_register(self):
       for exception in self.exceptionList: 
            print('Registrando Exception')
            self.app.register_error_handler(exception, exception.getExceptionFunction)