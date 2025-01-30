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

@pytest.fixture
def test_list_b(test_board: Board):
    return test_board.lists.pop(1)

@pytest.fixture
def test_card(test_list_a: List):
    return test_list_a.cards.pop()

@pytest.fixture(scope='session', autouse=True)
def cleanup():
    try:
        yield
    finally:
        pass

    @pytest.fixture(scope='session', autouse=True)
    def restore(test_project: Project, test_editor: User, test_viewer: User):
        test_project.delete()
        test_editor.delete()
        test_viewer.delete()

def test_create_users():
    # Editor user
    assert planka.create_user('pytest_editor', 'pytest_editor@plankapy.com', 'sdfnlksadfanksd', 'Editor'), 'Failed to create editor user'
    # Viewer user
    assert planka.create_user('pytest_viewer', 'pytest_viewer@plankapy.com', 'wddnflkasjfd', 'Viewer'), 'Failed to create viewer user'

def test_restore_user(test_viewer: User):
    
    deleted_user = test_viewer.delete()
    assert deleted_user, 'Failed to delete user'

    # Restore user (Passwords cannot be restored)
    restored_user = planka.create_user(deleted_user.username, deleted_user.email, 'sdfnlksadfanksd', deleted_user.name)

    assert restored_user.username == deleted_user.username, 'Failed to restore username'

    # New ID for restored user
    assert deleted_user != restored_user, 'Failed to restore user'


def test_create_project():
    assert planka.create_project('Pytest Project'), 'Failed to create project'

def test_change_gradient(test_project: Project):
    for gradient in test_project.gradients:
        test_project.set_background_gradient(gradient)
        assert test_project.background.get('name') == gradient, f'{test_project.background.get("name")} != {gradient}'

    # Test backwards compatibility
    for gradient in test_project.gradients:
        with test_project.editor():
            test_project.background = gradient
        assert test_project.background.get('name') == gradient, f'{test_project.background.get("name")} != {gradient}'

def test_set_project_background(test_project: Project):
    assert test_project.set_background_image('https://planka.app/cms-content/1/uploads/images/606395ea59a7c35fa8/demo28594da7dd7582c7f4c59bb263d1048e.gif'), 'Failed to set background'        

def test_add_project_manager(test_project: Project, test_editor: User):
    assert test_project.add_project_manager(test_editor), 'Failed to add manager'
    assert test_editor in test_project.managers, f'{test_editor.name} not in {test_project.name} managers'
    assert test_project in test_editor.manager_of, f'{test_editor.name} not manager of {test_project.name}'

def test_remove_project_manager(test_project: Project, test_editor: User):
    assert test_project.remove_project_manager(test_editor), 'Failed to remove manager'
    assert test_editor not in test_project.managers, f'{test_editor.name} still in {test_project.name} managers'
    assert test_project not in test_editor.manager_of, f'{test_editor.name} still manager of {test_project.name}'

def test_remove_user_avatar(test_editor: User, test_viewer: User):
    assert not test_editor.remove_avatar(), 'Failed to remove avatar'
    assert not test_viewer.remove_avatar(), 'Failed to remove avatar'

def test_set_user_avatar(test_editor: User, test_viewer: User):
    assert test_editor.set_avatar('https://planka.app/cms-content/1/uploads/site/sitelogomenue.png'), 'Failed to set avatar'
    assert test_viewer.set_avatar('https://www.python.org/static/img/python-logo-large.c36dccadd999.png'), 'Failed to set avatar'

def test_create_board(test_project: Project):
    assert test_project.create_board('Pytest Board'), 'Failed to create board'

def test_add_editor_to_board(test_board: Board, test_editor: User):
    assert test_board.add_user(test_editor, role='editor'), 'Failed to add editor'
    assert test_editor in test_board.editors, f'{test_editor.name} not in {test_board.name} editors'

