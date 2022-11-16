from flask import current_app
from .userModel import UserModel

class UserManager():
    def __init__(self, credentials_needed_values):
        self.user_model: UserModel = current_app.config.get('EASY_FRAMEWORK_USER_MODEL')
        self.user_credentials_needed = ['login', 'password']
        self.credentials_needed_values = credentials_needed_values

    def getUserFromDb(self)-> UserModel:
        return self.user_model.get.one(*[getattr(self.user_model, item)== self.credentials_needed_values[item] for item in self.user_credentials_needed])