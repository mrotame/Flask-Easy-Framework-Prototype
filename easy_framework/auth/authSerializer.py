from easy_framework.serializer import BaseSerializer, fields


class AuthSerializer(BaseSerializer):
    class Meta():
        login = fields.Str()
        password = fields.Str(load_only=True)

    class PostMeta(Meta):
        login = fields.Str(required=True)
        password = fields.Str(required=True, load_only=True)