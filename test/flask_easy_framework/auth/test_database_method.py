import pytest
from flask import Flask, g
from pytest import fixture

from easy_framework.auth.authModel import AuthModel
from easy_framework.auth.databaseMethod import DatabaseMethod
from easy_framework.exception.apiExceptions import InvalidCredentials
from easy_framework.user.userModel import UserModel
from easy_framework.user.userMixin import AnonymousUser, UserMixin


class TestDatabaseMethod():
    def authJson(self):
        return {
            'login': 'test',
            'password': 'test'
        }

    @fixture
    def userModel(self, flaskApp: Flask):
        return flaskApp.config.get('EASY_FRAMEWORK_USER_MODEL')

    def test_generate_hash_token(self, flaskApp: Flask):
        with flaskApp.test_request_context('/', json=self.authJson()):
            assert len(DatabaseMethod().generateHashToken()) >= 128

    def test_request_a_new_token_with_no_user_registered_and_get_404(self, flaskApp: Flask):
        with flaskApp.test_request_context('/', json=self.authJson()):
            with pytest.raises(InvalidCredentials) as exc_info:
                DatabaseMethod().generateSession(None)
                assert type(exc_info.value) is InvalidCredentials

    def test_request_a_new_token_and_get_token(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(login='test', password='test').save()
            assert (t := DatabaseMethod().generateSession(user)
                    ) is not None and type(t) is str

    def test_request_a_new_token_and_check_token_in_database(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethod().generateSession(user)
            tokenModel: AuthModel = AuthModel.get.one(AuthModel.token == token)
            assert tokenModel is not None
            assert tokenModel.user_id == user.id

    def test_check_an_existent_token(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethod().generateSession(user)
            with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
                DatabaseMethod().loadUser()
                assert g.user is not None

    def test_check_an_nonexistent_token(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethod().generateHashToken()
        with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethod().loadUser()
            assert isinstance(g.user, AnonymousUser)

    def test_get_user_from_existent_token(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethod().generateSession(user)
        with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethod().loadUser()
            assert isinstance(g.user, UserMixin)
