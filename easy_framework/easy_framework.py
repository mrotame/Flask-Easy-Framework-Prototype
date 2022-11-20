import typing as t
from datetime import timedelta

from flask import Flask

from .auth import AuthManager
from .auth.authView import AuthView
from .database import Database
from .exceptions.apiExceptions import ApiExceptions
from .user.userManager import UserManager
from .user.userModel import UserModel


class EasyFramework():
    exceptionList: t.List[BaseException] = ApiExceptions.exceptions

    def __init__(self, app: Flask) -> None:
        self.app = app

        self.setDefaultConfig()
        self.database_register()
        self.exceptions_register()
        self.authView_register()
        self.userManager_register()
        self.authManager_register()

    def setDefaultConfig(self):
        # -- DATABASE CONFIG --
        self.app.config.setdefault('EASY_FRAMEWORK_DB_DIALECT', 'sqlite')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_URI', '/')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_PORT', '')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_DBNAME', 'sqlite.db')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_USERNAME', '')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_PASSWORD', '')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_CREATE_ALL', False)
        # -- AUTH MODULE CONFIG --
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_VIEW', AuthView)
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_MANAGER', AuthManager)
        self.app.config.setdefault(
            'EASY_FRAMEWORK_AUTH_VIEW_AUTO_REGISTER', True)
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_TYPE', 'database')
        self.app.config.setdefault(
            'EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION', timedelta(days=1))
        # -- USER CONFIG --
        self.app.config.setdefault('EASY_FRAMEWORK_USER_MODEL', UserModel)
        self.app.config.setdefault('EASY_FRAMEWORK_USER_MANAGER', UserManager)

    def authView_register(self):
        if self.app.config.get('EASY_FRAMEWORK_AUTH_VIEW_AUTO_REGISTER') is True:
            view: AuthView = self.app.config.get('EASY_FRAMEWORK_AUTH_VIEW')
            for route in view.routes:
                self.app.add_url_rule(
                    route, view_func=view.as_view(view.name+'/'+route))

    def exceptions_register(self):
        for exception in self.exceptionList:
            print('Registrando Exception')
            self.app.register_error_handler(
                exception, exception.getExceptionFunction)

    def userManager_register(self):
        self.app.userManager = self.app.config['EASY_FRAMEWORK_USER_MANAGER'](
            self.app)

    def authManager_register(self):
        self.app.authManager = self.app.config['EASY_FRAMEWORK_AUTH_MANAGER'](
            self.app)

    def database_register(self):
        self.app.config['EASY_FRAMEWORK_DATABASE'] = Database(self.app)
