from __future__ import annotations

from typing import Type, overload
from datetime import datetime


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
)
from .handlers import (
    TokenAuth, 
    PasswordAuth, 
    BaseAuth, 
    JSONHandler,
)

from .constants import (
    Gradient,
    LabelColor,
    ActionType,
    BoardRole,
    Background,
    BackgroundImage,
    get_position,
    set_position,
    SortOption,
    ListSorts,
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
        board = Board(name='My Board', position=0)
        board.name = 'My New Board'
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
    elif args and not kwargs:
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
        All implemented public properties return API responses with accessed. This means that the values are not cached 
        and will be updated on every access. If you wish to cache values, you are responsible for doing so. By default, 
        property access will always provide the most up to date information.
        
        Example:
            ```python
            len(project.cards)
            >>> 5
            project.create_card('My Card')
            len(project.cards)
            >>> 6
            ```

    Example:
        ```python
        from plankapy import Planka, PasswordAuth

        auth = PasswordAuth('username', 'password')
        planka = Planka('https://planka.example.com', auth)

        planka.me
        >>> User(id=...9234, name='username', ...)
        ```
    
    Tip:
        If you want to store a property chain to update later, but dont want to call it by full name, you can use a lambda

        Example:
            ```python
            card = lambda: planka.project[0].boards[0].lists[0].cards[0]
            comments = lambda: card().comments
            len(comments())
            >>> 2
            card().add_comment('My Comment')
            len(comments())
            >>> 3
            ```
    
    Tip:
        All objects inherit the `editor` context manager from the `Model` class except `Planka`.
        This means if you want to make changes to something, you can do it directly to attributes
        in an editor context instead of calling the model's `update` method

        Example:
            ```python
            with card.editor():
                card.name = 'My New Card'
                card.description = 'My New Description'
            ```
    """
    def __init__(self, url: str, auth: Type[BaseAuth]):        
        self._url = url
        self._auth = auth
        self._create_session()

    def _create_session(self) -> None:
        """INTERNAL: Creates a new session with the current authentication method and url"""
        self.handler = JSONHandler(self.url)
        self.handler.headers['Authorization'] = self.auth.authenticate(self.url)
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
            planka.auth = TokenAuth('<new_token>')
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
            planka.url = 'https://planka.example.com'
            ```
        """
        self._url = url
        self._create_session(self.auth)

    @property
    def projects(self) -> list[Project]:
        """List of all projects on the Planka instance
        
        Returns:
            List of all projects
        """
        route = self.routes.get_project_index()
        return [
            Project(**project).bind(self.routes)
            for project in route()['items']
        ]
    
    @property
    def users(self) -> list[User]:
        """List of all users on the Planka instance
        
        Returns:
            List of all users
        """
        route = self.routes.get_user_index()
        return [
            User(**user).bind(self.routes)
            for user in route()['items']
        ]
    
    @property
    def notifications(self) -> list[Notification]:
        """List of all notifications for the current user
        
        Returns:
            List of all notifications
        """
        route = self.routes.get_notification_index()
        return [
            Notification(**notification).bind(self.routes)
            for notification in route()['items']
        ]
    
    @property
    def project_background_images(self, NOT_IMPLEMENTED) -> list[BackgroundImage]:
        """Get Project Background Images
        
        Attention:
            Requires client side rendering, not currently supported
        
        Raises:
            NotImplementedError
        """
        raise NotImplementedError('Getting project backgrounds is not currently supported by plankapy')

    @property
    def user_avatars(self, NOT_IMPLEMENTED) -> list[str]:
        """Get User Avatars

        Attention:
            Requires client side rendering, not currently supported
        
        Raises:
            NotImplementedError
        """
        raise NotImplementedError('Getting user avatars is not currently supported by plankapy')

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
            This method has overloaded arguments, 
            You can pass a `Project` instance or provide a required `name` argument

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
            new_project = planka.create_project('My Project')
            new_project.set_background_gradient('blue-xchange') # Set background gradient
            new_project.add_project_manager(planka.me) # Add current user as project manager
            ```
        """
        overload = parse_overload(args, kwargs, model='project', 
                                  options=('name', 'position', 'background', 'backgroundImage'), 
                                  required=('name',))

        overload['position'] = overload.get('position', 0)
        
        if 'background' in overload: # Convert gradient to expected format
            overload['background'] = {'name': overload['background'], 'type': 'gradient'}

        route = self.routes.post_project()
        return Project(**route(**overload)['item']).bind(self.routes)
        
    def create_user(self, username: str, email: str, password: str, name: str=None) -> User:
        """Create a new user

        Danger:
            Supplied password must be moderately secure or a 400 error will be raised

        Args:
            username: Will assign username to `name` and `username`
            email: 
            password: Must be moderately secure or will raise a 400 error!
            name: The full name of the user (default: `username` value)
        """
        route = self.routes.post_user()
        return User(**route(username=username, name=name or username, password=password, email=email)['item']).bind(self.routes)

class Project(Project_):
    """Interface for interacting with planka Projects and their included sub-objects
    
    Note:
        All implemented public properties return API responses with accessed. This means that the values are not cached 
        and will be updated on every access. If you wish to cache values, you are responsible for doing so. By default, 
        property access will always provide the most up to date information.
    """
    @property
    def _included(self) -> JSONHandler.JSONResponse:
        """Included data for the project
        
        Warning:
            This property is meant to be used internally for building objects in the other proeprties
            It can be directly accessed, but it will only return JSON data and not objects
        
        Returns:
            Included data for the project
        """
        route = self.routes.get_project(id=self.id)
        return route()['included']
    
    @property
    def users(self) -> list[User]:
        """All users in the project
        
        Returns:
            List of all users
        """
        return [
            User(**user).bind(self.routes)
            for user in self._included['users']
        ]
    
    @property
    def managers(self) -> list[ProjectManager]:
        """All project managers
        
        Returns:
            List of all project managers
        """
        return [
            ProjectManager(**projectManager).bind(self.routes)
            for projectManager in self._included['projectManagers']
        ]
    
    @property
    def boardMemberships(self) -> list[BoardMembership]:
        """All board memberships and roles in the project
        
        Note:
            This property is not a list of users, but a list of `BoardMembership` objects
            that define the user's role in the project boards. This is used to remove memberships
            in associated project boards and will likely never be used directly
        
        Returns:
            List of all board membership relations in the project    
        """
        return [
            BoardMembership(**boardMembership).bind(self.routes)
            for boardMembership in self._included['boardMemberships']
        ]

    @property
    def boards(self) -> list[Board]:
        """All boards in the project
        
        Returns:
            List of all boards
        """
        return [
            Board(**board).bind(self.routes)
            for board in self._included['boards']
        ]
    
    @overload
    def create_board(self, board: Board) -> Board: ...

    @overload
    def create_board(self, name: str, position: int=0) -> Board: ...

    def create_board(self, *args, **kwargs) -> Board:
        """Creates a new board in the project from a name and position or a Board instance
        
        Args:
            name (str): Name of the board
            position (int): Position of the board (default: 0)
            
        Args: Alterate
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
            new_manager = project.create_project_manager(planka.me)
            other_manager = project.create_project_manager(userId='...1234')
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
    def remove_project_manager(project_manager: User) -> User: ...

    @overload
    def remove_project_manager(userId: int) -> User: ...

    def remove_project_manager(self, *args, **kwargs) -> User:
        overload = parse_overload(args, kwargs,
                                  model='user',
                                  options=('userId',),
                                  required=('userId',)
        )
        
        if 'userId' not in overload: # Case for User object
            overload['userId'] = overload['id']
        
        for manager in self.managers:
            if manager.userId == overload['userId']:
                manager.delete()

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
    def update(self, name: str=None, background: Gradient=None, 
               backgroundImage: BackgroundImage=None) -> Project: ...

    def update(self, *args, **kwargs) -> Project:
        """Updates the project with new values
            
        Args:
            name (str): Name of the project (required)
            background (Gradient): Background gradient of the project (default: None)
            backgroundImage (BackgroundImage): Background image of the project (default: None)
        

        Args: Alternate
            project (Project): Project instance to update (required)
        
        Returns:
            Project: Updated project instance

        Example:
            ```python
            project.update(name='My New Project', background='blue-xchange'))
            ```
        """
        overload = parse_overload(args, kwargs, model='project', 
                                  options=('name', 'background', 'backgroundImage'),
                                  noarg=self)
        
        if 'background' in overload:
            overload['background'] = {'name': overload['background'], 'type': 'gradient'}

        route = self.routes.patch_project(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self

    def set_background_gradient(self, gradient: Gradient) -> None:
        """Set a background gradient for the project
        See Also:
            [Gradient][plankapy.constants.Gradient]: For available gradients
        
        Args:
            gradient (Gradient): Background gradient to set
        
        Example:
            ```python
            project.set_background_gradient('blue-xchange')
            ```
        """
        self.update(background=gradient)

    def set_background_image(self, image: BackgroundImage) -> None:
        """Set a background image for the project
        
        Warning:
            This method is not currently supported by plankapy

        Args:
            image (BackgroundImage): Background image to set
        
        Raises:
            NotImplementedError: Setting background images is not currently supported by plankapy
        """
        raise NotImplementedError('setting project background images is not currently supported by plankapy')

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
    @property
    def _included(self) -> JSONHandler.JSONResponse:
        """Included data for the board
        
        Warning:
            This property is meant to be used internally for building objects in the other proeprties
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
    def users(self) -> list[User]:
        """All users in the board

        Returns:
            List of all users
        """
        return [
            User(**user).bind(self.routes)
            for user in self._included['users']
        ]
    
    @property
    def editors(self) -> list[User]:
        """All users that can edit the board

        Returns:
            List of all editors
        """
        return [
            user
            for user in self.users
            for boardMembership in self.boardMemberships
            if boardMembership.userId == user.id and boardMembership.canComment
        ]
    
    @property
    def viewers(self) -> list[User]:
        """All users that can view the board
        
        Returns:
            List of all viewers
        """
        return [
            user
            for user in self.users
            for boardMembership in self.boardMemberships
            if boardMembership.userId == user.id and not boardMembership.canComment
        ]
    
    @property
    def boardMemberships(self) -> list[BoardMembership]:
        """All board memberships
        
        Note:
            This property is primarily here for internal use, '.editor' and '.viewer' properties 
            are derived from the board memberships

        Returns:
            List of all membership types (editor, viewer)
        """
        return [
            BoardMembership(**boardMembership).bind(self.routes)
            for boardMembership in self._included['boardMemberships']
        ]
    
    @property
    def labels(self) -> list[Label]:
        """All labels in the board
        
        Returns:
            List of all labels in the board
        """
        return [
            Label(**label).bind(self.routes)
            for label in self._included['labels']
        ]
    
    @property
    def lists(self) -> list[List]:
        """All lists in the board
        
        Returns:
            List of all lists in the board
        """
        return [
            List(**_list).bind(self.routes)
            for _list in self._included['lists']
        ]
    
    @property
    def cards(self) -> list[Card]:
        """All cards in the board
        
        Returns:
            A list of all cards in the board
        """
        return [
            Card(**card).bind(self.routes)
            for card in self._included['cards']
        ]
    
    @property
    def cardMemberships(self) -> list[CardMembership]:
        """All card -> user relationships in the board
        
        Note:
            This property is used by the `Card` class to determine its users

        Returns:
            A list of all card memberships in the board
        """
        return [
            CardMembership(**cardMembership).bind(self.routes)
            for cardMembership in self._included['cardMemberships']
        ]
    
    @property
    def cardLabels(self) -> list[CardLabel]:
        """All card -> label relationships in the board
        
        Note:
            This property is used by the `Card` class to determine its labels

        Returns:
            A list of all card labels in the board
        """
        return [
            CardLabel(**cardLabel).bind(self.routes)
            for cardLabel in self._included['cardLabels']
        ]
    
    @property
    def tasks(self) -> list[Task]:
        """All tasks in the board
        
        Note:
            This property is used by the `Card` class to determine its tasks

        Returns:
            A list of all card tasks in the board
        """
        return [
            Task(**task).bind(self.routes)
            for task in self._included['tasks']
        ]
    
    @property
    def attachments(self) -> list[Attachment]:
        """All attachments in the board
        
        Note:
            This property is used by the `Card` class to determine its attachments
            
        Returns:
            A list of all card attachments in the board
        """
        return [
            Attachment(**attachment).bind(self.routes)
            for attachment in self._included['attachments']
        ]

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
            new_list = board.create_list('My List')

            l = List(name='My List', position=0)
            new_list2 = board.create_list(l)
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
            new_label = board.create_label('My Label')
            label = Label(name='My Label', position=0, color='wet-moss')
            new_label2 = board.create_label(label)
            ```
        """
        overload = parse_overload(args, kwargs, model='label', 
                                  options=('name', 'position', 'color'), 
                                  required=('name',)) # Only name requires user provided value
        
        # Required arguments with defaults must be manually assigned
        overload['position'] = overload.get('position', 0)
        overload['color'] = overload.get('color', LabelColor.__args__[0])
        overload['boardId'] = self.id

        route = self.routes.post_label(boardId=self.id)
        return Label(**route(**overload)['item']).bind(self.routes)

    def add_user(self, user: User, canComment: bool=False) -> BoardMembership:
        """Adds a user to the board
        
        Args:
            user (User): User instance to add
            canComment (bool): Whether the user can comment on the board (default: False)
        
        Returns:
            BoardMembership: New board membership
        """
        role = 'editor' if canComment else 'viewer'
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
    def projects(self) -> list[Project]:
        """All projects the user is a member of
        
        Returns:
            List of all projects the user is a member of
        """
        projects_route = self.routes.get_project_index()
        projects = [
            Project(**project).bind(self.routes)
            for project in projects_route()['items']
        ]
        return [
            project
            for project in projects
            for user in project.users
            if user.id == self.id
        ]
    
    @property
    def boards(self) -> list[Board]:
        """All boards the user is a member of
        
        Returns:
            List of all boards the user is a member of
        """
        return [
            boardMembership.board
            for project in self.projects
            for boardMembership in project.boardMemberships
            if boardMembership.userId == self.id
        ]
    
    @property
    def cards(self) -> list[Card]:
        """All cards assigned to the user in all projects
        
        Returns:
            List of all cards assigned to the user
        """
        return [
            cardMembership.card
            for board in self.boards
            for cardMembership in board.cardMemberships
            if cardMembership.userId == self.id
        ]
    
    @property
    def manager_of(self) -> list[Project]:
        """All projects the user is a manager of
        
        Returns:
            List of all projects the user is a manager of
        """
        return [
            project
            for project in self.projects
            for manager in project.managers
            if manager.userId == self.id
        ]
    
    @property
    def notifications(self) -> list[Notification]:
        """All notifications for the user
        
        Returns:
            List of all notifications for the user
        """
        route = self.routes.get_notification_index()
        return [
            Notification(**notification).bind(self.routes)
            for notification in route()['items']
            if notification['userId'] == self.id
        ]
    
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
    
    @property
    def user(self) -> User:
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def action(self) -> Action:
        action_route = self.routes.get_action(id=self.actionId)
        return Action(**action_route()['item']).bind(self.routes)
    
    @property
    def card(self) -> Card:
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)
    
    @overload
    def update(self): ...
    
    @overload
    def update(self, notification: Notification): ...
    
    @overload
    def update(self, isRead: bool=None): ...
    
    def update(self, *args, **kwargs) -> Notification:
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
        """
        self.update(isRead=True)
    
    def refresh(self) -> None:
        """Refreshes the notification data"""
        route = self.routes.get_notification(id=self.id)
        self.__init__(**route()['item'])

