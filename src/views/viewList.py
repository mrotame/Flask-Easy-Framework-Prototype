from typing import List
from flask.views import View
from .user.view import View as userView

class ViewList():
    viewList: List[View] = [
        userView
    ]