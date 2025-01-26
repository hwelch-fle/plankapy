from datetime import datetime
import time

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
)

planka = Planka('http://localhost:3000', PasswordAuth('demo', 'demo'))

def reset_planka():
    for project in planka.projects:
        project.delete()

    for user in planka.users:
        user.delete() if user != planka.me else None

def create_users() -> tuple[User, User]:
    # Editor user
    assert (editor := planka.create_user('editor', 'editor@plankapy.com', 'sdfnlksadfanksd', 'Editor'))
    # Viewer user
    assert (viewer := planka.create_user('viewer', 'viewer@plankapy.com', 'wddnflkasjfd', 'Viewer'))

    return editor, viewer

def test_restore_user():
    user, *_ = [user for user in planka.users if user != planka.me]
    
    deleted_user = user.delete()
    assert deleted_user

    # Restore user (Passwords cannot be restored)
    restored_user = planka.create_user(deleted_user.username, deleted_user.email, 'sdfnlksadfanksd', deleted_user.name)

    assert restored_user.username == deleted_user.username

    # New ID for restored user
    assert deleted_user != restored_user


def test_create_project():
    assert (project := planka.create_project('Test Project'))
    assert project.name == 'Test Project'

def test_change_gradient():
    project = planka.projects[0]
    for gradient in project.gradients:
        with project.editor():
            project.background = gradient
        
        assert project.background.get('name') == gradient

def test_add_project_manager():
    project = planka.projects[0]
    user, *_ = [u for u in planka.users if u.username == 'editor']

    assert project.add_project_manager(user)
    assert user in project.managers
    assert project in user.manager_of

def test_remove_project_manager():
    project = planka.projects[0]
    user, *_ = [u for u in planka.users if u.username == 'editor']

    assert project.remove_project_manager(user)
    assert user not in project.managers
    assert project not in user.manager_of

def test_create_board():
    project = planka.projects[0]
    assert (board := project.create_board('Test Board'))
    assert board.name == 'Test Board'

def test_add_editor_to_board():
    project = planka.projects[0]
    board = project.boards[0]
    user, *_ = [u for u in planka.users if u.username == 'editor']

    assert board.add_user(user, role='editor')
    assert user in board.editors

def test_add_viewer_to_board():
    project = planka.projects[0]
    board = project.boards[0]
    user, *_ = [u for u in planka.users if u.username == 'viewer']

    assert board.add_user(user, role='viewer')
    assert user in board.viewers

def test_create_labels():
    project = planka.projects[0]
    board = project.boards[0]
    assert (label := board.create_label('Test Label'))
    colors = label.colors
    label.delete()

    for color in colors:
        assert (label := board.create_label(color, color=color))
        assert label.name == color
        assert label.color == color

def test_create_list():
    project = planka.projects[0]
    board = project.boards[0]
    assert (list_ := board.create_list('Test List'))
    assert list_.name == 'Test List'

    board.create_list('Test List 2')

def test_create_card():
    project = planka.projects[0]
    board = project.boards[0]
    list_ = board.lists[0]
    assert (card := list_.create_card('Test Card'))
    assert card.name == 'Test Card'

def test_create_card_tasks():
    project = planka.projects[0]
    board = project.boards[0]
    card = board.cards[0]
    for i in range(1,10):
        card.add_task(f'Task {i}', position=i)

def test_create_card_comments():
    project = planka.projects[0]
    board = project.boards[0]
    card = board.cards[0]
    for i in range(1,10):
        card.add_comment(f'Comment {i}')

def test_create_card_due_date():
    project = planka.projects[0]
    board = project.boards[0]
    card = board.cards[0]
    now = datetime.now()
    card.set_due_date(now)
    assert card.due_date.date() == now.date(), f"{card.due_date.date()} != {now.date()}"
    assert card.dueDate[0:10] == now.isoformat()[0:10]

def test_create_card_assignees():
    project = planka.projects[0]
    board = project.boards[0]
    card = board.cards[0]
    user, *_ = [u for u in planka.users if u.username == 'editor']
    card.add_member(user)
    assert user in card.members

def test_create_card_labels():
    project = planka.projects[0]
    board = project.boards[0]
    card = board.cards[0]
    label = board.labels[0]
    for label in board.labels:
        card.add_label(label)

def test_card_duplicate():
    project = planka.projects[0]
    board = project.boards[0]
    card = board.cards[0]
    assert (duplicate := card.duplicate())
    assert duplicate.name == card.name

def test_card_move():
    project = planka.projects[0]
    board = project.boards[0]
    card = board.cards[0]
    list_ = board.lists[1]
    card.move(list_)
    assert card.list == list_

def test_card_stopwatch():
    project = planka.projects[0]
    board = project.boards[0]
    card = board.cards[0]
    card.add_stopwatch()
    assert card.stopwatch

    card.stopwatch.start()
    time.sleep(1)
    card.stopwatch.stop()
    assert card.stopwatch.total == 1

    card.stopwatch.set(hours=1)
    assert card.stopwatch.total == 3600

    card.stopwatch.set()
    assert card.stopwatch.total == 0

    card.stopwatch.delete()

def main_test():
    # Tests run in order of declaration
    tests = [
        reset_planka,
        create_users,
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
    