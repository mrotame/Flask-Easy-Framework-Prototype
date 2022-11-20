__author__ = 'Matheus Menezes Almeida'
__date__ = '26/08/2022'
__email__ = 'matheus.almeida@compila.com.br'

'''
Classe responsável pelo decorator que exige login antes de continuar com a request
'''
from typing import Callable
from flask import request, current_app
from sqlalchemy.orm import Session
from easy_framework.auth import AuthManager
from easy_framework.exceptions import InvalidSession
from easy_framework.user import current_user


class Login_required():
    func: Callable

    def __init__(self) -> None:
        pass

    def __call__(self, func: Callable, *args, **kwargs) -> Callable:
        def valida_login(f=None):
            if (
                self.validateToken() and
                self.checkUser()
            ):
                
                if f is not None:
                    return func(f, *args, **kwargs)
                return func(*args, **kwargs)
            else:
                return self.returnNonAuthorizedError()
        return valida_login

    def checkTokenInRequest(self):
        return 'Authorization' in request.headers and 'Bearer ' in request.headers.get('Authorization', '')

    def validateToken(self):
        current_app.authManager.auth_method.validateToken()
        return True

    def checkUser(self):
        if current_user.is_authenticated is True:
            return True
        raise InvalidSession()

    def returnNonAuthorizedError(self, *args, **kwargs):
        return {'msg': 'Invalid session token or session token is expired' }, 401
