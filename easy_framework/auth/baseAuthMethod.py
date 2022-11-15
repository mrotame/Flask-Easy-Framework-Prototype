from abc import ABC, abstractmethod

class BaseAuthMethod(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generateToken(self):
        return self.generateHashToken()

    @abstractmethod
    def generateHashToken(self):
        pass

    @abstractmethod
    def validateToken(self):
        pass