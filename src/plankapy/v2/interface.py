"""
Base interface for Planka

When reading the documentation, all returned `list[PlankaModel]` types are 
actually `models.ModelLists` at runtime. These will also be properly type hinted by 
your static type checker and expose some alternate ways of indexing into model lists:

Example:
```python
>>> type(planka.projects)
ModelList

# Using an exact schema filter
>>> planka.projects[{'name': 'My Project'}]
[Project(name='My Project', ...)]

# Using a functional schema filter (name is replaced with the value of name)
>>> planka.projects[{'name': lambda name: 'My' in name}]
[Project(name='My Project', ...), Project(name='My Other Project', ...)]

# Using a model filter
>>> planka.projects[lambda project: project.owner == planka.me]
[<previous results>..., Project('Another Project I Own', ...)]
```

All dictionary based schema filtering can be done per key and the model will only 
be included in the output if all filters match.

Additionally, a `dpop` method is included that allows popping from a model list with 
a default value if no results
```python
>>> filtered = to_do_list.cards[lambda c: c.due_date and (c.due_date - datetime.now()).days < 4]
>>> if next_card := filtered.dpop():
...     print(next_card.url)
...     print(next_card.name)
... else:
...     print('No results')
https://planka.mydomain.com/cards/1234...
'Critical Project'
--or--
No results
```
"""

from __future__ import annotations
from functools import cached_property
from typing import Sequence
from datetime import timezone

from httpx import Client, HTTPStatusError

from .api import (
    PlankaEndpoints, 
    events,
)
from .models import *
from .models._helpers import queryable
from .models._literals import Language, TermsType, UserRole, ProjectType

# Allow Users to set `PLANKA_LANG` environment variable with their language
# Default to en-US if not set
import os
DEFAULT_LANG = os.environ.get('PLANKA_LANG', 'en-US')
del os

