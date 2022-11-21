from typing import TYPE_CHECKING
from easy_framework.serializer import BaseSerializer, fields
from flask import current_app
from marshmallow import post_load
if TYPE_CHECKING:
    from easy_framework.auth import PasswordManager


class AuthSerializer(BaseSerializer):
    @property
    def getPasswordManager(self):
        return current_app.config.get('EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER')

    class Meta():
        login = fields.Str()
        password = fields.Str(load_only=True)

    class PostMeta(Meta):
        login = fields.Str(required=True)
        fields.Str(required=True, load_only=True)
