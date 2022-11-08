from typing import Dict, List
from flask import request, current_app
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from src.serializers.baseSerializer import BaseSerializer

class GenericApiView(ABC):
    def __init__(self):
        self.dbSession = current_app.config['dbsession']()
        self.serializer: BaseSerializer = self.serializer()
        self.model = self.serializer.getModel()

    @property
    @abstractmethod
    def field_lookup(self) -> str:pass

    @property
    @abstractmethod
    def serializer(self) -> BaseSerializer:pass

    def dispatch_request(self):
        return getattr(self, str(request.method).lower())(self.dbSession)

    def singleEntity(self)->Dict[str,any]:
        res =  self.dbSession.query(self.model).filter(getattr(self.model,self.field_lookup) == request.args[self.field_lookup]).first()
        return self.serializer.dump(res)

    def listEntities(self)->List[Dict[str,any]]:
        res = self.dbSession.query(self.model).all()
        return [self.serializer.dump(res, many=True)]

    def createEntity(self)->Dict[str,any]:
        pass

    def updateEntity(self)->Dict[str,any]:
        pass

    def deleteEntity(self)->Dict[str,any]:
        pass