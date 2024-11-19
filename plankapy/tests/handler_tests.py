import os
import re
from random import randint

import sys
sys.path.append('..')

from plankapy.utils.handlers import BaseHandler
from tests.fake_planka import ROUTES

def get_rest_endpoints(request_type: str) -> dict:
    return {
        route.split(' ')[-1]: name 
        for route, name in ROUTES.items()
        if route.startswith(request_type)
    }

def rest_tests() -> bool:
    PASS = True
    if os.name == 'nt':
        os.system(f'start /b python fake_planka.py &')
    else:
        os.system(f'python fake_planka.py &')
    
    id_replacement = re.compile(r':\w+')
    handler = BaseHandler('http//127.0.0.1:1338')
    
    for request_type in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']:
        print(f'Running {request_type} tests')
        endpoints = get_rest_endpoints(request_type)
        for endpoint, value in endpoints.items():
            endpoint = id_replacement.sub(str(randint(1, 100)), endpoint)
            handler.endpoint = endpoint
            try:
                match request_type:
                    case 'POST':
                        response = handler.post(data={'payload': value})
                    case 'GET':
                        response = handler.get()
                    case 'PUT':
                        response = handler.put(data={'payload': value})
                    case 'PATCH':
                        response = handler.patch(data={'payload': value})
                    case 'DELETE':
                        response = handler.delete() 
                assert response.status in (200, 201)
                
            except Exception as e:
                print(f'{endpoint} failed: {e}')
                PASS = False
                continue
            print(f'{endpoint}: called {value}') 
    return PASS
        
if __name__ == '__main__':
    assert rest_tests()