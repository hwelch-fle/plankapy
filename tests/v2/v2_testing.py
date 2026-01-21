import sys
sys.path.append('../../src')

from plankapy.v2 import Planka
from httpx import Client

URL = 'http://localhost:1337'
USER = 'demo'
PASS = 'demo'

client = Client(base_url=URL)
planka = Planka(client)
planka.logon(USER, PASS)
prj = planka.projects[0]

cards = prj.boards[0].cards
from random import choice
from time import sleep
while True:
    card = choice(cards)
    card.add_attachment(r"https://random-d.uk/api/randomimg?t=1769031485189", cover=True, download_url=True)
    sleep(1)
    for attach in card.attachments:
        attach.delete()