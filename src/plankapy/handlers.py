from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urljoin

from pathlib import Path
from uuid import uuid4
from mimetypes import guess_type
from io import BytesIO
from . import __version__ # Used for User-Agent header

from typing import (
    Optional, 
    TypeAlias, 
    Generator, 
    Self, 
    Protocol, 
    Any,
    )
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
        raise NotImplementedError("Decoding must be implemented by subclass")

    def _open(self, request: Request) -> bytes:
        try:
            with urlopen(request) as response:
                return response.read()
        except HTTPError as error:
            error.add_note(f"endpoint: {request.full_url}\n"
                           f"headers: {request.headers}\n"
                           f"data: {request.data}\n"
                           )
            raise error
                
    def _get_file(self, url: str) -> bytes:
        return self._open(Request(
                url, 
                method='GET',
                headers={'User-Agent': f'Plankapy / {__version__}'}
            )
        )

    def get(self) -> bytes:
        return self._open(Request(
                self.endpoint,         
                headers=self.headers, 
                method='GET'
            )
        )
    
    def _post_file(self, file_path: Path, file_name: str) -> bytes:
        """Multipart formatting is hard"""
        # Set headers for file upload
        headers = self.headers.copy() # Make a copy of the headers
        
        headers['Connection'] = 'keep-alive'
        headers['Accept'] = '*/*'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        
        # Get file data and MIME type
        # Default to binary if MIME type is not found
        mime_type = guess_type(file_name)[0] or 'application/octet-stream' 
        
        # Generate boundary for multipart form data
        boundary_uuid = uuid4().hex
        boundary = f'--{boundary_uuid}'
        
        # Add multipart form data headers with boundary
        headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        
        # Get payload parts
        payload_disposition = f'Content-Disposition: form-data; name="file"; filename="{file_name}"'.encode('utf-8')
        payload_content_type = f"Content-Type: {mime_type}\r\n\r\n".encode('utf-8')
        if str(file_path).startswith('http'):
            # Pop the raw path from the Path object so we don't need to reformat the URL
            file_data = BytesIO(self._get_file(file_path._raw_paths.pop())).read()
        else:
            file_data = file_path.read_bytes()
        
        # Construct payload
        payload = BytesIO()
        payload.write(f'--{boundary}'.encode('utf-8'))    # Boundary
        payload.write(b'\r\n')                            # New line
        payload.write(payload_disposition)                # Content-Disposition
        payload.write(b'\r\n')                            # New line
        payload.write(payload_content_type)               # Content-Type
        payload.write(file_data)                          # File data
        payload.write(b'\r\n')                            # New line
        payload.write(f'--{boundary}--'.encode('utf-8'))  # End 
        payload.write(b'\r\n')                            # New line
        payload = payload.getvalue()                      # Get payload as bytes
        
        # Add content length to headers
        headers['Content-Length'] = len(payload)
        
        return self._open(Request(
            self.endpoint, 
            headers=headers, 
            method='POST', 
            data=payload
        ))
    
    def post(self, data: dict) -> bytes:

        # Pass file uploads to _post_file method
        if '_file' in data:
            file_path = Path(data.pop('_file'))
            file_name = data.pop('_file_name', file_path.name)
            return self._post_file(file_path, file_name)
              
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
        return f"< {self.__class__.__name__}: {self.endpoint} >"
    
    def authenticate(self) -> str: ...

class PasswordAuth(BaseAuth):
    """Authentication using a username or email and password
    
    Attributes:
        endpoint (str): The token to use for authentication (default: 'api/access-tokens')
    """
    
    endpoint = 'api/access-tokens'

    def __init__(self, username_or_email: str, password: str) -> None:
        """Initialize a PasswordAuth instance with a username or email and password
        
        Args:
            username_or_email (str): The username or email to use for authentication
            password (str): The password to use for authentication
            
        Example:
            ```python
            >>> auth = PasswordAuth('username', 'password')
            >>> auth.authenticate('http://planka.instance')
            {'Authorization' : 'Bearer <token>'}
            ```    
        """
        self.token = None
        self.credentials = {
            'emailOrUsername': username_or_email,
            'password': password
        }

    def authenticate(self, url: str) -> dict[str, str]:
        """Implementation of the authenticate method
        
        Args:
            url (str): The base url of the Planka instance
            
        Returns:
            Headers with the token in the `Authorization` key
        """
        self.token = JSONHandler(url, endpoint=self.endpoint).post(self.credentials)['item']
        return {"Authorization": f"Bearer {self.token}"}

class TokenAuth(BaseAuth):
    """Authentication using a pre-supplied token
    
    Attributes:
        endpoint (str): The token to use for authentication (default: 'api/access-tokens')
        
    Example:
        ```python
        >>> auth = TokenAuth('<token>')
        >>> auth.authenticate()
        {'Authorization : 'Bearer <token>'}
        ```
    """
    endpoint = 'api/access-tokens'

    def __init__(self, token: str) -> None:
        """Initialize a TokenAuth instance with a token
        
        Args:
            token (str): The token to use for authentication
        """
        self.token = token

    def authenticate(self, url: str=None) -> dict[str, str]:
        """Implementation of the authenticate method
        
        Args:
            url (str): Not used, but required by the protocol
        
        Returns:
           Headers with the token in the `Authorization` key
        """
        return {"Authorization": f"Bearer {self.token}"}

# TODO: Implement SSO auth with httpOnlyToken
# https://github.com/hwelch-fle/plankapy/pull/11/commits/72b8d06208dc961537ef2bcd8d65c11879b8d6b9#
class HTTPOnlyAuth(PasswordAuth): 
    """Authentication using an httpOnlyToken
    
    Note:
        This class requires the `requests` library
    """

    def authenticate(self, url: str) -> dict[str, str]:
        """"""
        try:
            import requests
        except (ModuleNotFoundError, ImportError) as e:
            e.add_note("`requests` library required for cookie base authentication\n"
                       "If you need this functionality, install it with `pip install requests`\n"
                       "otherwise, use one of the other Authentication protocols")
            raise e
        response = requests.post(urljoin(url, self.endpoint, '?withHttpOnlyToken=true'), json=self.credentials)
        headers = {}
        headers['Authorization'] = f"Bearer {response.json()['item']}"
        headers['Cookie'] = f"httpOnlyToken={response.cookies.get('httpOnlyToken', default='')}"
        return headers