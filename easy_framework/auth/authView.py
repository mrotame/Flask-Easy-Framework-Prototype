from flask import current_app, request
import typing as t
from easy_framework.view import GenericApiView

from ..user.userModel import UserModel
from .authManager import AuthManager
from .authModel import AuthModel
from .authSerializer import AuthSerializer
from ..exception import InvalidCredentials

if t.TYPE_CHECKING:
    from ..auth import PasswordManager


class AuthView(GenericApiView):
    field_lookup = None
    serializer = AuthSerializer
    model = AuthModel
    methods=['POST']
    routes=['/auth']
    name='FLASK_EASY_FRAMWORK_AUTH_DEFAULT_VIEW'

    def post(self):
        serialized_data = self.validateRequest()
        userModel: UserModel = current_app.config.get('EASY_FRAMEWORK_USER_MODEL')
        
        user: UserModel = userModel.get.one(**{'login': serialized_data['login']})
        passwordManager: PasswordManager = current_app.passwordManager
        
        if user is None or passwordManager.compare(serialized_data['password'], user.password) is not True:
            raise InvalidCredentials('Invalid login or password')

        token = current_app.authManager.auth_method.generateSession(user)
        return {'auth_token': token}, 200
