# Collection of sample scripts for plankapy.v2
from datetime import datetime, timedelta, timezone
import sys
sys.path.append('../src')
sys.path.append('src')

from plankapy.v2 import Planka
from plankapy.v2.models import *
from plankapy.v2.models import UserRole
from httpx import Client, HTTPStatusError
from random import choice

# Initialize a Planka instance using Demo user
client = Client(base_url='http://localhost:1337')
planka = Planka(client)
planka.logon('demo', 'demo')

def reset_planka():
    for project in planka.projects:
        for board in project.boards:
            board.delete()
        project.delete()
    for user in planka.users:
        if user != planka.me:
            user.delete()

def create_projects(*prj_names: str):
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
    
    PROJECTS = ['Project 1', 'Project 2', 'Project 3']
    USERS = ['user1', 'user2', 'user3']
    LISTS = ['To Do', 'Doing', 'Review', 'Done']
    LABELS = ['Overdue', 'On Schedule']
    BOARDS = ['Fontend', 'Backend']
    CARDS = ['Task 1', 'Task 2', 'Task 3', 'Task 4']

    reset_planka()

    # Build a Framework
    create_projects(*PROJECTS)
    for project in planka.projects:
        create_boards(project, *BOARDS)
        for board in project.boards:
            create_lists(board, *LISTS)
            create_labels(board, *LABELS)
            create_cards(board.active_lists[0], *CARDS)
    
    # Just kinda move stuff around randomly
    while True:
        try:
            for project in planka.projects:
                project.background_gradient = choice(BackgroundGradients)
                for board in project.boards:
                    overdue = [l for l in board.labels if l.name == 'Overdue'].pop()
                    on_schedule = [l for l in board.labels if l.name == 'On Schedule'].pop()

                    # Move 5 cards per board
                    for _ in range(5):
                        card = choice(board.cards)
                        to_list = choice(board.active_lists)
                        print(f'{project.name}->{board.name}: Moving Card {card.name} from List {card.list.name} To List {to_list.name}')
                        card.move(to_list, position='bottom')

                        # Pick a Due Date then do datemath to warn user of overdue cards and set labels
                        card.due_date = datetime.now() + timedelta(days=choice([-3, -2, -1, 0, 1, 2, 3]))
                        due_in_days = (card.due_date.replace(tzinfo=timezone.utc) - datetime.now().replace(tzinfo=timezone.utc)).days
                        if card.due_date.timestamp() > datetime.now().timestamp():
                            print(f'Card: {card.name} is due in {due_in_days} days')
                            card.remove_label(overdue)
                            card.add_label(on_schedule)
                        else:
                            print(f'WARNING Card: {card.name} is overdue by {due_in_days} days!')
                            card.remove_label(on_schedule)
                            card.add_label(overdue)
        except HTTPStatusError as e:
            print(e.response.json())