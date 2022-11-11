from typing import Dict, List, Literal
from flask import request, current_app
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from src.serializers.baseSerializer import BaseSerializer
from src.models.baseModel import BaseModel
from marshmallow import ValidationError


class GenericApiView(ABC):
    def __init__(self):
        self.serializer: BaseSerializer = self.serializer()
        self.model: BaseModel = self.serializer.getModel()

    @property
    @abstractmethod
    def field_lookup(self) -> str:pass

    @property
    @abstractmethod
    def serializer(self) -> BaseSerializer:pass

    def dispatch_request(self, *args, **kwargs):
        self.validations(*args, **kwargs)
        return getattr(self, str(request.method).lower())(*args, **kwargs)

    def validations(self):
        pass

    def getSingleEntity(self, *args, **kwargs)->Dict[str,any]:
        model: BaseModel = self.model()
        model = model.get_one(getattr(self.model, self.field_lookup) == kwargs[self.field_lookup])
        return self.serializer.dump(model)

    def getAllEntities(self, *args, **kwargs)->List[Dict[str,any]]:
        model: BaseModel = self.model()
        res = model.get_many()
        return self.serializer.dump(res, many=True)

    def createEntity(self, *args, **kwargs)->Dict[str,any]:
        json_data = request.get_json()
        try:
            serialized_data = self.serializer.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        model: BaseModel = self.model(**serialized_data)
        model.save()
        return self.serializer.dump(model)

    def updateEntity(self, *args, **kwargs)->Dict[str,any]:
        json_data = request.get_json()
        try:
            serialized_data = self.serializer.load(json_data)
        except ValidationError as e:
            return e.messages, 422

        model: BaseModel = self.model().get_one(getattr(self.model, self.field_lookup) == kwargs[self.field_lookup])
        model.__dict__.update(serialized_data)
        model.update()
        return self.serializer.dump(model)

    def deleteEntity(self, deleteMethod: Literal['soft','hard'], *args, **kwargs)->Dict[str,any]:
        model: BaseModel = self.model().get_one(getattr(self.model, self.field_lookup) == kwargs[self.field_lookup])
        if deleteMethod == 'hard':
            return model.delete(deleteMethod) 
        model.deleted = 1
        model.update()
        return '', 204
        