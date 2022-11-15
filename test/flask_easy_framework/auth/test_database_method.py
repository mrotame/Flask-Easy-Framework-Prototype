from easy_framework.auth.databaseMethod import DatabaseMethod
from flask import Flask

class TestDatabaseMethod():
    def test_generate_hash_token(self, flaskApp: Flask):
        with flaskApp.test_request_context():
            assert len(DatabaseMethod().generateHashToken()) >= 128

    def test_create_new_token_and_save_at_database(self, flaskApp: Flask):
        with flaskApp.test_request_context():
            DatabaseMethod().generateToken()