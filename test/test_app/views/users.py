from flask import Flask

from ..setupTest import SetupTest


class TestApp(SetupTest):
    def url(self):
        return '/user'

    def json(self):
        return {
            'login': 'teste',
            'password': '123'
        }

    def test_create_new_user(self, apiApp: Flask):
        res = apiApp.test_client().post(self.url(), json=self.json())
        assert res.status_code == 201
        json = res.get_json()
        assert 'id' in json
        assert 'login' in json
        assert 'password' not in json

    def test_get_created_user(self, apiApp: Flask):
        created_user = apiApp.test_client().post(self.url(),json=self.json())

        get_url = self.url() + f'?id={created_user.get_json().get("id")}'
        res = apiApp.test_client().get(get_url)
        json = res.get_json()
        assert created_user.get_json() == json

    
