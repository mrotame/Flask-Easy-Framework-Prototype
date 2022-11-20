from typing import TYPE_CHECKING

from flask import current_app, g, has_request_context
from werkzeug.local import LocalProxy

from .userModel import UserModel

current_user: UserModel = LocalProxy(lambda: __get_user())
if TYPE_CHECKING:
    from ..auth.authManager import AuthManager


def __get_user()->UserModel:
    if has_request_context:
        if 'user' not in g:
            authManager: AuthManager = current_app.authManager
            authManager.loadUser()
        return g.user
