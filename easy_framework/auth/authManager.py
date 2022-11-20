from flask import Flask
from .databaseMethod import DatabaseMethod
from .baseAuthMethod import BaseAuthMethod

class AuthManager():
    def __init__(self, app: Flask):
        self.app = app
        self.string_method = self.app.config.get('EASY_FRAMEWORK_AUTH_TYPE')

    @property
    def auth_method(self)-> BaseAuthMethod:
        try:
            return getattr(self, 'auth_method_'+self.string_method)()
        except AttributeError:
            raise AttributeError('auth method not found. Try: "database" or "jwt"(not implementes yet). If you are creating one, the auth method function must my called: "auth_method_myMethod"')

    def auth_method_database(self):
        return DatabaseMethod()

    def auth_method_jwt(self):
        pass

    def loadUser(self):
        self.auth_method.loadUser()
    