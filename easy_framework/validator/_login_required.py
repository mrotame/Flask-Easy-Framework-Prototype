__author__ = 'Matheus Menezes Almeida'
__date__ = '26/08/2022'
__email__ = 'matheus.almeida@compila.com.br'

'''
Classe responsável pelo decorator que exige login antes de continuar com a request
'''
from flask import request, current_app
from easy_framework.exception import InvalidSession
from easy_framework.exception import AuthMissingError
from easy_framework.user import current_user
from ._baseValidator import BaseValidator

class Login_required(BaseValidator):
    def validate(self, *args, **kwargs):
        self.checkTokenInRequest()
        self.validateToken()
        self.checkUser()

    def checkTokenInRequest(self):
        if 'Authorization' not in request.headers or 'Bearer ' not in request.headers.get('Authorization', ''):
            raise AuthMissingError()

    def validateToken(self):
        current_app.authManager.auth_method.validateToken()

    def checkUser(self):
        if current_user.is_authenticated is True:
            return True
        raise InvalidSession()