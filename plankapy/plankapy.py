import sys
sys.path.append('..')

from utils.routes import Routes
from utils.models import (
    Action,
    Archive,
    Attachment,
    Board,
    BoardMembership,
    Card,
    Stopwatch,
    CardLabel,
    CardMembership,
    CardSubscription,
    IdentityProviderUser,
    Label,
    List,
    Notification,
    Project,
    ProjectManager,
    Task,
    User,
)
from utils.handlers import (
    TokenAuth, 
    PasswordAuth, 
    BaseAuth, 
    JSONHandler,
)

from utils.constants import (
    Gradient,
    LabelColor,
    ActionType,
    BoardRole,
    Background,
    BackgroundImage,
    get_position,
    set_position,
)

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
    auth = PasswordAuth(username_or_email='demo', password='demo')
    planka = Planka('http://localhost:3000', auth=auth)

    get_projects = planka.routes.get_project_index()

    for project in get_projects:
        project = Project(**project)
        print(project.name)
        get_current_project = planka.routes.get_project(id=project.id)
        included = get_current_project()['included']

        if len(included['boards']) == 0:
            post_board = planka.routes.post_board(projectId=project.id)
            for board_name in ('Board 1', 'Board 2', 'Board 3'):
                board = Board(name=board_name,
                          position=set_position(1),
                          projectId=project.id)
                post_board(**board)
        
        # Update included after adding new boards
        included = get_current_project()['included']

        # TODO: Build the 'included' key into the model so
        # a nested response can be unrolled into correct Model types
        for board in included['boards']:
            board = Board(**board)
            print('\t'+board.name)