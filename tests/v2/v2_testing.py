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
