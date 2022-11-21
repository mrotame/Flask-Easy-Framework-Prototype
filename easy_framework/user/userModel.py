from typing import TYPE_CHECKING
from sqlalchemy import Column, String

from easy_framework.model.baseModel import BaseModel
from .userMixin import UserMixin
from flask import current_app

if TYPE_CHECKING:
    from easy_framework.auth import PasswordManager



class UserModel(BaseModel, UserMixin):
    __tablename__ = 'FLASK_EASY_FRAMEWORK_USER'
    login = Column(String(60))
    password = Column(String(255))

    @property
    def passwordManager(self):
        return current_app.config.get('EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER')()

    def save(self):
        self.password = self.passwordManager.hash(self.password)
        return super().save()
