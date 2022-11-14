import typing as t
from abc import ABC, abstractmethod
from typing import Dict, List, Literal

from flask import request
from marshmallow import ValidationError

from easy_framework.model.baseModel import BaseModel
from easy_framework.serializer.baseSerializer import BaseSerializer


class GenericApiView(ABC):
    field_lookup_value: any

    @property
    @abstractmethod
    def serializer(self) -> BaseSerializer:
        pass

    @property
    @abstractmethod
    def model(self, model:BaseModel)-> BaseModel: 
        return model

    @property
    @abstractmethod
    def field_lookup(self) -> str:pass

    def get_field_lookup_value(self)->any:
        self.field_lookup_value = request.args.get(self.field_lookup)

    def __init__(self):
        self.serializer = self.serializer()
        self.get_field_lookup_value()

    def get_serializer(self)->BaseSerializer:
        return self.serializer

    def dispatch_request(self, *args: t.List, **kwargs: t.Dict):
        self.validations(*args, **kwargs)
        return getattr(self, str(request.method).lower())(*args, **kwargs)

    def validations(self, *args, **kwargs):
        pass

    def getSingleEntity(self)->Dict[str,any]:
        model: BaseModel = self.model()
        model = model.get_one(getattr(self.model, self.field_lookup) == self.field_lookup_value)
        return self.get_serializer().dump(model)

    def getAllEntities(self)->List[Dict[str,any]]:
        model: BaseModel = self.model()
        res = model.get_many()
        return self.get_serializer().dump(res, many=True)

    def createEntity(self)->Dict[str,any]:
        json_data = request.get_json()
        try:
            serialized_data = self.get_serializer().load(json_data)
        except ValidationError as e:
            return e.messages, 422
        model: BaseModel = self.model(**serialized_data)
        model.save()
        return self.get_serializer().dump(model)

    def updateEntity(self, **kwargs)->Dict[str,any]:
        json_data = request.get_json()
        try:
            serialized_data = self.get_serializer().load(json_data)
        except ValidationError as e:
            return e.messages, 422

        model: BaseModel = self.model().get_one(getattr(self.model, self.field_lookup) == self.field_lookup_value)
        model.__dict__.update(serialized_data)
        model.update()
        return self.get_serializer().dump(model)

    def deleteEntity(self, deleteMethod: Literal['soft','hard'], *args, **kwargs)->Dict[str,any]:
        model: BaseModel = self.model().get_one(getattr(self.model, self.field_lookup) == self.field_lookup_value)
        if deleteMethod == 'hard':
            return model.delete(deleteMethod) 
        model.deleted = 1
        model.update()
        return '', 204
        