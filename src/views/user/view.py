from flask import request
from flask.views import View as flaskView
from ..baseView.genericApiView import GenericApiView
from src.serializers.userSerializer import UserSerializer
# from src.exceptions.api_exceptions import ValidationError

class View(GenericApiView, flaskView):
    name = 'userView'
    routes = ['/user', '/user/', '/user/<string:id>']
    field_lookup = 'id'
    methods=['GET','POST','PATCH', 'DELETE']
    serializer = UserSerializer

    def validations(self, *args, **kwargs):
        pass
        # if request.method != 'GET' and self.field_lookup in kwargs:
        #     raise ValidationError('page not found',404)

    def get(self, *args, **kwargs):
        if self.field_lookup in kwargs:
            return self.getSingleEntity(*args, **kwargs)
        else:
            return self.getAllEntities(*args, **kwargs)

    def post(self, *args, **kwargs): 
        return self.createEntity(*args, **kwargs)

    def patch(self, *args, **kwargs): 
        return self.updateEntity(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.deleteEntity('soft', *args, **kwargs)