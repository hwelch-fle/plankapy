import sys
sys.path.append('../src')

from plankapy import PasswordAuth, Planka

auth = PasswordAuth('demo', 'demo')
planka = Planka('http://localhost:3000', auth)