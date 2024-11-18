from utils.routes import Routes, Route
from utils.models import *
from utils.handlers import create_session

from typing import Generator

# This implementation is current;y prettly slow, about 2s for reading all boards and lists in an instance
class Planka:
    def __init__(self, url: str, *, username_or_email: str=None, password: str=None, token: str=None):
        if not url:
            raise ValueError('A URL must be provided')
        
        if token:
            self.handler = create_session(url, token=token)
        elif username_or_email and password:
            self.handler = create_session(url, emailOrUsername=username_or_email, password=password)
        else:
            raise ValueError('Either a token or username/email and password must be provided') 
        self.routes = Routes(self.handler)
                
    def projects(self) -> Generator[Project, None, None]:
        yield from (Project.from_dict(project) for project in self.routes.projects_index()()['items'])
    
    def boards(self, project: Project) -> Generator[Board, None, None]:
        yield from (Board.from_dict(board) for board in self.routes.projects_show(project.id)()['included']['boards'])
    
    def lists(self, board: Board) -> Generator[List, None, None]:
        yield from (List.from_dict(lst) for lst in self.routes.boards_show(board.id)()['included']['lists'])
    
if __name__ == '__main__':
    pass