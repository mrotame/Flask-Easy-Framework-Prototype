from abc import ABC, abstractmethod

from flask import current_app, request

from ..user.userManager import UserManager


class BaseAuthMethod(ABC):
    def __init__(self):
        pass

    def getUserManager(self)-> UserManager:
        return current_app.config.get('EASY_FRAMEWORK_USER_MANAGER')(request.get_json())

    @abstractmethod
    def generateToken(self):
        return self.generateHashToken()

    @abstractmethod
    def generateHashToken(self):
        pass

    @abstractmethod
    def validateToken(self):
        pass

    def getUser(self):
        userManager = self.getUserManager()
        return userManager.getUserFromDb()
