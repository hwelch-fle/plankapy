import sys
sys.path.append('../src')

import plankapy as ppy

import model_tests
import interface_tests

if __name__ == '__main__':
    auth = ppy.PasswordAuth(username_or_email='demo', password='demo')
    planka = ppy.Planka('http://localhost:3000', auth=auth)
    

    model_tests.test_base_model()
    model_tests.test_model_implementations()

    interface_tests.test_interfaces(planka)