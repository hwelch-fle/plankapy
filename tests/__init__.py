import sys
sys.path.append('../src')

import plankapy as ppy

import model_tests
import interface_tests

if __name__ == '__main__':
    auth = ppy.PasswordAuth(username_or_email='demo', password='demo')
    planka = ppy.Planka('http://localhost:3000', auth=auth)
    

    assert model_tests.test_base_model()
    assert interface_tests.test_interfaces(planka)

    print("All tests passed!")