from flask import request
from flask.views import View as flaskView
from ..baseView.genericApiView import GenericApiView
from src.serializers.userSerializer import UserSerializer


class View(GenericApiView, flaskView):
    name = 'userView'
    routes = ['/user']
    field_lookup = 'id'
    serializer = UserSerializer

    def get(self):
        if self.field_lookup in request.args:
            self.singleEntity()
        else:
            self.listEntities()

    def post(self): 
        return 'ok'

    def patch(self): 
        return 'ok'
