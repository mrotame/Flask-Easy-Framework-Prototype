from flask import Flask
from easy_framework import EasyFramework
from app import App
from pytest import fixture

class SetupTest():
    @fixture(scope='session')
    def apiApp(self):
        return App().app

        

    