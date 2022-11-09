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
        
    def get_one(self, model, *args, **kwargs):
        with self.getdbSession() as dbSession:
            return dbSession.query(model).filter(*args, **kwargs).first()

    def get_many(self, model, *args, **kwargs):
        with self.getdbSession() as dbSession:
            return dbSession.query(model).filter(*args, **kwargs).all()

    def save(self, model, *args, **kwargs):
        with self.getdbSession() as dbSession:
            model = model(*args, **kwargs)
            dbSession.add(model)
            dbSession.commit()
            dbSession.refresh(model)
            return model

    def update(self, model, field_lookup, field_lookup_value, *args, **kwargs):
        with self.getdbSession() as dbSession:
            entity = dbSession.query(model).filter_by(**{field_lookup: field_lookup_value}).first()
            for info in kwargs:
                setattr(entity, info, kwargs[info])
            dbSession.commit()
            dbSession.refresh(entity)
            return entity


    def delete(self, model, field_lookup, softdelete, *args, **kwargs):
        with self.getdbSession() as dbSession:
            pass
