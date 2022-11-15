import typing as t
from datetime import timedelta

from flask import Flask

from .auth import AuthManager
from .database import Database
from .exception.apiExceptions import ApiExceptions


class EasyFramework():
    exceptionList: t.List[BaseException] =  ApiExceptions.exceptions
    def __init__(self, app:Flask)-> None:
        self.app = app

        self.setDefaultConfig()
        self.database_register()
        self.exceptions_register()
        self.authView_register()

    def setDefaultConfig(self):
        self.app.config.setdefault('EASY_FRAMEWORK_DB_DIALECT','sqlite')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_URI','/')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_PORT','')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_DBNAME','sqlite.db')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_USERNAME','')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_PASSWORD','')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_CREATE_ALL', False)
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_VIEW', True)
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_MODULE', AuthManager)
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_TYPE', 'database')
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_TOKEN_EXPIDATION', timedelta(days=1))

    def authView_register(self):
        if self.app.config.get('EASY_FRAMEWORK_AUTH_VIEW') is True:
            pass
            # self.app.add_url_rule('/auth')

    def exceptions_register(self):
       for exception in self.exceptionList: 
            print('Registrando Exception')
            self.app.register_error_handler(exception, exception.getExceptionFunction)

    def database_register(self):
        self.app.config['database'] = Database(self.app)