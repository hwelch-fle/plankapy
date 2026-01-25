import sys
from typing import Any, Protocol

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

from datetime import datetime, timedelta
from functools import wraps

class HasDueDate(Protocol):
    @property
    def due_date(self) -> datetime: ...

def due_in(hours: float=0, days: float=0, weeks: float=0):
    def _inner(m: HasDueDate):
        if not m.due_date:
            return False
        by = timedelta(days=days, hours=hours, weeks=weeks)
        return (m.due_date - by) <= datetime.now()
    return _inner

cards = prj.boards[0].cards
filtered = cards[due_in(days=5)]

from random import choice
from time import sleep
# while True:
#     card = choice(cards)
#     card.add_attachment(r"https://random-d.uk/api/randomimg?t=1769031485189", cover=True, download_url=True)
#     sleep(1)
#     for attach in card.attachments:
#         attach.delete()
#
#while True:
#    p = choice(planka.projects)
#    new = p.update_background_image('https://random-d.uk/api/randomimg?t=1769031485189')
#    [bg.delete() for bg in p.background_images if bg != new]
#    sleep(5)