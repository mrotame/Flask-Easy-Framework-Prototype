from easy_framework.serializer import BaseSerializer, fields
from flask import current_app


class AuthSerializer(BaseSerializer):
    @property
    def getPasswordManager(self):
        return current_app.config.get('EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER')

    class Meta():
        login = fields.Str()
        password = fields.Str(load_only=True)

    class PostMeta(Meta):
        login = fields.Str(required=True)
        password = fields.Str(required=True, load_only=True)
