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

import httpx

class _BaseHandler(Protocol):
    """Protocol for implementing HTTP/s request handlers"""
    
    def __init__(self, base_url: str, *,
                 endpoint: Optional[str]=None, 
                 headers: Optional[dict[str, str]]=None) -> None: ...
    @property
    def endpoint(self) -> Optional[str]: ...
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


class SyncHttpxHandler(_BaseHandler): 
    """Handle all requests using HTTPX"""
    def __init__(self, base_url: str, *,
                 endpoint: Optional[str]=None, 
                 headers: Optional[dict[str, str]]=None) -> None:
        self.base_url = base_url
        self.headers = headers
        self._endpoint = endpoint
        self._client = httpx.Client

        # Auth is created seperately and passed to handler
        # Auth context adds cookies and token refreshing
        self._auth: httpx.Auth | None = None

    @property
    def auth(self) -> httpx.Auth:
        if self._auth is None:
            raise AuthError(f'No authentication provided for {self.base_url}')
        return self._auth

    @auth.setter
    def auth(self, auth: httpx.Auth) -> None:
        self._auth = auth

    @property
    def client(self) -> httpx.Client:
        return self._client(headers=self.headers, auth=self.auth)

    @property
    def endpoint(self) -> str:
        return urljoin(self.base_url, self._endpoint)
    
    @endpoint.setter
    def endpoint(self, value: str) -> None:
        self._endpoint = value

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.endpoint} >'
    
    def __str__(self) -> str:
        return self.endpoint

    def get(self) -> httpx.Response:
        with self._client() as client:
            return client.get(self.endpoint)

    def _get_file(self, url: str) -> bytes:
        with self._client() as client:
            return b''.join(client.get(url).iter_bytes())

    def post(self, data: dict) -> httpx.Response:
        with self.client as client:
            return client.post(self.endpoint, data=data)

    def _post_file(self, file_path: Path | str, file_name: str) -> httpx.Response:
        with self.client as client:
            client.headers['Connection'] = 'keep-alive'
            client.headers['Accept'] = '*/*'
            client.headers['Accept-Encoding'] = 'gzip, defalte, br'
            
            # Get file data and MIME type
            # Default to binary if MIME type is not found
            mime_type = guess_type(file_name)[0] or 'application/octet-stream' 

            # Handle string situations
            if isinstance(file_path, str):

                # Cast local path to Path
                if not file_path.startswith('http'):
                    file_path = Path(file_path)

                # Use _get_file to stream webfiles
                else:
                    with self.client as client:
                        return client.post(
                            self.endpoint, files={
                                'file': (file_name, self._get_file(file_path), mime_type)
                                }
                            )
            
            # At this point all remaining paths are Path objects
            with self.client as client:
                return client.post(
                    self.endpoint, files={
                        'file': (file_name, file_path.read_bytes(), mime_type)
                        }
                    )

    def put(self, data: dict) -> httpx.Response:
        with self.client as client:
            return client.put(self.endpoint, data=data)

    def patch(self, data: dict) -> httpx.Response:
        with self.client as client:
            return client.patch(self.endpoint, data=data)
    
    def delete(self) -> httpx.Response:
        with self.client as client:
            return client.delete(self.endpoint)

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

class AuthError(Exception): ...

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

class httpxPasswordAuth(httpx.Auth):
    """Password Authentication implementaion for use with the httpx Handlers
    
    Note:
        As long as the username and password is valid, expired tokens will be renewed
    
    Warning:
        This method will send your username and password in the headers as plaintext!
        If this is unacceptable (accessing over a network), make sure you are accessing
        the instance using SSL! For local management and 
    """
    def __init__(self, username: str, password: str) -> None:
        self.credentials = {'emailOrUsername': username, 'password': password}

        # Set by _get_token
        self.token = None
        self.cookies = httpx.Cookies()

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        # Set cookies/token if token is None
        if self.token is None:
            self.token, self.cookies = self._get_token(url=httpx.URL(request.url.host))

        # Use client context to pass cookies and auth header to request
        with httpx.Client(cookies=self.cookies, headers={'Authorization': f'Bearer {self.token}'}):
            response = yield request

        # Handle expired token/cookies
        if response.status_code == 401:
            self.token = None
            self.cookies = httpx.Cookies()
            self.auth_flow(request)

    def _get_token(self, url: httpx.URL) -> tuple[str, httpx.Cookies]:
        with httpx.Client(cookies=self.cookies) as client:
            response = client.post(url, data=self.credentials, params={'withHttpOnlyToken': True})

        # Call raise_for_status on response to allow HTTP Errors to bubble up
        self.cookies.update(response.raise_for_status().cookies)
        return response.json()['item']

class httpxTokenAuth(httpx.Auth):
    """Token Authentication implementaion for use with the httpx Handlers
    
    Note:
        Token based authentication cannot automatically renew when the token expires!
    """
    def __init__(self, token: str) -> None:
        self.token = token
        self.cookies = httpx.Cookies()

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        # Use client context to pass cookies and auth header to request
        with httpx.Client(cookies=self.cookies, headers={'Authorization': f'Bearer {self.token}'}):
            response = yield request
            response.raise_for_status()

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