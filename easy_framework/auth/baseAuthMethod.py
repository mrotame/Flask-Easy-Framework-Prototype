from abc import ABC, abstractmethod

from flask import current_app, request

from ..user.userManager import UserManager
from ..user.userModel import UserModel
from ..exceptions import AuthMissingError


class BaseAuthMethod(ABC):
    @property
    def token(self):
        return self.getTokenFromRequest()

    @property
    def userModel(self) -> UserModel:
        return current_app.config.get('EASY_FRAMEWORK_USER_MODEL')

    @abstractmethod
    def generateSession(self) -> str:
        return self.generateHashToken()

    @abstractmethod
    def generateHashToken(self) -> str:
        pass

    # The validateToken method should raise a registered error 
    # such as ValidationError from easy_framework.exception
    # if the token is not valid, or return None if it is valid
    #
    # Overwrite the validateToken method and call super() if needed
    @abstractmethod
    def validateToken(self) -> None:
        if self.token is None:
            raise AuthMissingError()

    @abstractmethod
    def getUserFromToken(self) -> str:
        pass

    def __init__(self):
        pass

    def getUserManager(self) -> UserManager:
        return current_app.userManager

    def loadUser(self) -> None:
        self.getUserManager().load_user(self.getUserFromToken())

    def getUser(self):
        userManager = self.getUserManager()
        return userManager.getUser(request.get_json())

    def getTokenFromRequest(self) -> str:
        try:
            return request.headers.get('Authorization', '').split()[1]
        except IndexError:
            return None
