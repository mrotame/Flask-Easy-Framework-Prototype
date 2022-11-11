from typing import List, Literal
from ..database.base import base
from sqlalchemy import Column, DateTime, Integer, SmallInteger
from src.database.database import Database
from sqlalchemy.sql import func
from datetime import datetime
from flask import current_app
from sqlalchemy.orm import Session


class BaseModel(base):
    __abstract__ = True
    id =  Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now()) 
    deleted = Column(SmallInteger, default=0)

    def getdbSession(self)-> Session:
        class DatabaseSession(object):
            db: Database = current_app.config['database']
            def __enter__(self)-> Session:
                return self.db.session_scoped()

            def __exit__(self, exc_type, exc_val, exc_tb)-> None:
                self.db.session_scoped.remove()
        return DatabaseSession()
        
    def get_one(self, *args, **kwargs)-> 'BaseModel':
        with self.getdbSession() as dbSession:
            return dbSession.query(self.__class__).filter(*args, **kwargs).filter(self.__class__.deleted != 1).first()

    def get_many(self, *args, **kwargs)-> List['BaseModel']:
        with self.getdbSession() as dbSession:
            return dbSession.query(self.__class__).filter(*args, **kwargs).filter(self.__class__.deleted != 1).all()

    def save(self, *args, **kwargs):
        with self.getdbSession() as dbSession:
            dbSession.add(self)
            dbSession.commit()
            dbSession.refresh(self)
            return self, 201

    def update(self, *args, **kwargs):
        with self.getdbSession() as dbSession:
            dbSession.merge(self)
            dbSession.commit()
            return self, 204

    def delete(self, *args, **kwargs):
        with self.getdbSession() as dbSession:
            dbSession.delete(self)
            dbSession.commit()
            
            return 'deleted', 204
