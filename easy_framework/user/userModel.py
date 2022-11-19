from sqlalchemy import Column, String

from easy_framework.model.baseModel import BaseModel

from .userMixin import UserMixin


class UserModel(BaseModel, UserMixin):
    __tablename__ = 'FLASK_EASY_FRAMEWORK_USER'
    login = Column(String(60))
    password = Column(String(255))
