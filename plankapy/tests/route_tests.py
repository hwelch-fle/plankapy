import sys
sys.path.append('..')

from plankapy.utils.routes import *
from plankapy.utils.routes import ROUTES
import plankapy.utils.routes as routes

from plankapy.utils.handlers import create_session

# Test using the default Planka demo credentials
planka = create_session('http://localhost:3000', emailOrUsername='demo', password='demo')

def validate_routes_implemented():
    try:
        not_implemented = set(ROUTES.keys()) - set(dir(routes))
        assert not not_implemented
        return True
    except AssertionError:
        print(f'Routes not implemented: {not_implemented}')
        return False

def test_routes():
    for route in ROUTES:
        route = getattr(routes, route)
        try:
            assert route(planka)
        except AssertionError:
            print(f'{route} failed')
            return False
        
def run_tests():
    assert validate_routes_implemented()
    assert test_routes()
    print('All tests passed')