from datetime import datetime

import sqlalchemy as sa
from marshmallow import fields

from easy_framework.model import BaseModel
from easy_framework.serializer import BaseSerializer


class ModelTest(BaseModel):
    __tablename__ = 'TestModel'
    username = sa.Column(sa.String)
    password = sa.Column(sa.String)
    test_datetime = sa.Column(sa.DateTime, default=datetime.now())
    info = sa.Column(sa.String)

class SerializerTest(BaseSerializer):
    model = ModelTest
    class Meta():
        test_datetime = fields.DateTime()
        info = fields.Str()

    exclude_from_methods = {
        'POST':'id',
        'GET': 'password',
        'PATCH':'id'
    }