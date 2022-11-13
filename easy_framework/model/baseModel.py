from typing import List
from easy_framework.database import base
from easy_framework.database import Database
from sqlalchemy import Column, DateTime, Integer, SmallInteger
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
            return self

    def update(self, *args, **kwargs):
        with self.getdbSession() as dbSession:
            dbSession.merge(self)
            dbSession.commit()
            return self

    def delete(self, *args, **kwargs):
        with self.getdbSession() as dbSession:
            dbSession.delete(self)
            dbSession.commit()

            return self
    
    '''
    # if needed, model can be self updated by merging after making the changes
    # like the example below:

    def selfChangeData(self, *args, **kwargs):
        with self.getdbSession() as dbSession: # Start the session within scope
            self.login = 'updatedFromBaseModel' # Change the data as you want
            dbSession.merge(self) # Merge to the new session
            dbSession.commit() # Commit the changes
            # After that, any changes will not be stored even if commited.
            return 'ok'
    '''