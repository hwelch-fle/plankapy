import sys
sys.path.append('..')

from utils.routes import Routes, Route
from utils.models import *
from utils.handlers import create_session
from utils.constants import *

# This implementation is current;y prettly slow, about 2s for reading all boards and lists in an instance
class Planka:
    def __init__(self, url: str, *, username_or_email: str=None, password: str=None, token: str=None):        
        if token:
            self.handler = create_session(url, token=token)
        elif username_or_email and password:
            self.handler = create_session(url, emailOrUsername=username_or_email, password=password)
        else:
            raise ValueError('Either a token or username/email and password must be provided')
        self.routes = Routes(self.handler)

if __name__ == '__main__':
    import time
    import random
    planka = Planka('http://localhost:3000', username_or_email='demo', password='demo')
    while True:
        for project in planka.routes.projects_index():
            project = Project(**project)
            gradient = random.choice(Gradient.__args__)

            project.background = Background(gradient).__dict__
            project.name = gradient
            changed_background = planka.routes.projects_update(project.id)(**dict(project))
            changed_background = Project(**changed_background['item'])
            print(f'{changed_background.name} changed to {changed_background.background}')
        time.sleep(1)