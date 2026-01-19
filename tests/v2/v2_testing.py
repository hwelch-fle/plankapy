import sys
from typing import Any
sys.path.append('../../src')

from datetime import datetime, timedelta
from plankapy.v2 import Planka
from httpx import Client, HTTPStatusError

URL = 'http://localhost:1337'
USER = 'demo'
PASS = 'demo'

import logging.config
import httpx

LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "http",
            "stream": "ext://sys.stderr"
        }
    },
    "formatters": {
        "http": {
            "format": "%(levelname)s [%(asctime)s] %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    'loggers': {
        'httpx': {
            'handlers': ['default'],
            'level': 'INFO',
        },
        'httpcore': {
            'handlers': ['default'],
            'level': 'INFO',
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

client = Client(base_url=URL)
planka = Planka(client)
planka.logon(USER, PASS)
prj = planka.projects[0]
try:
    #p1 = planka.create_project(
    #    name='New Project',
    #    type='private',
    #)

    new_user = (
        planka.create_user(
            email='new.user@test.com',
            password='vdkjsdfl23424',
            role='projectOwner',
            name='New User',
            username='nuser'
        ) 
        if not (existing := [u for u in planka.users if u.name == 'New User'])
        else existing.pop()
    )
    new_user.delete()
    #p1.delete()
    #p1.background_gradient = 'blue-steel'

except HTTPStatusError as e:
    print(e.request)
    print(e.request.url)
    print(e.request.headers)
    print(e.request.content)
    print(e)


project = planka.projects[0]

for board in project.boards:
    if 'My Board' in board.name:
        board.delete()

board = project.create_board(position=0, name='My Board')
board2 = project.create_board(position=0, name='My Board2')
board.project.background_gradient = 'purple-rose'
l1 = board.create_list(position=1, name='Active', type='active')
l2 = board.create_list(position=2, name='Closed', type='closed')
lbl = board.create_label(position=0, name='TODO', color='autumn-leafs')
lbl.add_to_board(board2)

for i in range(1, 11):
    card = l1.create_card(
        type='project', 
        position=i, 
        name=f'Card {i}', 
        description=f'The {i}th card in the {l1.name}', 
        dueDate=datetime.now() + timedelta(days=5)
    )
    card.add_label(lbl)

for card in l1.cards:
    card.add_members(planka.users, add_to_board=True, role='editor', can_comment=True)

print(len(lbl.gather_cards()))