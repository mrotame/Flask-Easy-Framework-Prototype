from easy_framework.serializer import BaseSerializer, fields


class AuthSerializer(BaseSerializer):
    class Meta():
        login = fields.Str(load_only=True)
        password = fields.Str(load_only=True)
