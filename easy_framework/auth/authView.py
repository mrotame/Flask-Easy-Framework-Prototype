from flask import current_app, request

from easy_framework.view import GenericApiView

from ..user.userModel import UserModel
from .authManager import AuthManager
from .authModel import AuthModel
from .authSerializer import AuthSerializer


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
        userModel = userModel.get.one(**serialized_data)
        token = current_app.authManager.auth_method.generateSession()
        return {'auth_token': token}, 200
