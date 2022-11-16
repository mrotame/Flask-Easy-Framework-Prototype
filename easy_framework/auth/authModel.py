from ..model import BaseModel
import sqlalchemy as sa
from flask import current_app
from datetime import datetime

class AuthModel(BaseModel):
    __tablename__ = 'FLASK_EASY_FRAMEWORK_SESSION'
    token = sa.Column(sa.String(256), nullable=False)
    user_id = sa.Column(sa.Integer, nullable=False)
    expiration_date = sa.Column(sa.DateTime, nullable=False)

    def save(self):
        self.expiration_date=datetime.now()+current_app.config.get('EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION')
        return super().save()