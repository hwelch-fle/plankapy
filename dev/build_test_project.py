import sys
sys.path.append('../../src')
sys.path.append('src')

from random import choices

from plankapy.v2.models import Project, Board, User, List, Task, Comment, Label, Attachment, Card, CustomField
from plankapy.v2 import Planka

def create_test_project(planka: Planka, name: str = 'plankapy Test Project') -> Project:
    # Delete any existing test projects
    for tp in planka.projects[{'name': name}]:
        for board in tp.boards:
            board.delete()
        tp.delete()
    return planka.create_project(name=name, type='shared')

def create_test_users(planka: Planka, *users: str, default_password: str='plankapy999'):
    # Delete any existing test users:
    for user in planka.users[{'name': lambda n: n in users}]:
        user.delete()
    return [
        planka.create_user(
            email=f'{name}@test.com', 
            name=name, 
            password=default_password,
            username=name,
            role='boardUser',
        )
        for name in users
    ]

def create_test_boards(project: Project, *boards: str) -> list[Board]:
    return [
        project.create_board(name=board)
        for board in boards
    ]

def create_test_labels(boards: list[Board], *labels: str) -> list[Label]:
    return [
        b.create_label(name=l, color='random')
        for b in boards
        for l in labels
    ]

def create_test_lists(boards: list[Board], *lists: str) -> list[List]:
    return [
        b.create_list(name=l, color='random')
        for b in boards
        for l in lists
    ]

def create_test_cards(lists: list[List], *cards: str) -> list[Card]:
    return [
        l.create_card(name=c)
        for l in lists
        for c in cards
    ]

def create_test_attachments(cards: list[Card], *attachments: str) -> list[Attachment]:
    return [
        c.add_attachment(a, cover=True, download_url=True)
        for c in cards
        for a in attachments
    ]

def create_test_fields(cards: list[Card], *fields: dict[str, list[str]]) -> list[CustomField]:
    return [
        cf
        for c in cards
        for cfg in fields
        for k, v in cfg.items()
        for cf in c.add_card_fields(*v, group=k).custom_fields
    ]

def create_test_tasks(cards: list[Card], *tasks: dict[str, list[str]]) -> list[Task]:
    return [
        tl.add_task(v)
        for c in cards
        for tskl in tasks
        for tl_name, tl_tasks in tskl.items()
        if (tl := c.create_task_list(name=tl_name))
        for v in tl_tasks
    ]

def create_test_comments(users: list[User], cards: list[Card], *comments: str) -> list[Comment]: ...

def main():
    test_project_name = 'plankapy Test Project'
    test_users = [
        'plankapy1', 
        'plankapy2', 
        'plankapy3', 
        'plankapy4',
    ]
    test_boards = [
        'board 1',
        'board 2',
        'board 3',
    ]
    test_lists = [
        'todo',
        'doing',
        'done',
    ]
    test_labels = [
        'label 1',
        'label 2',
        'label 3',
    ]
    test_fields = [
        {'group 1': ['f1', 'f2']},
        {'group 2': ['f1', 'f2']},
    ]
    test_cards = [f'Card {i}' for i in range(10)]
    test_attachments = ['https://random-d.uk/api/randomimg']
    test_tasks = [
        {'tl1': ['t1', 't2']},
        {'tl2': ['t1', 't2']},
    ]
    test_comments = [
        'hello world',
        'foo',
        'bar',
        'baz',
    ]

    # Connect to an instance at 1137 as default admin
    planka = Planka('http://localhost:1337')
    planka.login(username='demo', password='demo')

    project = create_test_project(planka, test_project_name)
    users = create_test_users(planka, *test_users)
    boards = create_test_boards(project, *test_boards)
    labels = create_test_labels(boards, *test_labels)
    lists = create_test_lists(boards, *test_lists)
    cards = create_test_cards(lists, *test_cards)
    attach = create_test_attachments(choices(cards, k=10), *test_attachments)
    fields = create_test_fields(cards, *test_fields)
    tasks = create_test_tasks(cards, *test_tasks)
    #comments = create_test_comments(users, cards, *test_comments)

if __name__ == '__main__':
    main()