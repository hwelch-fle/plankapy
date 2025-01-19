import sys
sys.path.append('..')

from utils.routes import Routes, Route
from utils.models import *
from utils.handlers import create_session
from utils.constants import *

# This implementation is current;y prettly slow, about 2s for reading all boards and lists in an instance
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
    import time
    import random
    planka = Planka('http://localhost:3000', username_or_email='demo', password='demo')

    while True:
        loop_start = time.time()
        prjs = 0
        for project in planka.routes.projects_index():
            prjs += 1
            project = Project(**project)
            gradient = random.choice(Gradient.__args__)
    
            project.background = Background(gradient).__dict__
            project.name = gradient
            changed_background = planka.routes.projects_update(project.id)(**project)
            changed_background = Project(**changed_background['item'])
            print(f'{changed_background.name} changed to {changed_background.background}')
        loop_end = time.time()
        print(f"{(loop_end-loop_start)/prjs:.2f} seconds per update")

    #for grad in Gradient.__args__:
    #    create_project = planka.routes.projects_create()
    #
    #    project = Project(name=grad, background=Background(grad).__dict__)
    #    project.validate()
    #    print(dict(**project))
    #    resp = create_project(**project)
    #    print(f"Created {grad}: {resp}")