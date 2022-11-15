__author__ = 'Matheus Menezes Almeida'
__date__ = '26/08/2022'
__email__ = 'matheus.almeida@compila.com.br'

'''
Classe responsável pelo decorator que exige login antes de continuar com a request
'''
from typing import Callable
from flask import request
from sqlalchemy.orm import Session

class Login_required():
    func: Callable

    def __init__(self, func:Callable)-> None:
        self.func = func

    def __call__(self, *args, **kwargs)-> Callable:
        if (
            self.checkTokenInRequest() and self.validateToken()
        ):  
            return self.func(*args, **kwargs)
        else:
            return self.retorna_nao_autorizado()

    def checkTokenInRequest(self):
        return 'Authorization' in request.headers and 'Bearer ' in request.headers.get('Authorization','')

    def validateToken(self):
        return True

    def returnNonAuthorizedError(self, *args, **kwargs):
        return {'msg':'Invalid session token',}, 401