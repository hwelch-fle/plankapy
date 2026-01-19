from __future__ import annotations
from functools import cached_property
from typing import Unpack
from warnings import warn

from httpx import Client
from .api import (
    PlankaEndpoints, 
    typ, # Response / Request typing
)
from .models import *

# Allow Users to set `PLANKA_LANG` environment variable with their language
# Default to en-US if not set
import os
DEFAULT_LANG = os.environ.get('PLANKA_LANG', 'en-US')
del os

class Planka:
    def __init__(self, client: Client, lang: str=DEFAULT_LANG) -> None:
        self.client = client
        self.endpoints = PlankaEndpoints(client)
        if lang not in Languages:
            warn(f'{lang} is not currently supported by Planka, using {DEFAULT_LANG}', EncodingWarning)
            lang = DEFAULT_LANG
        self.lang = lang
        
    def logon(self, username: str, password: str, *, token: str='', accept_terms: bool=False):
        """Authenticate with the planka instance"""
        if not token:
            token = self.endpoints.createAccessToken(
                emailOrUsername=username, 
                password=password,
                withHttpOnlyToken=True,
            )['item']
        if accept_terms:
            raise NotImplementedError('Term accepting workflow is not implemented yet')
            self.endpoints.getTerms(type='general', language=self.lang)
            self.endpoints.acceptTerms(pendingToken=token, signature=None)
        self.client.headers['Authorization'] = f'Bearer {token}'
    
    def logout(self) -> None:
        """Logout the current User"""
        self.endpoints.deleteAccessToken()
    
    @cached_property
    def me(self) -> User:
        """Get the User object for the currently logged in user"""
        return User(self.endpoints.getUser('me')['item'], self)

    @cached_property
    def config(self) -> Config:
        """Get the configuration info for the current Planka server"""
        return Config(self.endpoints.getConfig()['item'], self)

    @property
    def projects(self) -> list[Project]:
        """Get all Projects available to the current user"""
        return [Project(p, self) for p in self.endpoints.getProjects()['items']]

    @property
    def users(self) -> list[User]:
        """Get all Users on the current instance"""
        if self.me.role in ('admin', 'projectOwner'): 
            return [User(u, self) for u in self.endpoints.getUsers()['items']]
        else:
            raise PermissionError(f'Current user is not Admin or Project Owner!')
    
    def create_project(self, **kwargs: Unpack[typ.Request_createProject]) -> Project:
        """Creates a project. The current user automatically becomes a project manager.

        Args:
            type (Literal['public', 'private']): Type of the project
            name (str): Name/title of the project
            description (str): Detailed description of the project

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
        """
        return Project(self.endpoints.createProject(**kwargs)['item'], self)
    
    def create_user(self, **kwargs: Unpack[typ.Request_createUser]) -> User:
        """Creates a user account. Requires admin privileges.

        Args:
            email (str): Email address for login and notifications
            password (str): Password for user authentication (must meet password requirements)
            role (Literal['admin', 'projectOwner', 'boardUser']): User role defining access permissions
            name (str): Full display name of the user
        
        Optional:
            username (str): Unique username for user identification
            phone (str): Contact phone number
            organization (str): Organization or company name
            language (LanguageCode): Preferred language for user interface and notifications (example: 'en-US')
            subscribeToOwnCards (bool): Whether the user subscribes to their own cards
            subscribeToCardWhenCommenting (bool): Whether the user subscribes to cards when commenting
            turnOffRecentCardHighlighting (bool): Whether recent card highlighting is disabled

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            Conflict: 409 
        """
        return User(self.endpoints.createUser(**kwargs)['item'], self)


