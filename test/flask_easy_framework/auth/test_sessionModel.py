from datetime import datetime, timedelta

from flask import Flask

from easy_framework.auth.authModel import AuthModel


class TestAuthModel():
    def test_insert_new_session_and_check_it_values(self, flaskApp: Flask):
        with flaskApp.app_context():
            session = AuthModel(user_id=1, token='123').save()
            assert session.user_id == 1
            assert session.token == '123'
            assert type(session.expiration_date) is datetime

    def test_insert_new_session_and_check_its_expiration_datetime(self, flaskApp: Flask):
        with flaskApp.app_context():
            session = AuthModel(user_id=1, token='123').save()
            assert session.expiration_date > datetime.now()
            assert session.expiration_date < datetime.now() + flaskApp.config.get('EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION')
