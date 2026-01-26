from datetime import datetime, timedelta, timezone
import sys
sys.path.append('../src')
sys.path.append('src')

from plankapy.v2 import Planka
from plankapy.v2.models import *
from plankapy.v2.models import UserRole
from httpx import Client, HTTPStatusError
from random import choice, shuffle

def reset_planka(planka: Planka):
    for project in planka.projects:
        for board in project.boards:
            board.delete()
        project.delete()
    for user in planka.users:
        if user != planka.me:
            user.delete()

def create_projects(planka: Planka, *prj_names: str):
    return {
        name: planka.create_project(name=name, type='shared')
        for name in prj_names
    }
    
def create_boards(prj: Project, *board_names: str):
    return {
        name: prj.create_board(name=name, position=pos*16384) 
        for pos, name in enumerate(board_names, start=1)
    }

def create_lists(brd: Board, *list_names: str):
    return {
        name: brd.create_list(name=name, position=pos*16384, type='active') 
        for pos, name in enumerate(list_names, start=1)
    }

def create_users(*usernames: str, role: UserRole='admin'):
    return {
        name: planka.create_user(name=name, email=name+'@company.org', role=role, password=name+'12345') 
        for name in usernames
    }

def create_cards(list: List, *card_names: str):
    return {
        name: list.create_card(type='project', position=pos*16384, name=name)
        for pos, name in enumerate(card_names, start=1)
    }

def create_labels(board: Board, *label_names: str):
    return {
        name: board.create_label(name=name, position=pos*16384, color=choice(LabelColors))
        for pos, name in enumerate(label_names, start=1)
    }

if __name__ == '__main__':
    
    # Initialize a Planka instance using Demo user
    client = Client(base_url='http://localhost:1337')
    planka = Planka(client)
    planka.logon(username='demo', password='demo')
    
    # Objects to create
    projects = ['Project 1', 'Project 2', 'Project 3']
    users = ['user1', 'user2', 'user3']
    lists = ['To Do', 'Doing', 'Review', 'Done']
    labels = ['Overdue', 'On Schedule']
    boards = ['Fontend', 'Backend']
    cards = [f'Task {i}'for i in range(1,11)]
    base_fields = {'Group 1': ['field a', 'field b'], 'Group 2': ['field c', 'field d']}

    reset_planka(planka)

    # Build a Framework
    print('Creating Projects')
    create_projects(planka, *projects)
    print('Creating Users')
    create_users(*users)
    for project in planka.projects:
        print(f'Creating Boards in {project.name}')
        create_boards(project, *boards)
        for bcfg_name, bcfg_fields in base_fields.items():
            bcfg = project.create_base_custom_field_group(name=bcfg_name)
            for pos, field in enumerate(bcfg_fields, start=1):
                bcfg.create_field(name=field, position=16636*pos, showOnFrontOfCard=True)
        for board in project.boards:
            print(f'\tCreating Lists in {board.name}')
            create_lists(board, *lists)
            print(f'\tCreating Labels in {board.name}')
            create_labels(board, *labels)
            print(f'\tCreating Cards in {board.name}')
            create_cards(board.active_lists[0], *cards)
            print(f'\tAdding Members to {board.name}')
            board.add_members(planka.users, role='editor')
    
    # Just kinda move stuff around randomly
    while True:
        try:
            for project in planka.projects:
                project.background_gradient = choice(BackgroundGradients)
                for board in project.boards:
                    overdue = [l for l in board.labels if l.name == 'Overdue'].pop()
                    on_schedule = [l for l in board.labels if l.name == 'On Schedule'].pop()

                    cards = board.cards
                    shuffle(cards)
                    for card in cards:
                        user = choice(board.users)
                        to_list = choice(board.active_lists)
                        print(f'{project.name}->{board.name}: Moving Card {card.name} from List {card.list.name} To List {to_list.name}')
                        card.move(to_list, position='bottom')
                        for member in card.members:
                            card.remove_member(member)
                        user.add_to_card(card)
                        
                        # Pick a Due Date then do datemath to warn user of overdue cards and set labels
                        card.due_date = datetime.now() + timedelta(days=choice([-3, -2, -1, 0, 1, 2, 3]))
                        due_in = card.due_date - datetime.now().replace(tzinfo=card.due_date.tzinfo)
                        if card.due_date.timestamp() > datetime.now(tz=timezone.utc).timestamp():
                            print(f'Card: {card.name} is due in {due_in.days} days')
                            card.remove_label(overdue)
                            card.add_label(on_schedule)
                        else:
                            print(f'WARNING Card: {card.name} is overdue by {due_in.days} days!')
                            card.remove_label(on_schedule)
                            card.add_label(overdue)
        except HTTPStatusError as e:
            print(e.response.json())