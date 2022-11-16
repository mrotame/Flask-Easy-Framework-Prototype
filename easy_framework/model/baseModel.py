from datetime import datetime
from typing import List, Self

from flask import current_app
from sqlalchemy import Column, DateTime, Integer, SmallInteger
from sqlalchemy.orm import Session

from ..database import Database, base
from .get import Get


class GetDescriptor():
    def __get__(self, type, cls: 'BaseModel')->'Get':
        self.dbSession: Session = cls.get_databaseClass(cls)
        return Get(cls)
        

class BaseModel(base):
    __abstract__ = True
    id =  Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now()) 
    deleted = Column(SmallInteger, default=0)
    get = GetDescriptor()

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        cls.db: Database = cls.get_databaseClass(cls)
        return super().__new__(cls)

    def get_databaseClass(self)-> Database:
        return Database(current_app)
    
    def get_one(self, *args, **kwargs)-> 'BaseModel':
        with self.db.getScopedSession() as dbSession:
            if args is not None and len(args) > 0 :
                return self.get_one_base_query(dbSession, self.__class__).filter(*args, **kwargs).first()
            return self.get_one_base_query(dbSession, self.__class__).filter_by(**kwargs).first()

    def get_many(self, *args, **kwargs)-> List['BaseModel']:
        with self.db.getScopedSession() as dbSession:
            return self.get_many_base_query(dbSession, self.__class__).filter(*args, **kwargs).all()

    def save(self):
        with self.db.getScopedSession() as dbSession:
            self.save_procedure(dbSession)
            return self

    def update(self):
        with self.db.getScopedSession() as dbSession:
            self.update_procedure(dbSession)
            return self

    def delete(self, method='soft'):
        with self.db.getScopedSession() as dbSession:
            if method=='hard':
                self.hard_delete_procedure(dbSession)
            else:
                self.soft_delete_procedure(dbSession)
            return self

    def get_one_base_query(self, dbSession: Session, model):
        return dbSession.query(model).filter(model.deleted != 1)

    def get_many_base_query(self, dbSession:Session, model):
        return dbSession.query(model).filter(model.deleted != 1)

    def save_procedure(self, dbSession: Session):
        dbSession.add(self)
        dbSession.commit()
        dbSession.refresh(self)

    def update_procedure(self, dbSession:Session):
        dbSession.merge(self)
        dbSession.commit()

    def hard_delete_procedure(self, dbSession:Session):
        dbSession.delete(self)
        dbSession.commit()

    def soft_delete_procedure(self, dbSession:Session):
        self.deleted = 1
        dbSession.merge(self)
        dbSession.commit()
    
    '''
    # if needed, model can be self updated by merging after making the changes
    # like the example below:

    def selfChangeData(self, *args, **kwargs):
        with self.db.getScopedSession() as dbSession: # Start the session within scope
            self.login = 'updatedFromBaseModel' # Change the data as you want
            dbSession.merge(self) # Merge to the new session
            dbSession.commit() # Commit the changes
            # After that, any changes will not be stored even if commited.
            return 'ok'
    '''