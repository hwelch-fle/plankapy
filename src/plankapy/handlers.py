from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urljoin

from typing import Optional, TypeAlias, Generator, Self, Protocol, Any
import json

from contextlib import contextmanager

class _BaseHandler(Protocol):
    """Protocol for implementing HTTP/s request handlers"""
    
    def __init__(self, base_url: str, *,
                 endpoint: Optional[str]=None, 
                 headers: Optional[dict[str, str]]=None) -> None: ...
    @property
    def endpoint(self) -> str: ...
    @endpoint.setter
    def endpoint(self, value: str): ...
    def encode_data(self, data: dict, encoding: str='utf-8') -> bytes: ...
    def decode_data(self) -> Any: ...
    def get(self) -> Any: ...
    def post(self, data: dict) -> Any: ...
    def put(self, data: dict) -> Any: ...
    def patch(self, data: dict) -> Any: ...
    def delete(self) -> Any: ...
    @contextmanager
    def endpoint_as(self, endpoint: Optional[str]=None) -> Generator[Self, None, None]: ... 

class urllibHandler(_BaseHandler):
    """Base class for handling HTTP requests using urllib"""
    def __init__(self, base_url: str, *,
                 endpoint: Optional[str]=None, 
                 headers: Optional[dict[str, str]]=None) -> None:
        self.base_url = base_url
        self._endpoint = endpoint
        self.headers = headers if headers else {'Content-Type': 'application/json'}
    
    @property
    def endpoint(self) -> str:
        return urljoin(self.base_url, self._endpoint)
    
    @endpoint.setter
    def endpoint(self, value: str):
        self._endpoint = value

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.endpoint} >'
    
    def __str__(self):
        return self.endpoint
    
    def encode_data(self, data: dict, encoding: str='utf-8') -> bytes:
        return json.dumps(data).encode(encoding)

    def decode_data(self):
        raise NotImplementedError("Decoding must be implemeted by subclass")

    def _open(self, request: Request) -> bytes:
        try:
            with urlopen(request) as response:
                return response.read()
        except HTTPError as error:
            error.add_note(f"endpoint: {request.full_url}\n"
                           f"headers: {request.headers}\n"
                           f"data: {request.data}")
            raise error
                

    def get(self) -> bytes:
        return self._open(Request(
                self.endpoint,         
                headers=self.headers, 
                method='GET'
            )
        )
    
    def post(self, data: dict) -> bytes:
        return self._open(Request(
                self.endpoint, 
                headers=self.headers, 
                method='POST', 
                data=self.encode_data(data)
            )
        )
    
    def put(self, data: dict) -> bytes:
        return self._open(Request(
                self.endpoint, 
                headers=self.headers, 
                method='PUT', 
                data=self.encode_data(data)
            )
        )
    
    def patch(self, data: dict) -> bytes:
        return self._open(Request(
                self.endpoint, 
                headers=self.headers, 
                method='PATCH', 
                data=self.encode_data(data)
            )
        )
    
    def delete(self) -> bytes:
        return self._open(Request(
                self.endpoint, 
                headers=self.headers, 
                method='DELETE'
            )
        )
        
    @contextmanager
    def endpoint_as(self, endpoint: Optional[str]=None) -> Generator[Self, None, None]:
        _endpoint = self.endpoint
        self.endpoint = endpoint
        try:
            yield self
        finally:
            self.endpoint = _endpoint

class JSONHandler(urllibHandler):
    """Handler for JSON data (Uses urllib)"""
    JSONResponse: TypeAlias = dict[str, str]

    def decode_data(self, data: bytes, encoding: str='utf-8') -> dict:
        try:
            return json.loads(data.decode(encoding))
        except json.JSONDecodeError:
            return {'body': data.decode(encoding)}

    def get(self) -> JSONResponse:
        return self.decode_data(super().get())

    def post(self, data: dict) -> JSONResponse:
        return self.decode_data(super().post(data))
    
    def put(self, data: dict) -> JSONResponse:
        return self.decode_data(super().put(data))
    
    def patch(self, data: dict) -> JSONResponse:
        return self.decode_data(super().patch(data))
    
    def delete(self) -> JSONResponse:
        return self.decode_data(super().delete())

class BaseAuth(Protocol):
    endpoint = None
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.endpoint}"
    
    def authenticate(self) -> str:
        raise NotImplementedError

class PasswordAuth(BaseAuth):
    endpoint = 'api/access-tokens'

    def __init__(self, username_or_email: str, password: str) -> None:
        self.token = None
        self.credentials = {
            'emailOrUsername': username_or_email,
            'password': password
        }

    def authenticate(self, url: str) -> str:
        self.token = JSONHandler(url, endpoint=self.endpoint).post(self.credentials)['item']
        return f"Bearer {self.token}"

class TokenAuth(BaseAuth):
    endpoint = 'api/access-tokens'

    def __init__(self, token: str) -> None:
        self.token = token

    def authenticate(self, url: str=None) -> str:
        """URL not required for getting auth string with pre-supplied token"""
        return f"Bearer {self.token}"

# TODO: Implement SSO auth with httpOnlyToken
# https://github.com/hwelch-fle/plankapy/pull/11/commits/72b8d06208dc961537ef2bcd8d65c11879b8d6b9#
class HTTPOnlyAuth(BaseAuth): ...