class BoardMembership(BoardMembership_):
    
    @property
    def user(self) -> User:
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def board(self) -> Board:
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @overload
    def update(self): ...
    
    @overload
    def update(self, boardMembership: BoardMembership): ...
    
    @overload
    def update(self, role: BoardRole=None, canComment: bool=None): ...
    
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
    
    def update(self, *args, **kwargs) -> BoardMembership:
        overload = parse_overload(
            args, kwargs, 
            model='boardMembership', 
            options=('role', 'canComment'),
            noarg=self)
        
        route = self.routes.patch_board_membership(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def refresh(self) -> None:
        """Refreshes the board membership data"""
        for membership in self.board.boardMemberships:
            if membership.id == self.id:
                self.__init__(**membership)
    
class Label(Label_):
    
    @property
    def board(self) -> Board:
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @property
    def cards(self) -> list[Card]:
        return [
            cardLabel.card
            for cardLabel in self.board.cardLabels
            if cardLabel.labelId == self.id
        ]
    
    @overload
    def update(self) -> Label: ...
    
    @overload
    def update(self, label: Label) -> Label: ...
    
    @overload
    def update(self, name: str=None, color: LabelColor=None, position: int=None) -> Label: ...
    
    def update(self, *args, **kwargs) -> Label:
        overload = parse_overload(
            args, kwargs, 
            model='label', 
            options=('name', 'color', 'position'),
            noarg=self)
              
        route = self.routes.patch_label(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
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
        user_route = self.routes.get_user(id=self.creatorUserId)
        return User(**user_route()['item']).bind(self.routes)
    
class Card(Card_):
    
    @property
    def creator(self) -> User:
        user_route = self.routes.get_user(id=self.creatorUserId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def board(self) -> Board:
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @property
    def list(self) -> List:
        for list in self.board.lists:
            if list.id == self.listId:
                return list
    
    @property
    def labels(self) -> list[Label]:
        return [
            cardLabel.label
            for cardLabel in self.board.cardLabels
            if cardLabel.cardId == self.id
        ]
        
    @property
    def members(self) -> list[User]:
        return [
            cardMembership.user
            for cardMembership in self.board.cardMemberships
            if cardMembership.cardId == self.id
        ]
      
    @property
    def comments(self) -> list[Action]:
        route = self.routes.get_action_index(cardId=self.id)
        return [
            Action(**action).bind(self.routes)
            for action in route()['items']
        ]
    
    @property
    def tasks(self) -> list[Task]:
        return [
            task
            for task in self.board.tasks
            if task.cardId == self.id
        ]
    
    def move(self, list: List) -> Card:
        listId = list.id
        self.listId = listId
        self.update()
    
    def duplicate(self) -> Card:
        route = self.routes.post_duplicate_card(id=self.id)
        return Card(**route(**self)['item']).bind(self.routes)
    
    def add_label(self, label: Label) -> CardLabel:
        route = self.routes.post_card_label(cardId=self.id)
        return CardLabel(**route(labelId=label.id, cardId=self.id)['item']).bind(self.routes)

    def add_member(self, user: User) -> CardMembership:
        route = self.routes.post_card_membership(cardId=self.id)
        return CardMembership(**route(userId=user.id, cardId=self.id)['item']).bind(self.routes)
    
    def add_comment(self, comment: str) -> Action:
        route = self.routes.post_comment_action(cardId=self.id)        
        return Action(**route(text=comment, cardId=self.id)['item']).bind(self.routes)

    @overload
    def add_task(self, task: Task) -> Task: ...

    @overload
    def add_task(self, name: str, position: int=0, 
                 isCompleted: bool=False, isDeleted: bool=False) -> Task: ...
        
    def add_task(self, *args, **kwargs) -> Task:
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

    def add_stopwatch(self) -> None:
        """Adds a stopwatch to the card"""
        self.refresh()

        if self.stopwatch:
            return
        
        with self.editor():
            self.stopwatch = {**Stopwatch(startedAt=None, total=0).stop()}

    def remove_label(self, label: Label) -> None:
        """Removes a label from the card, does not delete the label"""
        for card_label in self.board.cardLabels:
            if card_label.cardId == self.id and card_label.labelId == label.id:
                card_label.delete()

    def remove_member(self, user: User) -> None:
        for card_membership in self.board.cardMemberships:
            if card_membership.cardId == self.id and card_membership.userId == user.id:
                card_membership.delete()
    
    def remove_comment(self, comment_action: Action) -> None:
        """Pass a comment from self.comments to remove it"""
        for comment in self.comments:
            if comment.id == comment_action.id:
                comment.delete()

    def remove_stopwatch(self) -> None:
        """Removes the stopwatch from the card"""
        self.refresh()
        with self.editor():
            self.stopwatch = None

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
        route = self.routes.get_card(id=self.id)
        self.__init__(**route()['item'])
        
class CardLabel(CardLabel_):
    
    @property
    def card(self) -> Card:
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)
    
    @property
    def board(self) -> Board:
        board_route = self.routes.get_board(id=self.card.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @property
    def label(self) -> Label:
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
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def card(self) -> Card:
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
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def card(self) -> Card:
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)

class IdentityUserProvider(IdentityProviderUser_):
    
    @property
    def user(self) -> User:
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)

class List(List_):
    
    @property
    def board(self) -> Board:
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @property
    def cards(self) -> list[Card]:
        return [
            card
            for card in self.board.cards
            if card.listId == self.id
        ]
    
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
        overload = parse_overload(
            args, kwargs, 
            model='card', 
            options=('name', 'position', 'description', 'dueDate', 
                    'isDueDateCompleted', 'stopwatch', 
                    'creatorUserId', 'coverAttachmentId', 
                    'isSubscribed'), 
            required=('name',),
            noarg=self)
        
        overload['boardId'] = self.boardId
        overload['listId'] = self.id
        overload['position'] = overload.get('position', 0)

        route = self.routes.post_card(id=self.id)
        return Card(**route(**overload)['item']).bind(self.routes)

    def _sort(self, sort: SortOption) -> None:
        route = self.routes.post_sort_list(id=self.id)
        route(**{'type': ListSorts[sort]})

    def sort_by_name(self) -> None:
        self._sort('Name')
    
    def sort_by_due_date(self) -> None:
        self._sort('Due date')
        
    def sort_by_newest(self) -> None:
        self._sort('Newest First')
    
    def sort_by_oldest(self) -> None:
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
    def update(self, _list: List) -> List: ...

    @overload
    def update(self, name: str=None, position: int=None) -> List: ...

    def update(self, *args, **kwargs) -> List:
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

class ProjectManager(ProjectManager_):
    
    @property
    def user(self) -> User:
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def project(self) -> Project:
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
