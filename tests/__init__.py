import sys
sys.path.append('../src')

import plankapy as ppy

if __name__ == '__main__':
    auth = ppy.PasswordAuth(username_or_email='demo', password='demo')
    planka = ppy.Planka('http://localhost:3000', auth=auth)
    