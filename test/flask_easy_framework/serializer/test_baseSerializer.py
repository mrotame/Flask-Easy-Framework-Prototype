from test.conftest import SerializerTest
from flask import Flask

class TestBaseSerializer():
    def test_(self, flaskApp: Flask):
        assert False
        # with flaskApp.test_request_context('/',data={}):
        #     serializer = SerializerTest() 