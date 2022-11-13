from easy_framework.model.baseModel import BaseModel
from sqlalchemy import Column, String

class User(BaseModel):
    __tablename__ = 'User'
    login = Column(String(60))
    password = Column(String(255))

