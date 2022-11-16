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

    def returnUserFromToken(self):
        if 'Authorization' in request.headers and 'Bearer' in request.headers.get('Authorization', ''):
            token = request.headers.get('Authorization', 'non token').split()[1]
            userModel = current_app.config.get('EASY_FRAMEWORK_USER_MODEL')
            user = userModel.get.one(AuthModel.token==token, userModel.id == AuthModel.id)
            # session = AuthModel.get.one(
            #     request.headers.get('Authorization', '').split()[1])
            if user is not None:
                return user
        return None
