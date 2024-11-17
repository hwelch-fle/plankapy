from urllib.request import Request, urlopen
from urllib.parse import urljoin

from typing import Optional, TypeAlias, Generator
import json

from contextlib import contextmanager

JSONResponse: TypeAlias = dict[str, str]

def encode_data(data: dict, encoding: str='utf-8') -> bytes:
    return json.dumps(data).encode(encoding)

def decode_data(data: bytes, encoding: str='utf-8') -> dict:
    return json.loads(data.decode(encoding))

class BaseHandler:
    def __init__(self, base_url: str, *,
                 endpoint: Optional[str]=None, 
                 headers: Optional[dict[str, str]]=None) -> None:
        self._base_url = base_url
        self._endpoint = endpoint
        self._headers = headers if headers else {}
    
    @property
    def endpoint(self):
        return urljoin(self._base_url, self._endpoint)
    
    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value
        
    @property
    def headers(self):
        return self._headers
    
    @headers.setter
    def headers(self, value):
        self._headers = value
        
    @property
    def base_url(self):
        return self._base_url
    
    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.endpoint} >'
    
    def __str__(self):
        return f'{self.endpoint}'
    
    def get(self) -> bytes:
        req = Request(self.endpoint, 
                      headers=self.headers, 
                      method='GET')
        with urlopen(req) as response:
            return response.read()
    
    def post(self, data: dict) -> bytes:
        req = Request(self.endpoint, 
                      headers=self.headers, 
                      method='POST', 
                      data=encode_data(data))
        with urlopen(req) as response:
            return response.read()
    
    def put(self, data: dict) -> bytes:
        req = Request(
            self.endpoint, 
            headers=self.headers, 
            method='PUT', 
            data=encode_data(data))
        with urlopen(req) as response:
            return response.read()
    
    def patch(self, data: dict) -> bytes:
        req = Request(self.endpoint, 
                      headers=self.headers, 
                      method='PATCH', 
                      data=encode_data(data))
        with urlopen(req) as response:
            return response.read()
    
    def delete(self) -> bytes:
        req = Request(self.endpoint, 
                      headers=self.headers, 
                      method='DELETE')
        with urlopen(req) as response:
            return response.read()
        
    @contextmanager
    def endpoint_as(self, endpoint: Optional[str]=None) -> Generator['BaseHandler', None, None]:
        _endpoint = self.endpoint
        self.endpoint = endpoint
        try:
            yield self
        finally:
            self.endpoint = _endpoint
    
class JSONHandler(BaseHandler):    
    def get(self) -> JSONResponse:
        return decode_data(super().get())

    def post(self, data: dict) -> JSONResponse:
        return decode_data(super().post(data))
    
    def put(self, data: dict) -> JSONResponse:
        return decode_data(super().put(data))
    
    def patch(self, data: dict) -> JSONResponse:
        return decode_data(super().patch(data))
    
    def delete(self) -> JSONResponse:
        return decode_data(super().delete())

def create_session(url: str, *,
                   emailOrUsername: Optional[str]=None, 
                   password: Optional[str], 
                   token: Optional[str]=None) -> JSONHandler:
    headers: dict[str, str] = {}
    headers['Content-Type'] = 'application/json'
    if not token:
        data = {
            'emailOrUsername': emailOrUsername,
            'password': password
        }
        with JSONHandler(url, headers=headers).endpoint_as('api/access-tokens') as handler:
            response = handler.post(data)
            token = response['item']
    headers['Authorization'] = f'Bearer {token}'
    return JSONHandler(url, headers=headers)