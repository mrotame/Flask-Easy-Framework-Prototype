from flask import request
from flask.views import View as flaskView
from easy_framework.view import GenericApiView
from ...serializers.userSerializer import UserSerializer
from easy_framework.exception.apiExceptions import ValidationError, AuthMissingError
from ...models.user import User

class View(GenericApiView, flaskView):
    name = 'userView'
    routes = ['/user', '/user/', '/user/<string:id>']
    field_lookup = 'id'
    methods=['GET','POST','PATCH', 'DELETE']
    serializer = UserSerializer
    model = User

    def validations(self, *args, **kwargs):
        if request.method == 'POST' and self.field_lookup in request.args:
            raise ValidationError('page not found',404)

    def get(self):
        if self.field_lookup in request.args:
            return self.getSingleEntity()
        else:
            return self.getAllEntities()

    def post(self): 
        return self.createEntity()

    def patch(self): 
        return self.updateEntity()

    def delete(self):
        return self.deleteEntity('soft')