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


class App():
    app: Flask = Flask(__name__)
    viewList: list[View] = ViewList().viewList

    def __init__(self, test:bool=False, registerViews:bool=True,)->None:
        logger.info("Iniciando API GeraFila...")
        jwt_extended.JWTManager(self.app)
        CORS(self.app)

        self.setConfigs()

        EasyFramework(self.app)
        
        if registerViews is True:
            self.registerViews()

    def registerViews(self):
        logger.info("Cadastrando rotas...")
        for item in self.viewList:
            for route in item.routes:
                logger.debug(f"Rota encontrada: {route} cadastrado com sucesso")
                self.app.add_url_rule(route, view_func=item.as_view(item.name+'/'+route))
            logger.debug(f"Rota cadastrado com sucesso")

    def setConfigs(self):
        self.app.config.update({
            'JSON_AS_ASCII': False,
            'JWT_SECRET_KEY': 'test_key',
            'JWT_ACCESS_TOKEN_EXPIRES': False,
            'EASY_FRAMEWORK_DB_CREATE_ALL':True
        })

    def runApp(self)->None:
        logger.info("Ininiciando app do flask")
        self.app.run(host='0.0.0.0', port="5005", debug=True)

if __name__ == "__main__":
    App().runApp()