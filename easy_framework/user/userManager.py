from flask import Flask
from .userModel import UserModel

class UserManager():
    def __init__(self, app: Flask):
        self.user_model: UserModel = app.config.get('EASY_FRAMEWORK_USER_MODEL')

    @property
    def user_credentials_needed(self):
        return ['login', 'password']

    def getUser(self, credentials_needed_values)-> UserModel:
        return self.user_model.get.one(*[getattr(self.user_model, item)== credentials_needed_values[item] for item in self.user_credentials_needed])