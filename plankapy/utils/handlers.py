from dataclasses import dataclass
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from http.client import HTTPResponse
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
        return urljoin(self.base_url, self._endpoint)
    
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
    
    def get(self) -> HTTPResponse:
        req = Request(self.endpoint, 
                      headers=self.headers, 
                      method='GET')
        with urlopen(req) as response:
            return response
    
    def post(self, data: dict) -> HTTPResponse:
        req = Request(self.endpoint, 
                      headers=self.headers, 
                      method='POST', 
                      data=encode_data(data))
        with urlopen(req) as response:
            return response
    
    def put(self, data: dict) -> HTTPResponse:
        req = Request(
            self.endpoint, 
            headers=self.headers, 
            method='PUT', 
            data=encode_data(data))
        with urlopen(req) as response:
            return response
    
    def patch(self, data: dict) -> HTTPResponse:
        req = Request(self.endpoint, 
                      headers=self.headers, 
                      method='PATCH', 
                      data=encode_data(data))
        with urlopen(req) as response:
            return response
    
    def delete(self) -> HTTPResponse:
        req = Request(self.endpoint, 
                      headers=self.headers, 
                      method='DELETE')
        with urlopen(req) as response:
            return response
        
    @contextmanager
    def endpoint_as(self, endpoint: Optional[str]=None) -> Generator['BaseHandler', None, None]:
        _endpoint = self.endpoint
        self.endpoint = endpoint
        yield self
        self.endpoint = _endpoint
    
class JSONHandler(BaseHandler):    
    def get(self) -> JSONResponse:
        return decode_data(super().get().read())

    def post(self, data: dict) -> JSONResponse:
        return decode_data(super().post(data).read())
    
    def put(self, data: dict) -> JSONResponse:
        return decode_data(super().put(data).read())
    
    def patch(self, data: dict) -> JSONResponse:
        return decode_data(super().patch(data).read())
    
    def delete(self) -> JSONResponse:
        return decode_data(super().delete().read())

@dataclass
class Session:
    url: str
    headers: Optional[dict[str, str]]=None

@contextmanager
def endpoint_as(handler: BaseHandler, endpoint: str):
    _endpoint = handler.endpoint
    handler.endpoint = endpoint
    yield handler
    handler.endpoint = _endpoint

def create_session(url: str, username_or_email: str, password: str, token: Optional[str]=None) -> Session:
    if token:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    else:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {username_or_email}:{password}'
        }
    return Session(url, headers)

class ProjectHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/projects', headers=session.headers)
        
class BoardHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/boards', headers=session.headers)
        
class CardHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/cards', headers=session.headers)

class ListHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/lists', headers=session.headers)

class AttachmentHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/attachments', headers=session.headers)

class TaskHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/tasks', headers=session.headers) 

class NotificationHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/notifications', headers=session.headers)

class UserHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/users', headers=session.headers)

class AttachmentHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/attachments', headers=session.headers)
        
class AccessHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/access-tokens', headers=session.headers)
        
class LabelHandler(JSONHandler):
    def __init__(self, session: Session) -> None:
        super().__init__(session.url, endpoint='api/labels', headers=session.headers)