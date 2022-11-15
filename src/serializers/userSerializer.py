from marshmallow import Schema, ValidationError, fields

from easy_framework.serializer.baseSerializer import BaseSerializer
from ..models.user import User


class UserSerializer(BaseSerializer):
    class Meta():
        login = fields.Str(required=True)
        password = fields.Str(load_only=True, required=True)
    


        