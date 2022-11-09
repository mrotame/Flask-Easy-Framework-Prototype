from typing import Dict, List
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
        return getattr(self, str(request.method).lower())(*args, **kwargs)

    def getSingleEntity(self, *args, **kwargs)->Dict[str,any]:
        
        model: BaseModel = self.model()
        res = model.get_one(self.model, getattr(self.model, self.field_lookup) == kwargs[self.field_lookup])
        return self.serializer.dump(res)

    def getAllEntities(self, *args, **kwargs)->List[Dict[str,any]]:
        model: BaseModel = self.model()
        res = model.get_many(self.model)
        return [self.serializer.dump(res, many=True)]

    def createEntity(self, *args, **kwargs)->Dict[str,any]:
        json_data = request.get_json()
        try:
            serialized_data = self.serializer.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        model: BaseModel = self.model()
        res = model.save(self.model, **serialized_data)
        return self.serializer.dump(res)

    def updateEntity(self, *args, **kwargs)->Dict[str,any]:
        json_data = request.get_json()
        breakpoint()
        self.serializer.load(json_data)
        model: BaseModel = self.model()
        res = model.update(self.model, self.field_lookup, kwargs[self.field_lookup], **json_data)
        return self.serializer.dump(res)

    def deleteEntity(self, deleteMethod='soft', *args, **kwargs)->Dict[str,any]:
        pass