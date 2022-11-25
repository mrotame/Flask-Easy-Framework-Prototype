import secrets

from flask import current_app, request

from .baseAuthMethod import BaseAuthMethod
from .authModel import AuthModel
from ..exception import ValidationError, InvalidCredentials

class DatabaseMethod(BaseAuthMethod):
    token_len = 256
    def generateSession(self, user):
        token = self.generateHashToken()
        if user is None:
            raise InvalidCredentials('User not found or password is invalid')
        session = AuthModel(token=token, user_id=user.id)
        session.save()
        return token

    def generateHashToken(self):
        return secrets.token_hex(int(self.token_len/2))

    def getUserFromToken(self):
        if 'Authorization' in request.headers and 'Bearer' in request.headers.get('Authorization', ''):
            token = self.token
            userModel = self.userModel
            user = userModel.get.one(AuthModel.token==token, userModel.id == AuthModel.user_id)
            return user

    def validateToken(self):
        super().validateToken()
        if not isinstance(self.token, str):
            raise ValidationError('Invalid token type. Token is not a string', 498)
        if len(self.token) != self.token_len:
            raise ValidationError('Invalid token length', 498)
