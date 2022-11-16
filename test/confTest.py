from datetime import datetime

import sqlalchemy as sa
from flask import Flask
from pytest import fixture

from easy_framework import Database, EasyFramework
from easy_framework.model import BaseModel
from easy_framework.serializer import BaseSerializer
from marshmallow import fields


@fixture(scope="session")
def flaskApp():
    app = Flask(__name__)
    app.config['EASY_FRAMEWORK_DB_DBNAME'] = 'testdb.db'
    app.config['EASY_FRAMEWORK_DB_URI'] = '/'
    EasyFramework(app)
    return app

@fixture(scope='session')
def database(flaskApp: Flask)-> Database:
    return flaskApp.config['EASY_FRAMEWORK_DATABASE']

@fixture(autouse=True)
def between_tests(database: Database):
    database.dbConfig.create_all()
    yield
    database.dbConfig.close_all_sessions()
    database.dbConfig.delete_all()


class ModelTest(BaseModel):
    __tablename__ = 'TestModel'
    username = sa.Column(sa.String)
    password = sa.Column(sa.String)
    test_datetime = sa.Column(sa.DateTime, default=datetime.now())
    info = sa.Column(sa.String)

class SerializerTest(BaseSerializer):
    model = ModelTest
    class Meta():
        test_datetime = fields.DateTime()
        info = fields.Str()

    exclude_from_methods = {
        'POST':'id',
        'GET': 'password',
        'PATCH':'id'
    }