from sqlalchemy import create_engine
from sqlalchemy.orm import (Session, declarative_base, scoped_session,
                            sessionmaker)
from sqlalchemy.orm.session import close_all_sessions, engine

from src.models import *

from .base import base


class DbConfig():
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

    def __init__(
        self,
        dialect,
        uri,
        databaseName,
        port,
        username,
        password,
        create_all,  
    ) -> None :
        self.__dialect = dialect
        self.username = username
        self.__databaseName = databaseName
        self.__password = password
        self.__port = port
        self.__uri = uri
        
        self.base = base

        self.string_url = self.getStringUrl()
        self.engine = self.createEngine()

        self.session = sessionmaker(bind=self.engine)
        self.session_scoped = scoped_session(sessionmaker(bind=self.engine))
        if(create_all): self.create_all()

    def createEngine(self)-> engine:
        return create_engine(
            self.string_url, 
            pool_recycle=300,
            pool_pre_ping=True,
            echo=self.echo,
        ) 
    
    def getStringUrl(self)->str:
        if self.__dialect == 'sqlite':
            return f'{self.__dialect}://{self.__uri}{self.__databaseName}'

        return f'{self.__dialect}://{self.__username}:{self.__password}@{self.__uri}:{self.__port}/{self.__databaseName}'

    def create_all(self)-> None:
        self.base.metadata.create_all(self.engine)

    def delete_all(self)-> None:
        self.base.metadata.drop_all(self.engine)

    def close_all_sessions(self)->None:
        close_all_sessions()