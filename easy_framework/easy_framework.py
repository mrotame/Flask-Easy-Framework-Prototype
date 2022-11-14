import typing as t

from flask import Flask

from .database import Database
from .exception.apiExceptions import ApiExceptions


class EasyFramework():
    exceptionList: t.List[BaseException] =  ApiExceptions.exceptions
    def __init__(self, app:Flask)-> None:
        self.app = app

        self.setDefaultConfig()
        self.database_register()
        self.exceptions_register()

    def setDefaultConfig(self):
        self.app.config.setdefault('EASY_FRAMEWORK_DB_DIALECT','sqlite')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_URI','/')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_PORT','')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_DBNAME','sqlite.db')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_USERNAME','')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_PASSWORD','')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_CREATE_ALL', False)

    def exceptions_register(self):
       for exception in self.exceptionList: 
            print('Registrando Exception')
            self.app.register_error_handler(exception, exception.getExceptionFunction)

    def database_register(self):
        self.app.config['database'] = Database(self.app)