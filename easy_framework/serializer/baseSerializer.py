from abc import abstractmethod

from marshmallow import Schema, fields

from easy_framework.model.baseModel import BaseModel


class BaseSerializer(Schema):

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted = fields.Integer(dump_only=True)

    @property
    @abstractmethod
    def model(self)->BaseModel:
        pass

    def getModel(self)->BaseModel:
        return self.model