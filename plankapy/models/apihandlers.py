from urllib.request import Request, urlopen
from urllib.parse import urljoin
from http.client import HTTPResponse

from typing import Optional, TypeAlias
import json

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

    
class ProjectHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/projects', headers=headers)
        
class BoardHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/boards', headers=headers)
        
class CardHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/cards', headers=headers)

class ListHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/lists', headers=headers)

class AttachmentHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/attachments', headers=headers)

class TaskHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/tasks', headers=headers) 

class NotificationHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/notifications', headers=headers)

class UserHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/users', headers=headers)

class AttachmentHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/attachments', headers=headers)
        
class CommentActionHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/comment-actions', headers=headers)
        
class AccessHandler(JSONHandler):
    def __init__(self, base_url: str, *,
                 headers: Optional[dict[str, str]]=None) -> None:
        super().__init__(base_url, endpoint='api/access-tokens', headers=headers)