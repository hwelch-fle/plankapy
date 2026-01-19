import sys
sys.path.append('../../src')

from datetime import datetime
from plankapy.v2 import Planka
from httpx import Client, HTTPStatusError

URL = 'http://localhost:1337'
USER = 'demo'
PASS = 'demo'

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
    print(new_user.name)
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
    if board.name == 'My Board':
        board.delete()

board = project.create_board(position=0, name='My Board')
board.project.background_gradient = 'purple-rose'
l1 = board.create_list(position=1, name='Active', type='active')
l2 = board.create_list(position=2, name='Closed', type='closed')

for i in range(1, 11):
    l1.create_card(
        type='project', 
        position=i, 
        name=f'Card {i}', 
        description=f'The {i}th card in the {l1.name}', 
        dueDate=datetime.now().isoformat()
    )
