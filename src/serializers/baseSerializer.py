from abc import abstractmethod
from src.models.baseModel import BaseModel
from marshmallow import Schema, fields

class BaseSerializer(Schema):

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @property
    @abstractmethod
    def model(self)->BaseModel:
        pass

    def getModel(self)->BaseModel:
        return self.model