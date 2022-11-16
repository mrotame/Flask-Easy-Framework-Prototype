import pytest
from flask import Flask
from pytest import fixture

from easy_framework.auth.databaseMethod import DatabaseMethod
from easy_framework.exception.apiExceptions import InvalidCredentials
from easy_framework.user.userModel import UserModel
from easy_framework.auth.authModel import AuthModel


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
                DatabaseMethod().generateToken()
                assert type(exc_info.value) is InvalidCredentials

    def test_request_a_new_token_and_get_token(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            userModel(login='test', password='test').save()
            assert (t := DatabaseMethod().generateToken()
                    ) is not None and type(t) is str

    def test_request_a_new_token_and_check_token_in_database(self, flaskApp: Flask, userModel:UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            userModel = userModel(
                login='test', password='test')
            userModel.save()
            token = DatabaseMethod().generateToken()
            tokenModel: AuthModel = AuthModel.get.one(AuthModel.token==token) 
            assert tokenModel is not None
            assert tokenModel.user_id == userModel.id
            