class Planka:
    """Root object for connecting to a Planka instance
    
    A Planka instance can be initialized using a `base_url` or a `httpx.Client` objcet.
    If both arguments are passed, the `base_url` of the passed client will be overriden with
    the url passed to the `base_url` argument

    Example:

        Using the default Client with a base_url
        ```python
        >>> planka = Planka('https://planka.example.com')
        ... planka.client
        <httpx.Client object at 0x...>

        >>> planka.client.base_url
        URL('https://planka.example.com')
        ```
        Client based initialization
        ```python
        >>> hooks = {'request': [hook1, hook2], 'response': [hook3, hook4]}
        ... client = Client(event_hooks=hooks)
        ... planka = Planka('https://planka.example.com', client=client)
        ... planka.client.event_hooks
        {'request': [<hook1>, <hook2>], 'response': [<hook3>, <hook4>]}
        ```
    
    All Planka sessions will respect the configuration of the passed client object. For more configuration 
    options, see the httpx docs: https://www.python-httpx.org/advanced/clients/

    After initializing, the Planka instance required the authorization flow to 
    take place using the `login` method

    Example:
        ```python
        >>> # Using an API key
        ... planka.login(api_key='<my_api_key>')
        ... planka.projects
        [Project(...), Project(...), ...]
        ```
        ```python
        >>> # First time login (accept instance ToS)
        ... planka.login(username='me@email.com', password='mypassword', accept_terms=True)
        TERMS OF SERVICE
        --- More ToS ---

        >>> planka.projects
        [Project(...), Project(...), ...]
        ```

    Logging in with a username and password will work, but it's best practice to authenticate 
    using an api key, which you can get from your instance administrator.
    """

    def __init__(self, 
                 base_url: str|None=None, 
                 *, 
                 client: Client|None=None, 
                 timezone: timezone = timezone.utc) -> None:
        """
        Args:
            base_url: The base url of the instance (e.g. `https://planka.app`)
            client: An optional pre-configured `httpx.Client` object to use as the session client
            timezone: An optional timezone to cast all datetimes to for date math

        Raises:
            ValueError: If no base_url or no client with a base_url
        """
        if client is None and base_url:
            self.client = Client(base_url=base_url)
        elif client and base_url is None:
            if not client.base_url:
                raise ValueError(
                    f'If using a client, the client\'s base_url attribute must be set '
                    'or a base_url must be passed to the Planka initializer'
                )
            self.client = client
        elif base_url and client:
            self.client = client
            self.client.base_url = base_url
        else:
            raise ValueError(f'base_url and/or client must be passed')
        
        self.endpoints = PlankaEndpoints(self.client)
        self.timezone = timezone
        
        # Assigned after login() is called
        self.current_role: UserRole | None = None
        self.current_id = None
    
    def accept_terms(self, pending_token: str, terms_type: TermsType='general', lang: Language='en-US'):
        """If the User has never logged on, or is required to accept new terms, allow them to do so"""
        terms = self.endpoints.getTerms(type=terms_type, language=lang)['item']
        print(terms['content'])
        sig = terms['signature']
        self.endpoints.acceptTerms(pendingToken=pending_token, signature=sig)
    
    def login(self, 
              *, 
              username: str|None=None, 
              password: str|None=None, 
              api_key: str|None=None, 
              accept_terms: TermsType | None=None,
              terms_lang: Language='en-US') -> None:
        
        """Authenticate with the planka instance
        
        Args:
            username (str | None): User username/email 
            password (str | None): User password
            api_key (str | None): User API Key
            accept_terms (TermsType | None): If you user has not accepted the terms, run the term acceptance flow
            terms_lang: If accepting terms, request them in this language
            
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
                self.accept_terms(e.response.json()['pendingToken'], terms_type=accept_terms, lang=terms_lang)
                self.login(username=username, password=password)
        
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
    @queryable
    def notifications(self) -> list[Notification]:
        """Get all notifications for the current User"""
        return [Notification(n, self) for n in self.endpoints.getNotifications()['items']]

    @property
    @queryable
    def unread_notifications(self) -> list[Notification]:
        """Get all unread Notifications for the current user"""
        return [n for n in self.notifications if not n.is_read]

    @cached_property
    def config(self) -> Config:
        """Get the configuration info for the current Planka server"""
        return Config(self.endpoints.getConfig()['item'], self)

    @property
    @queryable
    def webhooks(self) -> list[Webhook]:
        """Get all configured Webhooks (requires admin)"""
        return [
            Webhook(w, self) 
            for w in self.endpoints.getWebhooks()['items']
            if self.me.role == 'admin'
        ]

    @property
    @queryable
    def projects(self) -> list[Project]:
        """Get all Projects available to the current user
        
        Note:
            admins will get all instance Projects
            projectOwners will get all owned projects and shared projects
            all others will get only assigned and shared projects
        """
        return [Project(p, self) for p in self.endpoints.getProjects()['items']]

    @property
    @queryable
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
    
    @queryable
    def read_notifications(self) -> list[Notification]:
        """Read all Notifications for the current User"""
        return [Notification(n, self) for n in self.endpoints.readAllNotifications()['items']]
    
    def create_project(self, 
                       *,
                       name: str,
                       type: ProjectType,
                       description: str|None=None) -> Project:
        """Creates a project. The current user automatically becomes a project manager.

        Must be a Project Owner or an Admin
        
        Args:
            type: Type of the project
            name: Name/title of the project
            description: Detailed description of the project
        """
        return Project(
            self.endpoints.createProject(
                name=name, 
                type=type, 
                description=description,
            )['item'], 
            self
        )
    
    def create_user(self, 
                    *,
                    email: str,
                    password: str,
                    role: UserRole,
                    name: str,
                    username: str|None=None,
                    phone: str|None=None,
                    organization: str|None=None,
                    language: Language|None=None,
                    subscribe_to_own_cards: bool=False,
                    subscribe_to_cards_when_commenting: bool=True,
                    turn_off_recent_card_highlighting: bool=False) -> User:
        """Creates a user account. Requires admin privileges.

        Only `email`, `password`, `role`, and `name` are required

        Args:
            email (str): Email address for login and notifications
            password (str): Password for user authentication (must meet password requirements)
            role (UserRole): User role defining access permissions
            name (str): Full display name of the user
            username (str): Unique username for user identification
            phone (str): Contact phone number
            organization (str): Organization or company name
            language (LanguageCode): Preferred language for user interface and notifications (example: `en-US`)
            subscribe_to_own_cards (bool): Whether the user subscribes to their own cards
            subscribe_to_cards_when_commenting (bool): Whether the user subscribes to cards when commenting
            turn_off_recent_card_highlighting (bool): Whether recent card highlighting is disabled
        """

        return User(
            self.endpoints.createUser(
                email=email,
                password=password,
                role=role,
                name=name,
                username=username,
                phone=phone,
                organization=organization,
                language=language,
                subscribeToOwnCards=subscribe_to_own_cards,
                subscribeToCardWhenCommenting=subscribe_to_cards_when_commenting,
                turnOffRecentCardHighlighting=turn_off_recent_card_highlighting,
            )['item'], 
            self
        )

    def create_webhook(self, 
                       *,
                       name: str,
                       url: str,
                       access_token: str|None=None,
                       events: Sequence[events.PlankaEvent]|None=None,
                       excluded_events: Sequence[events.PlankaEvent]|None=None) -> Webhook:
        """Create a Webhook. Requires admin
        
        Args:
            name: Name/title of the webhook
            url: URL endpoint for the webhook
            access_token: Access token for webhook authentication
            events: list of events that trigger the webhook
            excluded_events: Comma-separated list of events excluded from the webhook
        """
        args = {
            'name': name,
            'url': url
        }
        if events:
            args['events'] = ','.join(events)
        if excluded_events:
            args['excludedEvents'] = ','.join(excluded_events)
        if access_token:
            args['accessToken'] = access_token
        return Webhook(self.endpoints.createWebhook(**args)['item'], self)
        
