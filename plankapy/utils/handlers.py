from urllib.request import Request, urlopen
from urllib.parse import urljoin

from typing import Optional, TypeAlias, Generator
import json

from contextlib import contextmanager

JSONResponse: TypeAlias = dict[str, str]

def encode_data(data: dict, encoding: str='utf-8') -> bytes:
    return json.dumps(data).encode(encoding)

def decode_data(data: bytes, encoding: str='utf-8') -> dict:
    try:
        return json.loads(data.decode(encoding))
    except json.JSONDecodeError:
        return {'body': data.decode(encoding)}

class BaseHandler:
    def __init__(self, base_url: str, *,
                 endpoint: Optional[str]=None, 
                 headers: Optional[dict[str, str]]=None) -> None:
        self._base_url = base_url
        self._endpoint = endpoint
        self._headers = headers if headers else {}
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.endpoint} >'

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


class BaseAuth:
    endpoint = None
    def __repr__(self) -> str:
        return f"<{self.__class__.__name___}: "
    def authenticate(self) -> str:
        raise NotImplementedError(f"Authentication not implemeted by {self.__class__.__name__}")

class PasswordAuth(BaseAuth):
    endpoint = 'api/access-tokens'

    def __init__(self, username_or_email: str, password: str) -> None:
        self.token = None
        self.data = {
            'emailOrUsername': username_or_email,
            'password': password
        }

    def authenticate(self, url: str) -> str:
        with JSONHandler(url, headers={'Content-Type': 'application/json'}).endpoint_as(self.endpoint) as handler:
            self.token = handler.post(self.data)['item']
        return f"Bearer {self.token}"

class TokenAuth(BaseAuth):
    endpoint = 'api/access-tokens'

    def __init__(self, token: str) -> None:
        self.token = token

    def authenticate(self, url: str) -> str:
        return f"Bearer {self.token}"

# TODO: Implement SSO auth for httpOnlyToken auth
# https://github.com/hwelch-fle/plankapy/pull/11/commits/72b8d06208dc961537ef2bcd8d65c11879b8d6b9#
class HTTPOnlyAuth(BaseAuth): ...

