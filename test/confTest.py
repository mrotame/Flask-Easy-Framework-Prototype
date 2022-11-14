from datetime import datetime

import sqlalchemy as sa
from flask import Flask
from pytest import fixture

from easy_framework import Database, EasyFramework
from easy_framework.model import BaseModel


@fixture(scope="session")
def flaskApp():
    app = Flask(__name__)
    app.config['EASY_FRAMEWORK_DB_DBNAME'] = 'testdb.db'
    app.config['EASY_FRAMEWORK_DB_URI'] = '/'
    EasyFramework(app)
    return app

@fixture(scope='session')
def database(flaskApp: Flask)-> Database:
    return flaskApp.config['database']

@fixture(autouse=True)
def between_tests(database: Database):
    database.dbConfig.create_all()
    yield
    database.dbConfig.close_all_sessions()
    database.dbConfig.delete_all()


    
class ModelTest(BaseModel):
    __tablename__ = 'TestModel'
    id = sa.Column(sa.Integer, primary_key=True)
    test_datetime = sa.Column(sa.DateTime, default=datetime.now())
    info = sa.Column(sa.String)
