from marshmallow import Schema, fields, ValidationError
from src.models.user import User
from .baseSerializer import BaseSerializer
# class Validators:
#     def validate_must_be_larger_than_6(self, data):
#         if len(data) != 6:
#             raise ValidationError("Password must have more than 5 chars")

class UserSerializer(BaseSerializer):
    model = User

    def __init__(self, *args, **kwargs):
        id = fields.Integer()
        created_at = fields.DateTime()
        updated_at = fields.DateTime()
        login = fields.Str()
        password = fields.Str(load_only=True, validate= self.validate_must_be_larger_than_6)

        super().__init__(*args, **kwargs)

    def validate_must_be_larger_than_6(self, data):
        if len(data) != 6:
            raise ValidationError("Password must have more than 5 chars")

    


    


        