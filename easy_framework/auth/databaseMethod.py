import secrets
from flask import request
from .baseAuthMethod import BaseAuthMethod
from .sessionModel import SessionModel

class DatabaseMethod(BaseAuthMethod):
    def generateToken(self):
        token = self.generateHashToken()
        session = SessionModel(token=token)
        session.save()
        return token

    def generateHashToken(self):
        return secrets.token_hex(128)

    def validateToken(self):
        if 'Authorization' in request.headers and 'Bearer' in request.headers.get('Authorization',''):
            session = SessionModel.get.one(request.headers.get('Authorization','').split()[1])
            if session is not None:
                return True
        return False