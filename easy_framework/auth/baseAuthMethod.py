from abc import ABC, abstractmethod

from flask import current_app, request

from ..user.userManager import UserManager
from ..user.userModel import UserModel

class BaseAuthMethod(ABC):
    @property
    def token(self):
        return request.headers.get('Authorization', 'non token').split()[1]

    @property
    def userModel(self)->UserModel:
        return current_app.config.get('EASY_FRAMEWORK_USER_MODEL')

    @abstractmethod
    def generateSession(self)->str:
        return self.generateHashToken()

    @abstractmethod
    def generateHashToken(self)->str:
        pass

    @abstractmethod
    def getUserFromToken(self)->UserModel:
        pass

    def __init__(self):
        pass

    def getUserManager(self)-> UserManager:
        return current_app.userManager

    def loadUser(self)->None:
        self.getUserManager().load_user(self.getUserFromToken())
    
    def getUser(self):
        userManager = self.getUserManager()
        return userManager.getUser(request.get_json())