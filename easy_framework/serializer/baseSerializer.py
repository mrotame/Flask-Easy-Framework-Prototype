from abc import ABC, abstractmethod
import types
from flask import request
from marshmallow import Schema, fields

from easy_framework.model.baseModel import BaseModel


class BaseSerializer(Schema):
    exclude_from_methods = {}

    @abstractmethod
    def Meta():
        class Meta:
            pass
        return Meta

    class MainMeta():
        id = fields.Integer(dump_only=True)
        created_at = fields.DateTime(dump_only=True)
        updated_at = fields.DateTime(dump_only=True)
        deleted = fields.Integer(dump_only=True)

    def __new__(cls, *args, **kwargs):
        cls = cls.selectMeta(cls)
        return super().__new__(cls, *args, **kwargs)

    def set_exclude_from_methods(cls, meta):
        for item in cls.exclude_from_methods.get(request.method.lower(), {}):
            setattr(meta, item, None)
        return meta

    def selectMeta(cls):
        look_for = request.method.capitalize()+'Meta'
        try:
            requestedMeta = getattr(cls,look_for)
            return types.new_class(str(cls.__name__), (cls, cls.MainMeta, requestedMeta), {})
        except AttributeError:
            return types.new_class(str(cls.__name__), (cls, cls.MainMeta, cls.Meta), {})

    def getModel(self) -> BaseModel:
        return self.model
