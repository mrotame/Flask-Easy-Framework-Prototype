import typing as t

from flask import Flask, g

from .userMixin import AnonymousUser
from .userModel import UserModel


class UserManager():
    def __init__(self, app: Flask) -> None:
        self.app = app

    @property
    def user_model(self) -> UserModel:
        return self.app.config.get('EASY_FRAMEWORK_USER_MODEL')

    @property
    def user_credentials_needed(self) -> t.List[str]:
        return ['login', 'password']

    def getUser(self, credentials_needed_values) -> UserModel:
        return self.user_model.get.one(*[getattr(self.user_model, item) == credentials_needed_values[item] for item in self.user_credentials_needed])

    def load_user(self, user) -> None:
        if user is not None:
            g.user = user
        else:
            g.user = AnonymousUser()
