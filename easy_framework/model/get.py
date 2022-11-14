from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .baseModel import BaseModel

class Get():
    def __init__(self, cls):
        self.cls = cls

    def one(self, cls,*args, **kwargs)->'BaseModel':
        return self.cls().get_one(*args, **kwargs)

    def many(self,*args, **kwargs)->'BaseModel':
        return self.cls().get_many(*args,**kwargs)