from datetime import datetime
import time
import pytest

import sys
sys.path.append('../src')

from plankapy import (
    PasswordAuth, 
    Planka,
    Project,
    Board,
    List,
    Card,
    User,
    QueryableList,
)

planka = Planka('http://localhost:3000', PasswordAuth('demo', 'demo'))

def reset_planka():
    for project in planka.projects.select_where(lambda project: project.name == 'Pytest Project'):
        project.delete()

    for user in planka.users.select_where(lambda user: 'pytest' in user.username):
        user.delete()
reset_planka()

@pytest.fixture
def test_project():
    return planka.projects.pop_where(name='Pytest Project')

@pytest.fixture
def test_board(test_project: Project):
    return test_project.boards.pop_where(name='Pytest Board')

@pytest.fixture
def test_editor():
    return planka.users.pop_where(username='pytest_editor')

@pytest.fixture
def test_viewer():
    return planka.users.pop_where(username='pytest_viewer')

@pytest.fixture
def test_list_a(test_board: Board):
    return test_board.lists.pop()