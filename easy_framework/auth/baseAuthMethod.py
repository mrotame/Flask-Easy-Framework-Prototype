from abc import ABC, abstractmethod

from flask import current_app, request

from ..user.userManager import UserManager
from ..user.userModel import UserModel

class BaseAuthMethod(ABC):
    def __init__(self):
        pass

    def getUserManager(self)-> UserManager:
        return current_app.userManager

    @abstractmethod
    def generateSession(self)->str:
        return self.generateHashToken()

    @abstractmethod
    def generateHashToken(self)->str:
        pass

    @abstractmethod
    def returnUserFromToken(self)->UserModel:
        pass

    def getUser(self):
        userManager = self.getUserManager()
        return userManager.getUser(request.get_json())
