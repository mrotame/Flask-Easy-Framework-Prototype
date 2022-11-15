from abc import ABC, abstractmethod

from flask import request
from marshmallow import Schema, fields

from easy_framework.model.baseModel import BaseModel

class BaseSerializer(ABC):

    exclude_from_methods = {}

    @abstractmethod
    def Meta():
        class Meta:
            pass
        return Meta

    class MainMeta(Schema, Meta()):
        id = fields.Integer(dump_only=True)
        created_at = fields.DateTime(dump_only=True)
        updated_at = fields.DateTime(dump_only=True)
        deleted = fields.Integer(dump_only=True)

    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.Meta = type(str(self.__class__).split("'")[1], (self.MainMeta, self.Meta), {})
        self.Meta = self.set_exclude_from_methods(self.Meta)

    def set_exclude_from_methods(self, meta):
        for item in self.exclude_from_methods.get(request.method.lower(),{}):
            setattr(meta, item, None)
        return meta

    def getModel(self) -> BaseModel:
        return self.model
