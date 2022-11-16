from easy_framework.model.baseModel import BaseModel
from sqlalchemy import Column, String

class UserModel(BaseModel):
    __tablename__ = 'FLASK_EASY_FRAMEWORK_USER'
    login = Column(String(60))
    password = Column(String(255))