def test_add_viewer_to_board(test_board: Board, test_viewer: User):
    assert test_board.add_user(test_viewer, role='viewer'), 'Failed to add viewer'
    assert test_viewer in test_board.viewers, f'{test_viewer.name} not in {test_board.name} viewers'

def test_create_labels(test_board: Board):
    assert (label := test_board.create_label('Test Label')), 'Failed to create label'
    colors = label.colors
    assert label.delete(), 'Failed to delete label'

    for color in colors:
        assert (label := test_board.create_label(color, color=color)), f'Failed to create label with color {color}'
        assert label.name == color, f'{label.name} != {color}'
        assert label.color == color, f'{label.color} != {color}'

def test_create_list(test_board: Board):
    assert test_board.create_list('Pytest List 1', position=1), 'Failed to create list 1'
    assert test_board.create_list('Pytest List 2', position=2), 'Failed to create list 2'

def test_create_card(test_list_a: List):
    assert test_list_a.create_card('Pytest Card'), 'Failed to create card'

def test_create_card_tasks(test_card: Card):
    for i in range(1,11):
        test_card.add_task(f'Task {i}', position=i)

def test_create_card_comments(test_card: Card):
    for i in range(1,11):
        test_card.add_comment(f'Comment {i}')

def test_create_card_due_date(test_card: Card):
    now = datetime.now()
    assert test_card.set_due_date(now), 'Failed to set due date'
    assert test_card.due_date.date() == now.date(), f'{test_card.due_date.date()} != {now.date()}'
    assert test_card.dueDate[0:10] == now.isoformat()[0:10], f'{test_card.dueDate[0:10]} != {now.isoformat()[0:10]}'

def test_create_card_assignees(test_card: Card, test_editor: User):
    assert test_card.add_member(test_editor), 'Failed to add assignee'
    assert test_editor in test_card.members, f'{test_editor.name} not in {test_card.name}'

def test_create_card_labels(test_card: Card, test_board: Board):
    for label in test_board.labels:
        assert test_card.add_label(label), f'Failed to add label {label.name}'

def test_card_duplicate(test_card: Card):
    assert test_card.duplicate(), 'Failed to duplicate card'

def test_card_move(test_card: Card, test_list_b: List):
    assert test_card.move(test_list_b), 'Failed to move card'
    assert test_card.list == test_list_b, f'Failed to move card to {test_list_b.name}'

def test_card_stopwatch(test_card: Card):
    assert test_card.add_stopwatch(), 'Failed to add stopwatch'

    test_card.stopwatch.start()
    time.sleep(3)
    test_card.stopwatch.stop()
    assert test_card.stopwatch.total == 3, f'Stopwatch failed: {test_card.stopwatch.total} != 3'

    test_card.stopwatch.set(hours=1)
    assert test_card.stopwatch.total == 3600, f'Setting time failed {test_card.stopwatch.total} != 3600'

    test_card.stopwatch.set()
    assert test_card.stopwatch.total == 0, f'Reset failed: {test_card.stopwatch.total}'

    assert test_card.remove_stopwatch()
    assert test_card.stopwatch.startedAt is None and test_card.stopwatch.total == 0, 'Failed to delete stopwatch'


def main_test():
    # Tests run in order of declaration
    tests = [
        reset_planka,
        test_create_users,
        test_create_project,
        test_change_gradient,
        test_add_project_manager,
        test_remove_project_manager,
        test_create_board,
        test_add_editor_to_board,
        test_add_viewer_to_board,
        test_create_labels,
        test_create_list,
        test_create_card,
        test_card_duplicate,
        test_create_card_tasks,
        test_create_card_comments,
        test_create_card_due_date,
        test_create_card_assignees,
        test_create_card_labels,
        test_card_move,
        test_card_stopwatch,
        test_restore_user,
    ]

    for test in tests:
        name = test.__name__.replace('test_', '').replace('_', ' ').title()
        print(f'Running {name}...')
        test()
        print(f'{name} passed!\n')

    print('All tests passed!')

if __name__ == '__main__':
    main_test()
    