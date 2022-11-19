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

    def __new__(cls):
        cls.Meta = cls.selectMeta(cls)
        cls.Meta = cls.set_exclude_from_methods(cls, cls.Meta)
        return cls.Meta()

    # def __init__(self, *args, **kwargs):
    #     self.Meta = self.selectMeta()
    #     self.Meta = self.set_exclude_from_methods(self.Meta)

    def set_exclude_from_methods(self, meta):
        for item in self.exclude_from_methods.get(request.method.lower(), {}):
            setattr(meta, item, None)
        return meta

    def selectMeta(self):
        look_for = request.method.capitalize()+'Meta'
        try:
            requestedMeta = getattr(self,look_for)
            return type(str(self.__class__).split(
            "'")[1], (self.MainMeta, requestedMeta), {})
        except AttributeError:
            return type(str(self.__class__).split(
            "'")[1], (self.MainMeta, self.Meta), {})

    def getModel(self) -> BaseModel:
        return self.model
