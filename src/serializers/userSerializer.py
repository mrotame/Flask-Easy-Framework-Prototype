from marshmallow import Schema, fields, ValidationError
from src.models.user import User
from .baseSerializer import BaseSerializer

class UserSerializer(BaseSerializer):
    class Meta():
        model = User
    model = User
    login = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)
    

def validate_must_be_larger_than_6(self, data):
    if len(data) != 6:
        raise ValidationError("Password must have more than 5 chars")

    


    


        