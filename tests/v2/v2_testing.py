import sys
sys.path.append('../../src')

from plankapy.v2 import Planka
from httpx import Client

URL = 'http://localhost:1337'
USER = 'demo'
PASS = 'demo'
KEY = '3gBptWe7_THy8fN4qzrvcgu6u7w8yZquDeHwQNMDc'

client = Client(base_url=URL)
planka = Planka(client)

# Will log a warning if used
#planka.logon(username=USER, password=PASS)

planka.logon(api_key=KEY)
prj = planka.projects[0]

cards = prj.boards[0].cards
from random import choice
from time import sleep
# while True:
#     card = choice(cards)
#     card.add_attachment(r"https://random-d.uk/api/randomimg?t=1769031485189", cover=True, download_url=True)
#     sleep(1)
#     for attach in card.attachments:
#         attach.delete()
#
while True:
    p = choice(planka.projects)
    new = p.update_background_image('https://random-d.uk/api/randomimg?t=1769031485189')
    [bg.delete() for bg in p.background_images if bg != new]
    sleep(5)