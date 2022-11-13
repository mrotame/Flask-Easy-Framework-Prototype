from marshmallow import Schema, fields, ValidationError
from src.models.user import User
from easy_framework.serializer.baseSerializer import BaseSerializer

class UserSerializer(BaseSerializer):
    class Meta():
        model = User
    model = User
    login = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)


        