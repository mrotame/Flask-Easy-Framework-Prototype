from ..database.base import base
from sqlalchemy import Column, BigInteger, DateTime
from sqlalchemy.sql import func
from datetime import datetime

class BaseModel(base):
    __abstract__ = True
    id =  Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.now())