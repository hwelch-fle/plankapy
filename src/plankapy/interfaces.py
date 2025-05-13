from __future__ import annotations

from typing import Type, overload
from datetime import datetime

from pathlib import Path

from random import choice
from urllib.request import HTTPError

from .routes import Routes
from .models import (
    Model,
    Action_,
    Archive_,
    Attachment_,
    Board_,
    BoardMembership_,
    Card_,
    Stopwatch,
    CardLabel_,
    CardMembership_,
    CardSubscription_,
    IdentityProviderUser_,
    Label_,
    List_,
    Notification_,
    Project_,
    ProjectManager_,
    Task_,
    User_,
    QueryableList,
)
from .handlers import (
    BaseAuth, 
    JSONHandler,
)

from .constants import (
    Gradient,
    GradientCSSMap,
    LabelColor,
    LabelColorHexMap,
    BoardRole,
    BackgroundImage,
    SortOption,
    ListSorts,
    ListColors,
)


def parse_overload(args:tuple, kwargs: dict, model: str, options: tuple[str], required: tuple[str]=(), noarg:Model=None) -> dict:
    """Helper function that allows overloading with required values or a model instance

    Converts positional arguments to keyword arguments if not already provided

    Args:
        args (tuple): tuple of arguments
        kwargs (dict): dictionary of keyword arguments
        model (str): model name
        required (tuple[str]): required arguments
        noarg (Model): Used to pass self for update methods (default: None)

    Returns:
        dict: dictionary of required arguments

    Raises:
        ValueError: if required arguments are not provided

    Example:
        ```python
        # Positional required arguments
        >>> parse_overload(('My board', 0), {}, 'board', ('name', 'position'))
        {'name': 'My board', 'position': 0}

        # Keyword required arguments
        >>> parse_overload((), {'name': 'My board', 'position': 0}, 'board', ('name', 'position'))
        {'name': 'My board', 'position': 0}

        # Positional Model instance
        >>> parse_overload((Board(name='My Board', position=0)), {}, 'board', ('name', 'position'))
        {'name': 'My board', 'position': 0}

        # Keyword Model instance
        >>> parse_overload((), {'board': Board(name='My Board', position=0)}, 'board', ('name', 'position'))
        {'name': 'My board', 'position': 0}

        # No arguments
        >>> board = Board(name='My Board', position=0)
        >>> board.name = 'My New Board'
        >>> parse_overload((), {}, 'board', ('name', 'position'), noarg=self)
        {'name': 'My New Board', 'position': 0}
        ```

    """
    # Convert options and required to tuples if they have a single value
    if isinstance(options, str):
        options = (options,)
    if isinstance(required, str):
        required = (required,)

    # Unpack provided model
    if args and isinstance(args[0], Model) or model in kwargs:
        return {**args[0]} if args else {**kwargs[model]}

    # Convert positional to keyword arguments
    elif args:
        coded_args = dict(zip(options, args))
        kwargs.update(coded_args)

    # Use self if no arguments are provided
    elif noarg and not kwargs:
        return {**noarg}

    # Check for required arguments
    if not all([arg in kwargs for arg in required]):
        raise ValueError(f'Required: {required}')
    
    return kwargs

class Planka:
    """Root object for interacting with the Planka API

    Attributes:
        auth (Type[BaseAuth]): Authentication method
        url (str): Base url for the Planka instance
        handler (JSONHandler): JSONHandler instance for making requests

    Note:
        All objects that return a list of objects will return a `QueryableList` object. This object is a subclass of `list`
        see the `QueryableList` docs for more information
    
    Note:
        All implemented public properties return API responses with accessed. This means that the values are not cached 
        and will be updated on every access. If you wish to cache values, you are responsible for doing so. By default, 
        property access will always provide the most up to date information.
        
        Example:
            ```python
            >>> len(project.cards)
            5
            >>> project.create_card('My Card')
            >>> len(project.cards)
            6
            ```

    Example:
        ```python
        >>> from plankapy import Planka, PasswordAuth

        >>> auth = PasswordAuth('username', 'password')
        >>> planka = Planka('https://planka.example.com', auth)

        >>> planka.me
        User(id=...9234, name='username', ...)
        ```
    
    Tip:
        If you want to store a property chain to update later, but dont want to call it by full name, you can use a lambda

        Example:
            ```python
            >>> card = lambda: planka.project[0].boards[0].lists[0].cards[0]
            >>> comments = lambda: card().comments
            >>> len(comments())
            2
            
            >>> card().add_comment('My Comment')
            >>> len(comments())
            3
            ```
    
    Tip:
        All objects inherit the `editor` context manager from the `Model` class except `Planka`.
        This means if you want to make changes to something, you can do it directly to attributes
        in an editor context instead of calling the model's `update` method

        Example:
            ```python
            >>> with card.editor():
            ...    card.name = 'My New Card'
            ...    card.description = 'My New Description'

            >>> card.name
            'My New Card'
            ```
    """
    def __init__(self, url: str, auth: Type[BaseAuth]):        
        self._url = url
        self._auth = auth
        self._create_session()

    def _create_session(self) -> None:
        """INTERNAL: Creates a new session with the current authentication method and url"""
        self.handler = JSONHandler(self.url)
        self.handler.headers.update(self.auth.authenticate(self.url))
        self.routes = Routes(self.handler)
    
    @property
    def auth(self) -> Type[BaseAuth]:
        """Current authentication instance

        Returns:
            Authentication method
        """
        return self._auth

    @auth.setter
    def auth(self, auth: Type[BaseAuth]):
        """Changes the authentication method and creates a new session
        
        Args:
            auth (Type[BaseAuth]): New authentication method
            
        Warning:
            Changing the authentication method will create a new session with the current url, 
            If you need to change both the url and the authentication method, create a new Planka instance
            
        Example:
            ```python
            >>> planka.auth = TokenAuth('<new_token>')
            ```
        """
        self._auth = auth
        self._create_session(auth)

    @property
    def url(self) -> str:
        """The current planka url

        Returns:
            Planka url
        """
        return self._url
    
    @url.setter
    def url(self, url: str):
        """Changes the base url and creates a new session
        
        Args:
            url: New base url
        
        Warning:
            Changing the url will create a new session with the current authentication method, 
            If you need to change both the url and the authentication method, create a new Planka instance
            
        Example:
            ```python
            >>> planka.url = 'https://planka.example.com'
            ```
        """
        self._url = url
        self._create_session(self.auth)

    @property
    def projects(self) -> QueryableList[Project]:
        """Queryable List of all projects on the Planka instance
        
        Returns:
            Queryable List of all projects
        """
        route = self.routes.get_project_index()
        return QueryableList([
            Project(**project).bind(self.routes)
            for project in route()['items']
        ])
    
    @property
    def users(self) -> QueryableList[User]:
        """Queryable List of all users on the Planka instance
        
        Returns:
            Queryable List of all users
        """
        route = self.routes.get_user_index()
        return QueryableList([
            User(**user).bind(self.routes)
            for user in route()['items']
        ])
    
    @property
    def notifications(self) -> QueryableList[Notification]:
        """Queryable List of all notifications for the current user
        
        Returns:
            Queryable List of all notifications
        """
        route = self.routes.get_notification_index()
        return QueryableList([
            Notification(**notification).bind(self.routes)
            for notification in route()['items']
        ])
    
    @property
    def project_background_images(self) -> QueryableList[BackgroundImage]:
        """Get Project Background Images
        
        Returns:
            Queryable List of all project background images
        """
        return QueryableList(
            BackgroundImage(**project.backgroundImage)
            for project in self.projects
            if project.backgroundImage
        )

    @property
    def user_avatars(self) -> list[str]:
        """Get User Avatars

        Returns:
            Queryable List of all user avatar links
        """
        return [
            user.avatarUrl
            for user in self.users
            if user.avatarUrl
        ]
    @property
    def me(self) -> User:
        """Current Logged in User
        
        Returns:
            Current user
        """
        route = self.routes.get_me()
        return User(**route()['item']).bind(self.routes)
    
    @property
    def config(self) -> JSONHandler.JSONResponse:
        """Planka Configuration
        
        Returns:
            Configuration data
        """
        route = self.routes.get_config()
        return route()['item']
    
    @overload
    def create_project(self, project: Project) -> Project: ...

    @overload
    def create_project(self, name: str, position: int=None, 
                       background: Gradient=None) -> Project: ...

    def create_project(self, *args, **kwargs) -> Project:
        """Creates a new project
        
        Note:
            If no background is provided, a random gradient will be assigned

            If no position is provided, the project will be created at position 0

        Args:
            name (str): Name of the project (required)
            position (int): Position of the project (default: 0)
            background (Gradient): Background gradient of the project (default: None)
            
        Args: Alternate
            project (Project): Project instance to create
        
        Returns:
            Project: New project instance

        Example:
            ```python
            >>> new_project = planka.create_project('My Project')
            >>> new_project.set_background_gradient('blue-xchange') # Set background gradient
            >>> new_project.add_project_manager(planka.me) # Add current user as project manager
            ```
        """
        overload = parse_overload(args, kwargs, model='project', 
                                  options=('name', 'position', 'background'), 
                                  required=('name',))

        overload['position'] = overload.get('position', 0)
        
        style = overload.get('background', None)
        route = self.routes.post_project()
        project = Project(**route(**overload)['item']).bind(self.routes)

        with project.editor(): # Project POST does not accept background, so we set it after creation
            project.set_background_gradient(style or choice(Project.gradients))

        return project

        
    def create_user(self, username: str, email: str, password: str, name: str=None) -> User:
        """Create a new user
        
        Note:
            Planka will reject insecure passwords! If creating a user with a specific password fails, 
            try a more secure password
        
        Note:
            If the username is not lowercase, it will be converted to lowercase

        Args:
            username (str): Username of the user (required)
            email (str): Email address of the user (required)
            password (str): Password for the user (required)
            name (str): Full name of the user (default: `username`)

        Raises:
            ValueError: If the username or email already exists
            ValueError: If password is insecure or a 400 code is returned
        """

        username = username.strip()
        if not username.islower():
            print('Warning: Usernames are converted to lowercase')
            username = username.lower()

        for user in self.users:
            if user.username == username:
                raise ValueError(f'Username {username} already exists. '
                                 'Please use a different username')
            if user.email == email:
                raise ValueError(f'Email {email} already exists. '
                                 'Please use a different email address')
            
        route = self.routes.post_user()
        try:
            return User(**route(username=username, name=name or username, password=password, email=email)['item']).bind(self.routes)
        except HTTPError as e:
            if e.code == 400: # Invalid password, email, or username
                raise ValueError(
                    f'Failed to create user {username}:\n'
                    '\tTry: \n'
                    '\t\tA more secure password\n'
                    '\t\tValidating the user\'s email address\n'
                    '\t\tChecking that the username has no whitespace') from e
            else: # Unknown error
                raise e

