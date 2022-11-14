import os

from sqlalchemy import create_engine
from sqlalchemy.orm import (Session, declarative_base, scoped_session,
                            sessionmaker)

from src.models import *

from .base import base


class Database():
    __dialect: str
    __databaseName: str
    __uri: str
    __port: str
    __username: str
    __password: str

    echo: bool = False
    base: declarative_base
    engine: create_engine
    session: Session
    session_scoped: scoped_session

    def __init__(self, create_all=False, pool_size=1, max_overflow = 2, pool_timeout=300, pool_recycle=300) -> None :
        create_all = True if os.environ.get('database_create_all') == 'True' else create_all
        self.__dialect = os.environ.get('database_dialect')
        self.__uri = os.environ.get('database_uri')
        self.__port = os.environ.get('database_port')
        self.__databaseName = os.environ.get('database_name')
        self.__username = os.environ.get('database_user')
        self.__password = os.environ.get('database_pwd')

        self.pool_size=pool_size
        self.max_overflow = max_overflow  
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle
        
        self.base = base

        # Postgresql atring and engine

        # string_url = f'{self.__dialect}://{self.__username}:{self.__password}@{self.__uri}:{self.__port}/{self.__databaseName}'
        # self.engine = create_engine(
        #     string_url, 
        #     pool_size=pool_size,
        #     max_overflow=max_overflow,
        #     pool_recycle=pool_recycle,
        #     pool_pre_ping=True,
        #     pool_timeout=pool_timeout,
        #     pool_use_lifo=True,
        #     echo=self.echo,
        #     connect_args={
        #         "keepalives": 1,
        #         "keepalives_idle": 30,
        #         "keepalives_interval": 10,
        #         "keepalives_count": 5,
        #     }
        # )

        # sqlite string and engine
        
        string_url = f'{self.__dialect}:///app.db'
        self.engine = create_engine(
            string_url, 
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
            echo=self.echo,
        )

        self.session = sessionmaker(bind=self.engine)
        self.session_scoped = scoped_session(sessionmaker(bind=self.engine))

        if(create_all): self.create_all()

    def create_all(self) -> None:
        self.base.metadata.create_all(self.engine)

    def delete_all(self)-> None:
        self.base.metadata.drop_all(self.engine)