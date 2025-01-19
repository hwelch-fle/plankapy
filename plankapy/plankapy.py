import sys
sys.path.append('..')

from utils.routes import Routes, Route
from utils.models import *
from utils.handlers import TokenAuth, PasswordAuth, BaseAuth, JSONHandler
from utils.constants import *

class Planka:
    def __init__(self, url: str, auth: BaseAuth=None):
        if not auth:
            raise ValueError('No authentication method provided')
        self.url = url
        self.auth = auth
        self.handler = self._create_session(auth)
        self.routes = Routes(self.handler)

    def _create_session(self, auth: BaseAuth) -> JSONHandler:
        handler = JSONHandler(self.url)
        handler.headers['Authorization'] = auth.authenticate(self.url)
        return handler

if __name__ == '__main__':
    from pprint import pprint
    auth = PasswordAuth(username_or_email='demo', password='demo')
    planka = Planka('http://localhost:3000', auth=auth)

    get_index = planka.routes.get_project_index()
    pprint(get_index())