"""
Base interface for Planka

Note:
    If you would like to use a different language with Planka, either set the `lang` parameter 
    on initialization, or set the `PLANKA_LANG` environment variable with yout preferred language
    ```python
    >>> planka = Planka(..., lang='zh-CN')
    >>> planka.lang
    zh-CN
    ```
    Or
    ```
    declare -x PLANKA_LANG="zh-CN"
    ```
    ```python
    >>> planka = Planka(...)
    >>> planka.lang
    zh-CN
"""

from __future__ import annotations
from functools import cached_property
from typing import Unpack
from warnings import warn
from datetime import timezone

from httpx import Client, HTTPStatusError
from .api import (
    PlankaEndpoints, 
    paths, # Response / Request typing
)
from .models import *
from .models._literals import TermsType, UserRole

# Allow Users to set `PLANKA_LANG` environment variable with their language
# Default to en-US if not set
import os
DEFAULT_LANG = os.environ.get('PLANKA_LANG', 'en-US')
del os

class Planka:
    def __init__(self, client: Client, *, lang: str=DEFAULT_LANG, timezone: timezone = timezone.utc) -> None:
        self.client = client
        self.endpoints = PlankaEndpoints(client)
        if lang not in Languages:
            warn(f'{lang} is not currently supported by Planka, using {DEFAULT_LANG}', EncodingWarning)
            lang = DEFAULT_LANG
        self.lang = lang
        self.timezone = timezone
        
        # Assigned after logon() is called
        self.current_role: UserRole | None = None
        self.current_id = None
    
    def accept_terms(self, pending_token: str, terms_type: TermsType='general'):
        """If the User has never logged on, or is required to accept new terms, allow them to do so"""
        terms = self.endpoints.getTerms(type=terms_type, language=self.lang)['item']
        print(terms['content'])
        sig = terms['signature']
        self.endpoints.acceptTerms(pendingToken=pending_token, signature=sig)
    
    def logon(self, *, 
              username: str|None=None, 
              password: str|None=None, 
              api_key: str|None=None, 
              accept_terms: TermsType | None=None) -> None:
        
        """Authenticate with the planka instance
        
        Args:
            username (str | None): User username/email 
            password (str | None): User password
            api_key (str | None): User API Key
            accept_terms (TermsType | None): If you user has not accepted the terms, run the term acceptance flow
            
        Note:
            After accepting the terms, please get an API key from the Planka server. If you need to accept extended terms, please 
            set the `terms` flag to the terms you are accepting. These terms will be printed to `stdout` during the flow.
        """
        # API Key
        if api_key:
            self.client.headers['X-Api-Key'] = api_key
        
        # User/Pass with term acceptance flow
        elif username and password:
            try:
                # Get Bearer Auth
                token = self.endpoints.createAccessToken(emailOrUsername=username, password=password, withHttpOnlyToken=True)['item']
                self.client.headers['Authorization'] = f'Bearer {token}'
            except HTTPStatusError as e:
                if accept_terms is None:
                    raise PermissionError(f'Please logon again with `accept_terms` set to the terms you must accept')
                self.accept_terms(e.response.json()['pendingToken'], terms_type=accept_terms)
                self.logon(username=username, password=password)
        
        # Invalid Creds
        else:
            raise PermissionError(f'No credentials supplied! Must provide a user/password or an api_key')
            
        self.current_role = self.me.role
        self.current_id = self.me.id
    
    def logout(self) -> None:
        """Logout the current User"""
        self.endpoints.deleteAccessToken()
    
    @cached_property
    def me(self) -> User:
        """Get the User object for the currently logged in user"""
        return User(self.endpoints.getUser('me')['item'], self)

    @property
    def notifications(self) -> list[Notification]:
        """Get all notifications for the current User"""
        return [Notification(n, self) for n in self.endpoints.getNotifications()['items']]

    @property
    def unread_notifications(self) -> list[Notification]:
        """Get all unread Notifications for the current user"""
        return [n for n in self.notifications if not n.is_read]

    @cached_property
    def config(self) -> Config:
        """Get the configuration info for the current Planka server"""
        return Config(self.endpoints.getConfig()['item'], self)

    @property
    def webhooks(self) -> list[Webhook]:
        """Get all configured Webhooks (requires admin)"""
        return [
            Webhook(w, self) 
            for w in self.endpoints.getWebhooks()['items']
            if self.me.role == 'admin'
        ]

    @property
    def projects(self) -> list[Project]:
        """Get all Projects available to the current user
        
        Note:
            admins will get all instance Projects
            projectOwners will get all owned projects and shared projects
            all others will get only assigned and shared projects
        """
        return [Project(p, self) for p in self.endpoints.getProjects()['items']]

    @property
    def users(self) -> list[User]:
        """Get all Users on the current instance (requires admin or projectOwner role)
        
        Note:
            projectOwners will only get Users in their Projects
            admins will get all instance Users
            all others will get an empty list 
        """
        return [
            User(u, self) 
            for u in self.endpoints.getUsers()['items']
            if self.current_role in ('admin', 'projectOwner')
        ]
    
    def read_notification(self) -> list[Notification]:
        """Read all Notifications for the current User"""
        return [Notification(n, self) for n in self.endpoints.readAllNotifications()['items']]
    
    def create_project(self, **kwargs: Unpack[paths.Request_createProject]) -> Project:
        """Creates a project. The current user automatically becomes a project manager.

        Args:
            type (ProjectType): Type of the project
            name (str): Name/title of the project
            description (str): Detailed description of the project

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            PermissionError: If User is not an admin or projectOwner
            ValidationError: 400 
            Unauthorized: 401 
        """
        if self.current_role not in ('admin', 'projectOwner'):
            raise PermissionError(f'Onlt Admins and Project Owners can create Projects')
        return Project(self.endpoints.createProject(**kwargs)['item'], self)
    
    def create_user(self, **kwargs: Unpack[paths.Request_createUser]) -> User:
        """Creates a user account. Requires admin privileges.

        Args:
            email (str): Email address for login and notifications
            password (str): Password for user authentication (must meet password requirements)
            role (UserRole): User role defining access permissions
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
            PermissionError: If the current user is not an admin
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            Conflict: 409 
        """
        if self.current_role != 'admin':
            raise PermissionError(f'Only Admins can create Users')
        return User(self.endpoints.createUser(**kwargs)['item'], self)

    def create_webhook(self, **kwargs: Unpack[paths.Request_createWebhook]) -> Webhook:
        """Create a Webhook (admin only)
        
        Args:
            name (str) : Name/title of the webhook
            url (str): URL endpoint for the webhook
            accessToken (NotRequired[str]): Access token for webhook authentication
            events (NotRequired[WebhookEvent]): list of events that trigger the webhook
            excludedEvents (NotRequired[WebhookEvent]): Comma-separated list of events excluded from the webhook
        
        Returns:
            Webhook
        
        Raises:
            PermissionError: If the current user is not an admin
        """
        if self.current_role != 'admin':
            raise PermissionError(f'Only admins can create Webhooks')
        return Webhook(self.endpoints.createWebhook(**kwargs)['item'], self)
        
