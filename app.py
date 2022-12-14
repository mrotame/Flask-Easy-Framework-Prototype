import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

import os

import flask_jwt_extended as jwt_extended
from flask import Flask
from flask.views import View
from flask_cors import CORS
from loguru import logger

from easy_framework import EasyFramework
from src.views.viewList import ViewList
from src.models.user import User


class App():
    app: Flask = Flask(__name__)
    viewList: list[View] = ViewList().viewList

    def __init__(self, test:bool=False, registerViews:bool=True,)->None:
        logger.info("Loading configs...")
        jwt_extended.JWTManager(self.app)
        CORS(self.app)

        self.setConfigs()

        EasyFramework(self.app)
        
        if registerViews is True:
            self.registerViews()

    def registerViews(self):
        logger.info("Registering routes...")
        for item in self.viewList:
            for route in item.routes:
                logger.debug(f"Route detected: {route} - registered succesfull")
                self.app.add_url_rule(route, view_func=item.as_view(item.name+'/'+route))
            logger.debug(f"All routes registered")

    def setConfigs(self):
        self.app.config.update({
            'JWT_SECRET_KEY': 'test_key',
            'JWT_ACCESS_TOKEN_EXPIRES': False,
            'EASY_FRAMEWORK_DB_CREATE_ALL':True,
            'EASY_FRAMEWORK_USER_MODEL': User
        })

    def runApp(self)->None:
        logger.info("Starting flask app ")
        self.app.run(host='0.0.0.0', port="5005", debug=True)

if __name__ == "__main__":
    App().runApp()