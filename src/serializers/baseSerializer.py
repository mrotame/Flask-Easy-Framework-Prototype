from abc import abstractmethod
from src.models.baseModel import BaseModel
from marshmallow import Schema

class BaseSerializer(Schema):
    @property
    @abstractmethod
    def model(self)->BaseModel:
        pass

    def getModel(self)->BaseModel:
        return self.model