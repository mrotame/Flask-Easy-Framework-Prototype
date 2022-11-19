import secrets

from flask import current_app, request

from .baseAuthMethod import BaseAuthMethod
from .authModel import AuthModel
from ..exception.apiExceptions import InvalidCredentials

class DatabaseMethod(BaseAuthMethod):
    def generateSession(self):
        token = self.generateHashToken()
        user = self.getUser()
        if user is None:
            raise InvalidCredentials('User not found or password is invalid')
        session = AuthModel(token=token, user_id=user.id)
        session.save()
        return token

    def generateHashToken(self):
        return secrets.token_hex(128)

    def getUserFromToken(self):
        if 'Authorization' in request.headers and 'Bearer' in request.headers.get('Authorization', ''):
            token = self.token
            userModel = self.userModel
            user = userModel.get.one(AuthModel.token==token, userModel.id == AuthModel.user_id)
            return user
            
