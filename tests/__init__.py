import plankapy as pk

if __name__ == '__main__':
    auth = pk.PasswordAuth(username_or_email='demo', password='demo')
    planka = pk.Planka('http://localhost:3000', auth=auth)