class Project(Project_):
    """Interface for interacting with planka Projects and their included sub-objects
    
    Attributes:
        gradients (list[Gradient]): All available gradients
        gradient_to_css (dict[Gradient, str]): Mapping of gradient names to CSS values
    """

    gradients = Gradient.__args__
    gradient_to_css = GradientCSSMap

    @property
    def _included(self) -> JSONHandler.JSONResponse:
        """Included data for the project
        
        Warning:
            This property is meant to be used internally for building objects in the other properties
            It can be directly accessed, but it will only return JSON data and not objects
        
        Returns:
            Included data for the project
        """
        route = self.routes.get_project(id=self.id)
        return route()['included']
    
    @property
    def users(self) -> QueryableList[User]:
        """All users in the project
        
        Returns:
            Queryable List of all users
        """
        return QueryableList([
            User(**user).bind(self.routes)
            for user in self._included['users']
        ])
    
    @property
    def projectManagers(self) -> QueryableList[ProjectManager]:
        """All project managers (ProjectManager Relations)
        
        Note:
            This property is not a list of users, but a list of `ProjectManager` objects
            that define the user's role in the project. This is used to remove managers
            in associated project boards and will likely never be used directly

        Returns:
            Queryable List of all project manager relations
        """
        return QueryableList([
            ProjectManager(**projectManager).bind(self.routes)
            for projectManager in self._included['projectManagers']
        ])

    @property
    def managers(self) -> QueryableList[User]:
        """All project managers (Users)
        
        Returns:
            Queryable List of all project managers
        """
        return QueryableList([
            user
            for user in self.users
            for projectManager in self.projectManagers
            if projectManager.userId == user.id
        ])
        
    
    @property
    def boardMemberships(self) -> QueryableList[BoardMembership]:
        """All board memberships and roles in the project
        
        Note:
            This property is not a list of users, but a list of `BoardMembership` objects
            that define the user's role in the project boards. This is used to remove memberships
            in associated project boards and will likely never be used directly
        
        Returns:
            Queryable List of all board membership relations in the project    
        """
        return QueryableList([
            BoardMembership(**boardMembership).bind(self.routes)
            for boardMembership in self._included['boardMemberships']
        ])

    @property
    def boards(self) -> QueryableList[Board]:
        """All boards in the project
        
        Returns:
            Queryable List of all boards
        """
        return QueryableList([
            Board(**board).bind(self.routes)
            for board in self._included['boards']
        ])
    
    def download_background_image(self, path: Path) -> Path | None:
        """Download a background image from the project
        
        Args:
            path (Path): Path to save the image file
        
        Returns:
            Path: Path to the downloaded image file or None if no background image is set
            
        Example:
            ```python
            >>> project.download_background_image('/home/user/downloads/background.jpg')
            ```
        """
        if not self.backgroundImage:
            return None
        
        path = Path(path)
        path.write_bytes(self.routes.handler._get_file(self.backgroundImage['url']))
        return path
        

    def gradient_css(self) -> str | None:
        """Get the CSS value for the project gradient

        Note:
            If the project has no gradient set, this will return `None`

        Returns:
            CSS value for the gradient
        """
        gradient = self.background
        if gradient.type != 'gradient':
            return None
        return self.gradient_to_css[gradient.name]

    @overload
    def create_board(self, board: Board) -> Board: ...

    @overload
    def create_board(self, name: str, position: int=0) -> Board: ...

    def create_board(self, *args, **kwargs) -> Board:
        """Creates a new board in the project from a name and position or a Board instance
        
        Args:
            name (str): Name of the board
            position (int): Position of the board (default: 0)
            
        Args: Alternate
            board (Board): Board instance to create

        Returns:
            Board: New board instance
        """
        overload = parse_overload(
            args, kwargs, 
            model='board', 
            options=('name', 'position'), 
            required=('name',))

        overload['position'] = overload.get('position', 0)
        overload['projectId'] = self.id
        
        route = self.routes.post_board(projectId=self.id)
        return Board(**route(**overload)['item']).bind(self.routes)

    @overload
    def add_project_manager(self, user: User) -> ProjectManager: ...

    @overload
    def add_project_manager(self, userId: int) -> ProjectManager: ...

    def add_project_manager(self, *args, **kwargs) -> ProjectManager:
        """Creates a new project manager in the project

        Note:
            This method has overloaded arguments,
            You can pass a `User` instance or provide a required `userId` argument

        Args:
            userId (int): id of the user to make project manager (required)

        Args: Alternate    
            user (User): User instance to create (required)

        Returns:
            ProjectManager: New project manager instance
        
        Example:
            ```python
            >>> new_manager = project.create_project_manager(planka.me)
            >>> other_manager = project.create_project_manager(userId='...1234')
            ```
        
        """
        overload = parse_overload(
            args, kwargs, 
            model='user', 
            options=('userId',), 
            required=('userId',))

        userId = overload.get('userId', None)
        
        if not userId: # Get id from passed User
            userId = overload.get('id')
        
        # Don't assign a manager twice (raises HTTP 409 - Conflict)
        if userId in [manager.id for manager in self.managers]:
            return

        route = self.routes.post_project_manager(projectId=self.id)
        return ProjectManager(**route(userId=userId, projectId=self.id)['item']).bind(self.routes)

    @overload
    def remove_project_manager(project_manager: User) -> ProjectManager | None: ...

    @overload
    def remove_project_manager(userId: int) -> ProjectManager | None: ...

    def remove_project_manager(self, *args, **kwargs) -> ProjectManager | None:
        overload = parse_overload(args, kwargs,
                                  model='user',
                                  options=('userId',),
                                  required=('userId',)
        )
        
        if 'userId' not in overload: # Case for User object
            overload['userId'] = overload['id']
        
        for manager in self.projectManagers:
            if manager.userId == overload['userId']:
                return manager.delete()

    def delete(self) -> Project:
        """Deletes the project
        
        Danger:
            This action is irreversible and cannot be undone
        
        Returns:
            Project: Deleted project instance
        """
        self.refresh()
        route = self.routes.delete_project(id=self.id)
        route()
        return self

    @overload
    def update(self, project: Project) -> Project: ...

    @overload
    def update(self, name: str=None) -> Project: ...

    def update(self, *args, **kwargs) -> Project:
        """Updates the project with new values
        
        Note:
            To set background image, use the `set_background_image` method
            To set a background gradient, use the `set_background_gradient` method
        
        Args:
            name (str): Name of the project (required)
            
        Args: Alternate
            project (Project): Project instance to update (required)
        
        Returns:
            Project: Updated project instance

        Example:
            ```python
            >>> project.update(name='My New Project', background='blue-xchange'))
            ```
        """
        overload = parse_overload(
            args, kwargs, model='project', 
            options=('name',),
            noarg=self)

        # Keep it backwards compatible
        # Allow setting gradient directly by name
        if 'background' in overload and isinstance(overload['background'], str):
            bg = overload.pop('background') # Remove background from overload
            if bg in self.gradients:
                self.set_background_gradient(bg) # Set the gradient if it's valid

        route = self.routes.patch_project(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self

    def set_background_gradient(self, gradient: Gradient) -> Project:
        """Set a background gradient for the project
        
        Args:
            gradient (Gradient): Background gradient to set
        
        Returns:
            Project: Updated project instance

        Raises:
            ValueError: If the gradient name is not in the available gradients
            
        Example:
            ```python
            >>> project.set_background_gradient('blue-xchange')
            ```
        """
        if gradient not in self.gradients:
            raise ValueError(
                f'Invalid gradient: {gradient}'
                f'Available gradients: {self.gradients}')
        
        with self.editor():
            self.backgroundImage = None            
            self.background = {'name': gradient, 'type': 'gradient'}
        
        return self
    
    def set_background_image(self, image: Path) -> BackgroundImage:
        """Add a background image to the project

        Args:
            image (Path): Path to the image file
            
        Returns:
            BackgroundImage: New background image
        """
        route = self.routes.post_project_background_image(id=self.id)
        return BackgroundImage(**route(_file=image)['item']['backgroundImage'])
        
    def remove_background_image(self) -> None:
        """Remove the background image from the project"""
        with self.editor():
            if self.backgroundImage:
                self.backgroundImage = None
                self.background = {'name': f'{choice(self.gradients)}', 'type': 'gradient'}

    def refresh(self) -> None:
        """Refreshes the project data
        
        Note:
            All objects accessed by properties are always up to date, but the root object that contains those
            properties keeps a cache of its own data. This method refreshes the root object data.

            FUTURE: This method might be removed or disabled in the future if I can get a __getattr__ implementation
            to work without causing infinite recursion updating the root object when properties are accessed

        """
        route = self.routes.get_project(id=self.id)
        self.__init__(**route()['item'])

class Board(Board_):
    """Interface for interacting with planka Boards and their included sub-objects
    
    Note:
        All implemented public properties return API responses with accessed. This means that the values are not cached 
        and will be updated on every access. If you wish to cache values, you are responsible for doing so. By default, 
        property access will always provide the most up to date information. 
    """

    roles = BoardRole.__args__

    @property
    def _included(self) -> JSONHandler.JSONResponse:
        """Included data for the board
        
        Warning:
            This property is meant to be used internally for building objects in the other properties
            It can be directly accessed, but it will only return JSON data and not objects

        Returns:
            Included data for the board
        """
        route = self.routes.get_board(id=self.id)
        return route()['included']
    
    @property
    def project(self) -> Project:
        """Project the board belongs to
        
        Note:
            All objects include a reference to their parent object and parent objects include a reference to their children
            This means that you can traverse the entire API structure from any object

        Returns:
            Project: Project instance
        """
        project_route = self.routes.get_project(id=self.projectId)
        return Project(**project_route()['item']).bind(self.routes)

    @property
    def users(self) -> QueryableList[User]:
        """All users in the board

        Returns:
            Queryable List of all users
        """
        return QueryableList([
            User(**user).bind(self.routes)
            for user in self._included['users']
        ])
    
    @property
    def editors(self) -> QueryableList[User]:
        """All users that can edit the board

        Returns:
            Queryable List of all editors
        """
        return QueryableList([
            user
            for user in self.users
            for boardMembership in self.boardMemberships
            if boardMembership.userId == user.id and boardMembership.role == 'editor'
        ])
    
    @property
    def viewers(self) -> QueryableList[User]:
        """All users that can view the board
        
        Returns:
            Queryable List of all viewers
        """
        return QueryableList([
            user
            for user in self.users
            for boardMembership in self.boardMemberships
            if boardMembership.userId == user.id and boardMembership.role == 'viewer'
        ])
    
    @property
    def boardMemberships(self) -> QueryableList[BoardMembership]:
        """All board memberships
        
        Note:
            This property is primarily here for internal use, '.editor' and '.viewer' properties 
            are derived from the board memberships

        Returns:
            Queryable List of all membership types (editor, viewer)
        """
        return QueryableList([
            BoardMembership(**boardMembership).bind(self.routes)
            for boardMembership in self._included['boardMemberships']
        ])
    
    @property
    def labels(self) -> QueryableList[Label]:
        """All labels in the board
        
        Returns:
            Queryable List of all labels in the board
        """
        return QueryableList([
            Label(**label).bind(self.routes)
            for label in self._included['labels']
        ])
    
    @property
    def lists(self) -> QueryableList[List]:
        """All lists in the board
        
        Returns:
            Queryable List of all lists in the board
        """
        return QueryableList([
            List(**_list).bind(self.routes)
            for _list in self._included['lists']
        ])
    
    @property
    def cards(self) -> QueryableList[Card]:
        """All cards in the board
        
        Returns:
            A list of all cards in the board
        """
        return QueryableList([
            Card(**card).bind(self.routes)
            for card in self._included['cards']
        ])
    
    @property
    def cardMemberships(self) -> QueryableList[CardMembership]:
        """All card -> user relationships in the board
        
        Note:
            This property is used by the `Card` class to determine its users

        Returns:
            A list of all card memberships in the board
        """
        return QueryableList([
            CardMembership(**cardMembership).bind(self.routes)
            for cardMembership in self._included['cardMemberships']
        ])
    
    @property
    def cardLabels(self) -> QueryableList[CardLabel]:
        """All card -> label relationships in the board
        
        Note:
            This property is used by the `Card` class to determine its labels

        Returns:
            A list of all card labels in the board
        """
        return QueryableList([
            CardLabel(**cardLabel).bind(self.routes)
            for cardLabel in self._included['cardLabels']
        ])
    
    @property
    def tasks(self) -> QueryableList[Task]:
        """All tasks in the board
        
        Note:
            This property is used by the `Card` class to determine its tasks

        Returns:
            A list of all card tasks in the board
        """
        return QueryableList([
            Task(**task).bind(self.routes)
            for task in self._included['tasks']
        ])
    
    @property
    def attachments(self) -> QueryableList[Attachment]:
        """All attachments in the board
        
        Note:
            This property is used by the `Card` class to determine its attachments
            
        Returns:
            A list of all card attachments in the board
        """
        return QueryableList([
            Attachment(**attachment).bind(self.routes)
            for attachment in self._included['attachments']
        ])

    @overload
    def create_list(self, _list: List) -> List: ...

    @overload
    def create_list(self, name: str, position: int) -> List: ...

    def create_list(self, *args, **kwargs) -> List:
        """Creates a new list in the board
        
        Args:
            name (str): Name of the list (required)
            position (int): Position of the list (default: 0)
            
        Args: Alternate
            list (List): List instance to create
            
        Returns:
            List: New list instance
            
        Example:
            ```python
            >>> new_list = board.create_list('My List')

            >>> l = List(name='My List', position=0)
            >>> new_list2 = board.create_list(l)
            ```
        """
        overload = parse_overload(args, kwargs, model='list', 
                                  options=('name', 'position'), 
                                  required=('name',))
        
        overload['position'] = overload.get('position', 0)
        overload['boardId'] = self.id

        route = self.routes.post_list(boardId=self.id)
        return List(**route(**overload)['item']).bind(self.routes)
    
    @overload
    def create_label(self, label: Label) -> Label: ...

    @overload
    def create_label(self, name: str, position: int=0, color: LabelColor=None) -> Label: ...

    def create_label(self, *args, **kwargs) -> Label:
        """Creates a new label in the board
        
        Args:
            name (str): Name of the label (required)
            position (int): Position of the label (default: 0)
            color (LabelColor): Color of the label (default: "berry-red")
            
        Args: Alternate
            label (Label): Label instance to create
        
        Returns:
            Label: New label instance
            
        Example:
            ```python
            >>> new_label = board.create_label('My Label')
            >>> label = Label(name='My Label', position=0, color='wet-moss')
            >>> new_label2 = board.create_label(label)
            ```
        """
        overload = parse_overload(args, kwargs, model='label', 
                                  options=('name', 'position', 'color'), 
                                  required=('name',)) # Only name requires user provided value
        
        # Required arguments with defaults must be manually assigned
        overload['position'] = overload.get('position', 0)
        overload['color'] = overload.get('color', choice(LabelColor.__args__))
        overload['boardId'] = self.id

        route = self.routes.post_label(boardId=self.id)
        return Label(**route(**overload)['item']).bind(self.routes)

    def add_user(self, user: User, role: BoardRole='viewer', canComment: bool=False) -> BoardMembership:
        """Adds a user to the board
        
        Args:
            user (User): User instance to add
            canComment (bool): Whether the user can comment on the board (default: False)
        
        Returns:
            BoardMembership: New board membership

        Raises:
            ValueError: If the role is invalid (must be 'viewer' or 'editor')
        """
        if role not in self.roles:
            raise ValueError(f'Invalid role: {role}')
        
        if role == 'editor':
            canComment = True
        route = self.routes.post_board_membership(boardId=self.id)
        return BoardMembership(**route(userId=user.id, boardId=self.id, canComment=canComment, role=role)['item']).bind(self.routes)
    
    @overload
    def remove_user(self, user: User) -> User: ...

    @overload
    def remove_user(self, userId: int) -> User: ...

    def remove_user(self, *args, **kwargs) -> User:
        """Remove a user from a board
        """
        overload = parse_overload(args, kwargs,
                                  model='user',
                                  options=('userId',),
                                  required=('userId',))
        
        if 'userId' not in overload: # Case if passed User
            overload['userId'] = overload['id']

        for member in self.boardMemberships:
            if member.userId == overload['userId']:
                member.delete()

    def delete(self) -> Board:
        """Deletes the board

        Danger:
            This action is irreversible and cannot be undone
            
        Returns:
            Board: Deleted board instance
        """
        self.refresh()
        route = self.routes.delete_board(id=self.id)
        route()
        return self

    @overload
    def update(self) -> Board: ...

    @overload
    def update(self, board: Board) -> Board: ...

    @overload
    def update(self, name: str=None, position: int=None) -> Board: ...

    def update(self, *args, **kwargs) -> Board:
        """Updates the board with new values
        
        Args:
            name (str): Name of the board (optional)
            position (int): Position of the board (optional)
        
        Args: Alternate
            board (Board): Board instance to update (required)
        
        Note:
            If no arguments are provided, the board will update itself with the current values
            stored in its attributes
        
        Returns:
            Board: Updated board instance
        """
        overload = parse_overload(
            args, kwargs, 
            model='board', 
            options=('name', 'position'),
            noarg=self)
        
        route = self.routes.patch_board(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self

    def refresh(self) -> None:
        """Refreshes the board data"""
        route = self.routes.get_board(id=self.id)
        self.__init__(**route()['item'])

class User(User_):
    """Interface for interacting with planka Users and their included sub-objects

    """
    @property
    def projects(self) -> QueryableList[Project]:
        """All projects the user is a member of
        
        Returns:
            Queryable List of all projects the user is a member of
        """
        projects_route = self.routes.get_project_index()
        return QueryableList([
            Project(**project).bind(self.routes)
            for project in projects_route()['items']
        ]).select_where(lambda project: self in project.users)
    
    @property
    def boards(self) -> QueryableList[Board]:
        """All boards the user is a member of
        
        Returns:
            Queryable List of all boards the user is a member of
        """
        return QueryableList([
            boardMembership.board
            for project in self.projects
            for boardMembership in project.boardMemberships
            if boardMembership.userId == self.id
        ])
    
    @property
    def cards(self) -> QueryableList[Card]:
        """All cards assigned to the user in all projects
        
        Returns:
            Queryable List of all cards assigned to the user
        """
        return QueryableList([
            cardMembership.card
            for board in self.boards
            for cardMembership in board.cardMemberships
            if cardMembership.userId == self.id
        ])
    
    @property
    def manager_of(self) -> QueryableList[Project]:
        """All projects the user is a manager of
        
        Returns:
            Queryable List of all projects the user is a manager of
        """
        return QueryableList([
            project
            for project in self.projects
            for manager in project.managers
            if manager.id == self.id
        ])
    
    @property
    def notifications(self) -> QueryableList[Notification]:
        """All notifications for the user
        
        Returns:
            Queryable List of all notifications for the user
        """
        route = self.routes.get_notification_index()
        return QueryableList([
            Notification(**notification).bind(self.routes)
            for notification in route()['items']
            if notification['userId'] == self.id
        ])
    
    def download_avatar(self, path: Path) -> Path | None:
        """Download the user's avatar to a file
        
        Args:
            path (Path): Path to save the avatar image
        
        Raises:
            ValueError: If the user has no avatar
        """
        if self.avatarUrl is None:
            return None
        
        path = Path(path)
        path.write_bytes(self.routes.handler._get_file(self.avatarUrl))
        return path

    def set_avatar(self, image: Path) -> User:
        """Set the user's avatar
        
        Note:
            The image path can be a local filepath or a URL.

        Args:
            image (Path): Path to the image file

        Returns:
            User: Updated user instance
        """
        route = self.routes.post_user_avatar(id=self.id)
        return User(**route(_file=image)['item']).bind(self.routes)

    def remove_avatar(self) -> None:
        """Remove the user's avatar"""
        with self.editor():
            self.avatarUrl = None

    @overload
    def update(self) -> User: ...

    @overload
    def update(self, user: User) -> User: ...

    @overload
    def update(self, name: str=None, 
               username: str=None, email: str=None, 
               language: str=None, organization: str=None,
               phone: str=None, avatarUrl: str=None,
               isAdmin: bool=None, isDeletionLocked: bool=None,
               isLocked: bool=None, isRoleLocked: bool=None,
               isUsernameLocked: bool=None, subscribeToOwnCards:bool=None) -> User: ...

    def update(self, *args, **kwargs) -> User:
        """Updates the user with new values
        
        Args:
            name (str): Name of the user (optional)
            username (str): Username of the user (optional)
            email (str): Email of the user (optional)
            language (str): Language of the user (optional)
            organization (str): Organization of the user (optional)
            phone (str): Phone number of the user (optional)
            avatarUrl (str): Avatar url of the user (optional)
            isAdmin (bool): Whether the user is an admin (optional)
            isDeletionLocked (bool): Whether the user is deletion locked (optional)
            isLocked (bool): Whether the user is locked (optional)
            isRoleLocked (bool): Whether the user is role locked (optional)
            isUsernameLocked (bool): Whether the user is username locked (optional)
            subscribeToOwnCards (bool): Whether the user is subscribed to their own cards (optional)
            
        Args: Alternate
            user (User): User instance to update (required)
        
        Note:
            If no arguments are provided, the user will update itself with the current values stored in its attributes

        Returns:
            User: Updated user instance
        """
        overload = parse_overload(
            args, kwargs, 
            model='user', 
            options=('name', 'username', 'email', 'language', 
                     'organization', 'phone', 'avatarUrl', 
                     'isAdmin', 'isDeletionLocked', 'isLocked', 
                     'isRoleLocked', 'isUsernameLocked', 
                     'subscribeToOwnCards'),
            noarg=self)
        route = self.routes.patch_user(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def delete(self) -> User:
        """Deletes the user
        
        Danger:
            This action is irreversible and cannot be undone
        
        Returns:
            User: Deleted user instance
        """
        self.refresh()
        route = self.routes.delete_user(id=self.id)
        route()
        return self
    
    def refresh(self) -> None:
        """Refreshes the user data
        """
        route = self.routes.get_user(id=self.id)
        self.__init__(**route()['item'])

class Notification(Notification_):
    """Interface for interacting with planka Notifications
    
    Note:
        Only notifications that are associated with the current user can be accessed
    """
    @property
    def user(self) -> User:
        """User that the notification is associated with
        
        Returns:
            User: User instance
        """
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def action(self) -> Action:
        """Action that the notification is associated with
        
        Returns:
            Action: Action instance
        """
        action_route = self.routes.get_action(id=self.actionId)
        return Action(**action_route()['item']).bind(self.routes)
    
    @property
    def card(self) -> Card:
        """Card that the notification is associated with
        
        Returns:
            Card: Card instance
        """
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)
    
    @overload
    def update(self): ...
    
    @overload
    def update(self, notification: Notification): ...
    
    @overload
    def update(self, isRead: bool=None): ...
    
    def update(self, *args, **kwargs) -> Notification:
        """Updates the notification with new values
        
        Note:
            The only value that can be updated is the 'isRead' value. There is no way to delete a notification
            use the `.mark_as_read()` method to mark the notification as read

        Args:
            isRead (bool): Whether the notification is read (default: None)
            
        Args: Alternate
            notification (Notification): Notification instance to update with

        Note:
            If no arguments are provided, the notification will update itself with the current values stored in its attributes
        """
        overload = parse_overload(
            args, kwargs, 
            model='notification', 
            options=('isRead',),
            noarg=self)
        
        route = self.routes.patch_notification(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def mark_as_read(self) -> None:
        """Marks the notification as read
        
        Note:
            There is no way to delete a notification, only mark it as read
        """
        with self.editor():
            self.isRead = True
    
    def refresh(self) -> None:
        """Refreshes the notification data"""
        route = self.routes.get_notification(id=self.id)
        self.__init__(**route()['item'])

class BoardMembership(BoardMembership_):
    """Interface for interacting with planka Board Memberships
    
    Note:
        Only memberships that the current user has manager access to can be seen
    """
    @property
    def user(self) -> User:
        """User that the membership is associated with
        
        Returns:
            User: User instance
        """
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def board(self) -> Board:
        """Board that the membership is associated with
        
        Returns:
            Board: Board instance
        """
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @overload
    def update(self): ...
    
    @overload
    def update(self, boardMembership: BoardMembership): ...
    
    @overload
    def update(self, role: BoardRole=None, canComment: bool=None): ...
    
    def update(self, *args, **kwargs) -> BoardMembership:
        """Updates the board membership with new values
        
        Tip:
            Use `.editor()` context manager to update the board membership with the user as an editor

            Example:
            ```python
            >>> with boardMembership.editor():
            ...    boardMembership.role = 'editor'

            >>> boardMembership
            BoardMembership(userId='...', boardId='...', role='editor', canComment=True)
            ```
        
        Warning:
            canComment will always be set to True if the role is 'editor', if a context is used as a user is 
            switched to a viewer, they will maintain their ability to comment unless explicitly set to False

            Example:
            ```python
            >>> boardMembership.role
            'editor'

            >>> with boardMembership.editor():
            ...    boardMembership.role = 'viewer'
           
            >>> boardMembership.canComment
            True

            >>> # Using .update() will not automatically set canComment to False
            >>> # on role change unless specified
            >>> boardMembership.update(role='viewer')
            >>> boardMembership.canComment
            False
            ```

        Args:
            role (BoardRole): Role of the user in the board (default: None)
            canComment (bool): Whether the user can comment on the board (default: None)
        
        Args: Alternate
            boardMembership (BoardMembership): Board membership instance to update with
        
        Returns:
            BoardMembership: Updated board membership instance

        Raises:
            ValueError: If the role is invalid (must be 'viewer' or 'editor')

        Note:
            If no arguments are provided, the board membership will update itself with the current values stored in its attributes
        """
        overload = parse_overload(
            args, kwargs, 
            model='boardMembership', 
            options=('role', 'canComment'),
            noarg=self)
        
        if 'role' in overload:
            if overload['role'] not in self.roles:
                raise ValueError(
                    f'Invalid role: {overload["role"]}'
                    f'Available roles: {self.roles}')
            
            if overload['role'] == 'editor': # Editors can always comment
                overload['canComment'] = True
            
            if overload['role'] == 'viewer': # Viewers can only comment if explicitly set
                overload['canComment'] = overload.get('canComment', False)

        route = self.routes.patch_board_membership(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def delete(self) -> tuple[User, Board]:
        """Deletes the board membership relation
        
        Danger:
            This action is irreversible and cannot be undone
            
        Returns:
            User: The user that was removed from the board
        """
        self.refresh()
        route = self.routes.delete_board_membership(id=self.id)
        route()
        return (self.user, self.board)

    def refresh(self) -> None:
        """Refreshes the board membership data"""
        for membership in self.board.boardMemberships:
            if membership.id == self.id:
                self.__init__(**membership)
    
class Label(Label_):
    """Interface for interacting with planka Labels
    
    Note:
        Label Colors are defined in the `LabelColor` Literal
        currently:

    """
    colors = LabelColor.__args__
    colors_to_hex = LabelColorHexMap

    @property
    def board(self) -> Board:
        """Board the label belongs to
        
        Returns:
            Board: Board instance
        """
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @property
    def cards(self) -> QueryableList[Card]:
        """All cards with the label in the board
        
        Returns:
            Queryable List of all cards with the label in the board
        """
        return QueryableList([
            cardLabel.card
            for cardLabel in self.board.cardLabels
            if cardLabel.labelId == self.id
        ])
    
    @overload
    def update(self) -> Label: ...
    
    @overload
    def update(self, label: Label) -> Label: ...
    
    @overload
    def update(self, name: str=None, color: LabelColor=None, position: int=None) -> Label: ...
    
    def update(self, *args, **kwargs) -> Label:
        """Updates the label with new values
        
        Tip:
            Use `.editor()` context manager to update the label with the user as an editor

            Example:
            ```python
            >>> with label.editor():
            ...    label.name = 'My New Label'
            ...    label.color = 'lagoon-blue'

            >>> label
            Label(name='My New Label', color='lagoon-blue', position=0, ...)
            ``

        Args:
            name (str): Name of the label (optional)
            color (LabelColor): Color of the label (optional)
            position (int): Position of the label (optional)
            
        Args: Alternate
            label (Label): Label instance to update with
            
        Returns:
            Label: Updated label instance

        Raises:
            ValueError: If the color is not in the available colors
        """
        overload = parse_overload(
            args, kwargs, 
            model='label', 
            options=('name', 'color', 'position'),
            noarg=self)
        
        if 'color' in overload and overload['color'] not in self.colors:
            raise ValueError(
                f"Invalid color: {overload['color']}\n"
                f"Valid colors: {self.colors}")

        route = self.routes.patch_label(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def hex_color(self) -> str:
        """Returns the hex color of the label
        
        Returns:
            str: Hex color of the label
        """
        return self.colors_to_hex[self.color]

    def delete(self) -> Label:
        """Deletes the label
        
        Danger:
            This action is irreversible and cannot be undone
        
        Returns:
            Label: Deleted label instance
        """
        self.refresh()
        route = self.routes.delete_label(id=self.id)
        route()
        return self
        
    def refresh(self) -> None:
        """Refreshes the label data"""
        for label in self.board.labels:
            if label.id == self.id:
                self.__init__(**label)

class Action(Action_): 
    
    @property
    def card(self) -> Card:
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)
    
    @property
    def user(self) -> User:
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @overload
    def update(self): ...
    
    @overload
    def update(self, action: Action): ...
    
    @overload
    def update(self, text: str=None): ...
    
    def update(self, *args, **kwargs) -> Action:
        overload = parse_overload(
            args, kwargs, 
            model='action', 
            options=('text',),
            noarg=self)
        
        route = self.routes.patch_comment_action(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def delete(self) -> Action:
        """Deletes the comment action
        
        Danger:
            This action is irreversible and cannot be undone
        
        Returns:
            Action: Deleted comment action instance
        """
        self.refresh()
        route = self.routes.delete_comment_action(id=self.id)
        route()
        return self
    
    def refresh(self) -> None:
        """Refreshes the action data"""
        for action in self.card.comments:
            if action.id == self.id:
                self.__init__(**action)

class Archive(Archive_): 
    """Interface for interacting with planka Archives and their included sub-objects

    Warning:
        This class is not yet implemented and is a placeholder for future development
        There are no current Planka endpoints for interacting with `Archive` objects
    """
    ...

class Attachment(Attachment_):
    
    @property
    def creator(self) -> User:
        """User that created the attachment"""
        user_route = self.routes.get_user(id=self.creatorUserId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def card(self) -> Card:
        """Card the attachment belongs to"""
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)
    
    def refresh(self):
        """Refreshes the attachment data"""
        for attachment in self.card.attachments:
            if attachment.id == self.id:
                self.__init__(**attachment)
    
    def data(self) -> bytes:
        """Attachment data as bytes
        
        Returns:
            Attachment data
        """
        return self.routes.handler._get_file(self.url)

    def download(self, path: Path) -> None:
        """Downloads the attachment to a file
        
        Args:
            path (Path): Path to the file to save the attachment to
        """
        with open(path, 'wb') as file:
            file.write(self.data())

    def update(self) -> Attachment:
        """Updates the attachment with new values"""
        route = self.routes.patch_attachment(id=self.id)
        self.__init__(**route(**self)['item'])
        return self
    
    def delete(self) -> Attachment:
        """Deletes the attachment
        
        Danger:
            This action is irreversible and cannot be undone
        
        Returns:
            Attachment: Deleted attachment instance
        """
        self.refresh()
        route = self.routes.delete_attachment(id=self.id)
        route()
        return self
    
class Card(Card_):
    
    @property 
    def _included(self) -> JSONHandler.JSONResponse:
        route = self.routes.get_card(id=self.id)
        return route()['included']
        
    
    @property
    def creator(self) -> User:
        """User that created the card
        
        Returns:
            User: Creator of the card
        """
        user_route = self.routes.get_user(id=self.creatorUserId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def board(self) -> Board:
        """Board the card belongs to
        
        Returns:
            Board: Board instance
        """
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @property
    def list(self) -> List:
        """List the card belongs to
        
        Returns:
            List: List instance
        """
        for list in self.board.lists:
            if list.id == self.listId:
                return list
    
    @property
    def labels(self) -> QueryableList[Label]:
        """All labels on the card
        
        Returns:
            Queryable List of all labels on the card
        """
        return QueryableList([
            cardLabel.label
            for cardLabel in self.board.cardLabels
            if cardLabel.cardId == self.id
        ])
        
    @property
    def members(self) -> QueryableList[User]:
        """All users assigned to the card
        
        Returns:
            Queryable List of all users assigned to the card
        """
        return QueryableList([
            cardMembership.user
            for cardMembership in self.board.cardMemberships
            if cardMembership.cardId == self.id
        ])
      
    @property
    def comments(self) -> QueryableList[Action]:
        """All comments on the card
        
        Returns:
            Queryable List of all comments on the card
        """
        route = self.routes.get_action_index(cardId=self.id)
        return QueryableList([
            Action(**action).bind(self.routes)
            for action in route()['items']
        ])
    
    @property
    def tasks(self) -> QueryableList[Task]:
        """All tasks on the card
        
        Returns:
            Queryable List of all tasks on the card
        """
        return QueryableList([
            task
            for task in self.board.tasks
            if task.cardId == self.id
        ])
    
    @property
    def attachments(self) -> QueryableList[Attachment]:
        """All attachments on the card
        
        Returns:
            Queryable List of all attachments on the card
        """
        return QueryableList(
            Attachment(**attachment).bind(self.routes)
            for attachment in self._included['attachments'])
    
    @property
    def due_date(self) -> datetime | None:
        """Due date of the card in datetime format

        Note:
            The `dueDate` attribute is stored as an ISO 8601 string, this property will return
            the due date as a python datetime object
        
        Returns:
            Due date of the card
        """
        return datetime.fromisoformat(self.dueDate) if self.dueDate else None
    
    def move(self, list: List) -> Card:
        """Moves the card to a new list
        
        Args:
            list (List): List instance to move the card to
            
        Returns:
            Card: The moved card instance
        """
        self.listId = list.id
        self.boardId = list.boardId
        self.update()
        return self
    
    def duplicate(self) -> Card:
        """Duplicates the card
        
        Note:
            Duplicating a card will always insert it one slot below the original card

        Returns:
            Card: The duplicated card instance
        """
        route = self.routes.post_duplicate_card(id=self.id)
        return Card(**route(**self)['item']).bind(self.routes)
    
    # Not currently working without a file upload endpoint
    # For this to work, we'd need to take the attacment data, post it to the filesystem,
    # Then take the response object and dumb those values (url, coverUrl) into a new
    # Attachment object then post it to the card using the `post_attachment(cardId)` route
    def add_attachment(self, file_path: Path) -> Attachment:
        """Adds an attachment to the card
        
        Args:
            attachment (Path | <url>): Attachment instance to add (can be a file path or url)
            
        Returns:
            Attachment: New attachment instance
        """
        route = self.routes.post_attachment(cardId=self.id)
        return Attachment(**route(_file=file_path)['item']).bind(self.routes)
    
    def add_label(self, label: Label) -> CardLabel:
        """Adds a label to the card
        
        Args:
            label (Label): Label instance to add
            
        Returns:
            CardLabel: New card label instance
        """
        route = self.routes.post_card_label(cardId=self.id)
        return CardLabel(**route(labelId=label.id, cardId=self.id)['item']).bind(self.routes)

    def add_member(self, user: User) -> CardMembership:
        """Adds a user to the card
        
        Args:
            user (User): User instance to add
            
        Returns:
            CardMembership: New card membership instance
        """
        route = self.routes.post_card_membership(cardId=self.id)
        return CardMembership(**route(userId=user.id, cardId=self.id)['item']).bind(self.routes)
    
    def add_comment(self, comment: str) -> Action:
        """Adds a comment to the card
        
        Note:
            Comments can only be added by the authenticated user, all comments made
            through plankapy will be attributed to the user in `planka.me`

        Args:
            comment (str): Comment to add
            
        Returns:
            Action: New comment action instance
        """
        route = self.routes.post_comment_action(cardId=self.id)        
        return Action(**route(text=comment, cardId=self.id)['item']).bind(self.routes)

    @overload
    def add_task(self, task: Task) -> Task: ...

    @overload
    def add_task(self, name: str, position: int=0, 
                 isCompleted: bool=False, isDeleted: bool=False) -> Task: ...
        
    def add_task(self, *args, **kwargs) -> Task:
        """Adds a task to the card

        Args:
            name (str): Name of the task (required)
            position (int): Position of the task (default: 0)
            isCompleted (bool): Whether the task is completed (default: False)
            isDeleted (bool): Whether the task is deleted (default: False)

        Args: Alternate
            task (Task): Task instance to create

        Returns:
            Task: New task instance
        """
        overload = parse_overload(
            args, kwargs, 
            model='task', 
            options=('name', 'position', 'isCompleted', 'isDeleted'), 
            required=('name',)) # Only name requires user provided value
        
        route = self.routes.post_task(cardId=self.id)
        
        # Required arguments with defaults must be manually assigned
        overload['position'] = overload.get('position', 0)
        overload['isCompleted'] = overload.get('isCompleted', False)
        overload['isDeleted'] = overload.get('isDeleted', False)

        return Task(**route(**overload)['item']).bind(self.routes)

    def add_stopwatch(self) -> Stopwatch:
        """Adds a stopwatch to the card if there is not one already
        
        Warning:
            The stopwatch stored in the Card instance dictionary is actually a dictionary
            that is used to update the stopwatch on Planka. When you access the stopwatch
            attribute with `card.stopwatch`, a `Stopwatch` instance is generated. This is
            an implementation detail to keep the stopwatch interface separate from the Card
            interface.
        
            Example:
                ```python
                >>> card.add_stopwatch()
                >>> card.stopwatch
                Stopwatch(startedAt=None, total=0)

                >>> card.__dict__['stopwatch']
                {'startedAt': None, 'total': 0}

                >>> card.stopwatch.start()
                >>> card.stopwatch
                Stopwatch(startedAt=datetime.datetime(2024, 9, 30, 0, 0, 0), total=0)

                >>> card.__dict__['stopwatch']
                {'startedAt': '2024-9-30T00:00:00Z', 'total': 0}
                ```
        
        Returns:
            Stopwatch: A stopwatch instance used to track time on the card
        """
        self.refresh()

        if not self.stopwatch:
            with self.editor():
                self.stopwatch = {**Stopwatch(startedAt=None, total=0).stop()}
        return self.stopwatch

    def remove_attachment(self, attachment: Attachment) -> Attachment | None:
        """Removes an attachment from the card
        
        Args:
            attachment (Attachment): Attachment instance to remove
            
        Note:
            This method will remove the attachment from the card, but the attachment itself will not be deleted

        Returns:
            Card: The card instance with the attachment removed
        """
        for card_attachment in self.attachments:
            if card_attachment.id == attachment.id:
                return card_attachment.delete()
        return None
    
    def remove_label(self, label: Label) -> Card:
        """Removes a label from the card
        
        Args:
            label (Label): Label instance to remove
            
        Note:
            This method will remove the label from the card, but the label itself will not be deleted

        Returns:
            Card: The card instance with the label removed   
        """
        for card_label in self.board.cardLabels:
            if card_label.cardId == self.id and card_label.labelId == label.id:
                card_label.delete()
        return self

    def remove_member(self, user: User) -> Card:
        """Removes a user from the card
        
        Args:
            user (User): User instance to remove
            
        Note:
            This method will remove the user from the card, but the user itself will not be deleted
            
        Returns:
            Card: The card instance with the user removed
        """
        for card_membership in self.board.cardMemberships:
            if card_membership.cardId == self.id and card_membership.userId == user.id:
                card_membership.delete()
        return self
    
    def remove_comment(self, comment_action: Action) -> Card:
        """Pass a comment from self.comments to remove it
        
        Args:
            comment_action (Action): Comment instance to remove
            
        Note:
            This method will remove the comment from the card, but the comment itself will not be deleted
            
        Returns:
            Card: The card instance with the comment removed
        """
        for comment in self.comments:
            if comment.id == comment_action.id:
                comment.delete()
        return self

    def remove_stopwatch(self) -> Stopwatch:
        """Removes the stopwatch from the card
        
        Returns:
            Stopwatch: The stopwatch instance that was removed
        """
        self.refresh()
        with self.editor():
            _stopwatch = self.stopwatch
            self.stopwatch = None
        return _stopwatch

    # Stopwatch handling is a bit weird, this is a hacky override to always show the user a Stopwatch instance
    def __getattribute__(self, name):
        if name == 'stopwatch':
            current = super().__getattribute__(name)
            if not current:
                current = {'startedAt':None, 'total':0}
            return Stopwatch(_card=self, **current)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'stopwatch' and isinstance(value, Stopwatch):
            super().__setattr__(name, dict(value))
        else:
            super().__setattr__(name, value)

    def set_due_date(self, due_date: datetime  | None) -> Card:
        """Sets the due date of the card
        
        Args:
            dueDate (datetime): Due date of the card (None to remove)
            
        Returns:
            Card: The card instance with the due date set
        """
        with self.editor():
            self.dueDate = due_date.isoformat() if due_date else None
        return self

    @overload
    def update(self) -> Card: ...
    
    @overload
    def update(self, card: Card) -> Card: ...
    
    @overload
    def update(self, name: str, position: int=0, 
                    description: str=None, dueDate: datetime=None,
                    isDueDateCompleted: bool=None,
                    stopwatch: Stopwatch=None, boardId: int=None,
                    listId: int=None, creatorUserId: int=None,
                    coverAttachmentId: int=None, isSubscribed: bool=None) -> Card: ...
    
    def update(self, *args, **kwargs) -> Card:
        """Updates the card with new values
        
        Tip:
            It's recommended to use a `card.editor()` context manager to update the card

            Example:
            ```python
            >>> with card.editor():
            ...    card.name='New Name'

            >>> card
            Card(name='New Name', ...)
            ``

        Args:
            name (str): Name of the card (optional)
            position (int): Position of the card (optional)
            description (str): Description of the card (optional)
            dueDate (datetime): Due date of the card (optional)
            isDueDateCompleted (bool): Whether the due date is completed (optional)
            stopwatch (Stopwatch): Stopwatch of the card (optional)
            boardId (int): Board id of the card (optional)
            listId (int): List id of the card (optional)
            creatorUserId (int): Creator user id of the card (optional)
            coverAttachmentId (int): Cover attachment id of the card (optional)
            isSubscribed (bool): Whether the card is subscribed (optional)
        
        Args: Alternate
            card (Card): Card instance to update (required)
            
        Note:
            If no arguments are provided, the card will update itself with the current values stored in its attributes
        
        Returns:
            Card: Updated card instance
        """
        overload = parse_overload(
            args, kwargs, 
            model='card', 
            options=('name', 'position', 'description', 'dueDate', 
                    'isDueDateCompleted', 'stopwatch', 
                    'creatorUserId', 'coverAttachmentId', 
                    'isSubscribed'), 
            noarg=self)
                
        route = self.routes.patch_card(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def delete(self) -> Card:
        """Deletes the card
        
        Danger:
            This action is irreversible and cannot be undone
            
        Returns:
            Card: The deleted card instance
        """
        self.refresh()
        route = self.routes.delete_card(id=self.id)
        route()
        return self
    
    def refresh(self):
        """Refreshes the card data
        
        Note:
            This method is used to update the card instance with the latest data from the server
        """
        route = self.routes.get_card(id=self.id)
        self.__init__(**route()['item'])
        
class CardLabel(CardLabel_):
    
    @property
    def card(self) -> Card:
        """Card the label is attached to
        
        Returns:
            Card: Card instance
        """
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)
    
    @property
    def board(self) -> Board:
        """Board the card belongs to
        
        Returns:
            Board: Board instance
        """
        board_route = self.routes.get_board(id=self.card.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @property
    def label(self) -> Label:
        """Label attached to the card
        
        Returns:
            Label: Label instance
        """
        for label in self.board.labels:
            if label.id == self.labelId:
                return label

    def delete(self) -> tuple[Card, Label]:
        """Deletes the card label relationship
        
        Danger:
            This action is irreversible and cannot be undone
            
        Returns:
            tuple[Card, Label]: The card and label that were removed from each other
        """
        self.refresh()
        route = self.routes.delete_card_label(cardId=self.card.id, labelId=self.labelId)
        route()
        return (self.card, self.label)
    
class CardMembership(CardMembership_):
    
    @property
    def user(self) -> User:
        """User that is a member of the card
        
        Returns:
            User: User instance
        """
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def card(self) -> Card:
        """Card the user is a member of
        
        Returns:
            Card: Card instance
        """
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)

    def delete(self) -> tuple[User, Card]:
        """Deletes the card membership
        
        Danger:
            This action is irreversible and cannot be undone
            
        Returns:
            tuple[User, Card]: The user and card that were removed from each other
        """
        self.refresh()
        route = self.routes.delete_card_membership(id=self.id)
        route()
        return (self.user, self.card)
    
class CardSubscription(CardSubscription_): 
    
    @property
    def user(self) -> User:
        """User that is subscribed to the card
        
        Returns:
            User: User instance
        """
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def card(self) -> Card:
        """Card the user is subscribed to
        
        Returns:
            Card: Card instance
        """
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)

class IdentityUserProvider(IdentityProviderUser_):
    
    @property
    def user(self) -> User:
        """User that is a member of the identity provider
        
        Returns:
            User: User instance
        """
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)

class List(List_):
    
    @property
    def board(self) -> Board:
        """Board the list belongs to
        
        Returns:
            Board: Board instance
        """
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @property
    def cards(self) -> QueryableList[Card]:
        """All cards in the list
        
        Returns:
            Queryable List of all cards in the list
        """
        return QueryableList([
            card
            for card in self.board.cards
            if card.listId == self.id
        ])
    
    @overload
    def create_card(self, card: Card) -> Card: ...

    @overload
    def create_card(self, name: str, position: int=0, 
                    description: str=None, dueDate: datetime=None,
                    isDueDateCompleted: bool=None,
                    stopwatch: Stopwatch=None, boardId: int=None,
                    listId: int=None, creatorUserId: int=None,
                    coverAttachmentId: int=None, isSubscribed: bool=None) -> Card: ...
    
    def create_card(self, *args, **kwargs) -> Card:
        """Creates a card in the list
        
        Args:
            name (str): Name of the card (required)
            position (int): Position of the card (default: 0)
            description (str): Description of the card (optional)
            dueDate (datetime): Due date of the card (optional)
            isDueDateCompleted (bool): Whether the due date is completed (optional)
            stopwatch (Stopwatch): Stopwatch of the card (optional)
            boardId (int): Board id of the card (optional)
            listId (int): List id of the card (optional)
            creatorUserId (int): Creator user id of the card (optional)
            coverAttachmentId (int): Cover attachment id of the card (optional)
            isSubscribed (bool): Whether the card is subscribed (optional)
            
        Args: Alternate
            card (Card): Card instance to create
            
        Returns:
            Card: New card instance
        """
        overload = parse_overload(
            args, kwargs, 
            model='card', 
            options=('name', 'position', 'description', 'dueDate', 
                    'isDueDateCompleted', 'stopwatch', 
                    'creatorUserId', 'coverAttachmentId', 
                    'isSubscribed'), 
            required=('name',))
        
        overload['boardId'] = self.boardId
        overload['listId'] = self.id
        overload['position'] = overload.get('position', 0)

        route = self.routes.post_card(id=self.id)
        return Card(**route(**overload)['item']).bind(self.routes)

    def _sort(self, sort: SortOption) -> None:
        route = self.routes.post_sort_list(id=self.id)
        route(**{'type': ListSorts[sort]})

    def sort_by_name(self) -> None:
        """Sorts cards in the list by name
        
        Note:
            After sorting, a call to `list.cards` will return a sorted list of cards
        """
        self._sort('Name')
    
    def sort_by_due_date(self) -> None:
        """Sorts cards in the list by due date
        
        Note:
            After sorting, a call to `list.cards` will return a sorted list of cards
        """
        self._sort('Due date')
        
    def sort_by_newest(self) -> None:
        """Sorts cards in the list by newest first
        
        Note:
            After sorting, a call to `list.cards` will return a sorted list of cards
        """
        self._sort('Newest First')
    
    def sort_by_oldest(self) -> None:
        """Sorts cards in the list by oldest first
        
        Note:
            After sorting, a call to `list.cards` will return a sorted list of cards
        """
        self._sort('Oldest First')
    
    def delete(self) -> List:
        """Deletes the list
        
        Danger:
            This action is irreversible and cannot be undone
            
        Returns:
            List: Deleted list instance
        """
        self.refresh()
        route = self.routes.delete_list(id=self.id)
        route()
        return self

    @overload
    def update(self) -> List: ...

    @overload
    def update(self, list: List) -> List: ...

    @overload
    def update(self, name: str=None, position: int=None) -> List: ...

    def update(self, *args, **kwargs) -> List:
        """Updates the list with new values
        
        Tip:
            If you want to update a list, it's better to use the `editor()` context manager

            Example:
            ```python
            >>> with list_.editor():
            ...    list_.name = 'New List Name'
            ...    list_.position = 1

            >>> list
            List(id=1, name='New List Name', position=1, ...)
            ```

        Args:
            name (str): Name of the list (optional)
            position (int): Position of the list (optional)
            
        Args: Alternate
            list (List): List instance to update (required)
            
        Note:
            If no arguments are provided, the list will update itself with the current values stored in its attributes
            
        Returns:
            List: Updated list instance
        """
        overload = parse_overload(
            args, kwargs, 
            model='list', 
            options=('name', 'position'),
            noarg=self)
        
        route = self.routes.patch_list(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self

    def refresh(self) -> None:
        """Refreshes the list data"""
        for _list in self.board.lists:
            if _list.id == self.id:
                self.__init__(**_list)

    def set_color(self, color: ListColors) -> List:
        """Sets the color of the list
        
        Note:
            This method is only available in Planka 2.0.0 and later

        Args:
            color (str): Color of the list
            
        Returns:
            List: The list instance with the color set
        """
        if color not in ListColors.__args__:
            raise ValueError(
                f"Invalid color: {color}\n"
                f"Valid colors: {ListColors.__args__}")
        with self.editor():
            self.color = color
        return self
    
class ProjectManager(ProjectManager_):
    
    @property
    def user(self) -> User:
        """User that is a manager of the project
        
        Returns:
            User: User instance
        """
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def project(self) -> Project:
        """Project the user is a manager of

        Returns:
            Project: Project instance
        """
        project_route = self.routes.get_project(id=self.projectId)
        return Project(**project_route()['item']).bind(self.routes)
    
    def delete(self) -> tuple[User, Project]:
        """Deletes the project manager relationship
        
        Danger:
            This action is irreversible and cannot be undone
            
        Returns:
            tuple[User, Project]: The user and project that the user was manager of
        """
        self.refresh()
        route = self.routes.delete_project_manager(id=self.id)
        route()
        return (self.user, self.project)
     
    def refresh(self) -> None:
        """Refreshes the project manager data"""
        for manager in self.project.managers:
            if manager.id == self.id:
                self.__init__(**manager)

class Task(Task_):
    
    @property
    def card(self) -> Card:
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)
     
    @overload
    def update(self): ...
    
    @overload
    def update(self, task: Task): ...
    
    @overload
    def update(self, name: str=None, isCompleted: bool=None) -> Task: ...

    def update(self, *args, **kwargs) -> Task:
        """Updates the task with new values
        
        Tip:
            If you want to update a task, it's better to use the `editor()` context manager

            Example:
            ```python
            >>> with task.editor():
            ...    task.name = 'New Task Name'
            ...    task.isCompleted = True

            >>> task
            Task(id=1, name='New Task Name', isCompleted=True, ...)
            ```

        Args:
            name (str): Name of the task (optional)
            isCompleted (bool): Whether the task is completed (optional)
            
        Args: Alternate
            task (Task): Task instance to update (required)
        
        Note:
            If no arguments are provided, the task will update itself with the current values stored in its attributes
            
        Returns:
            Task: Updated task instance
        """
        overload = parse_overload(
            args, kwargs, 
            model='task', 
            options=('name', 'isCompleted'),
            noarg=self)
        
        route = self.routes.patch_task(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def delete(self) -> Task:
        """Deletes the task
        
        Danger:
            This action is irreversible and cannot be undone
            
        Returns:
            Task: Deleted task instance
        """
        self.refresh()
        route = self.routes.delete_task(id=self.id)
        route()
        return self
    
    def refresh(self) -> None:
        """Refreshes the task data"""
        tasks = self.card.board.tasks
        for task in tasks:
            if task.id == self.id:
                self.__init__(**task)
