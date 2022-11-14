from flask import Flask
from sqlalchemy.orm import Session

from .dbConfig import DbConfig


# Session factory to be used within scope
class SessionFactory():
    def __init__(self, cls: 'Database'):
        self.cls = cls

    def __enter__(self):
        return self.cls.getNewSession()

    def __exit__(self, exception_type, exception_value, traceback):
        self.cls.closeSession()

class Database():
    dbConfigClass = DbConfig
    dbSession: Session = None
    
    def __init__(self, app:Flask)-> None:
        self.app = app
        self.dbConfig = self.getDbConfig()

    def getDbConfig(self)->DbConfig:
        return self.dbConfigClass(
            create_all = self.app.config.get('EASY_FRAMEWORK_DB_CREATE_ALL'),
            dialect = self.app.config.get('EASY_FRAMEWORK_DB_DIALECT'),
            uri = self.app.config.get('EASY_FRAMEWORK_DB_URI'),
            port = self.app.config.get('EASY_FRAMEWORK_DB_PORT'),
            databaseName = self.app.config.get('EASY_FRAMEWORK_DB_DBNAME'),
            username = self.app.config.get('EASY_FRAMEWORK_DB_USERNAME'),
            password = self.app.config.get('EASY_FRAMEWORK_DB_PASSWORD')
        )

    # session = getNewSession()
    def getNewSession(self)-> Session:
        return self.dbConfig.session_scoped()

    # with getScopedSession() as dbSession:
    def getScopedSession(self)-> SessionFactory:
        return SessionFactory(self)

    # database.openSession()
    # database.dbSession
    def openSession(self)->None:
        self.dbSession = self.getNewSession()

    # close any opened session
    def closeSession(self)-> None:
        return self.dbConfig.session_scoped.remove()

    # with database.setScopedSession():
    # database.dbSession
    def setScopedSession(self)->None:
        class SessionFactory():
            def __enter__(factorySelf):
                self.openSession()

            def __exit__(factorySelf, exception_type, exception_value, traceback):
                self.closeSession()
        return SessionFactory()