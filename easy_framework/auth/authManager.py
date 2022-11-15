from flask import current_app
from .databaseMethod import DatabaseMethod

class AuthManager():
    def __init__(self):
        self.string_method = current_app.config.get('EASY_FRAMEWORK_AUTH_TYPE')

    @property
    def auth_method(self):
        try:
            return getattr(self, 'auth_method_'+self.string_method)
        except AttributeError:
            raise AttributeError('auth method not found. Try: "database" or "jwt". If you are creating one, the auth method function must my called: "auth_method_myMethod"')

    def auth_method_database(self):
        return DatabaseMethod()

    def auth_method_jwt(self):
        pass
    