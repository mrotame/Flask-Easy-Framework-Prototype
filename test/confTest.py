from flask import Flask
from pytest import fixture

from easy_framework import Database, EasyFramework


@fixture(scope="session")
def flaskApp():
    app = Flask(__name__)
    app.config['EASY_FRAMEWORK_DB_DBNAME'] = 'testdb.db'
    app.config['EASY_FRAMEWORK_DB_URI'] = '/'
    EasyFramework(app)
    return app


@fixture(scope='session')
def database(flaskApp: Flask) -> Database:
    return flaskApp.config['EASY_FRAMEWORK_DATABASE']


@fixture(autouse=True)
def between_tests(database: Database):
    database.dbConfig.create_all()
    yield
    database.dbConfig.close_all_sessions()
    database.dbConfig.delete_all()
