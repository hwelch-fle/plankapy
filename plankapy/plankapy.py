from __future__ import annotations

import sys
sys.path.append('..')

from typing import overload
from datetime import datetime
from urllib.error import HTTPError

from utils.routes import Routes
from utils.models import (
    Model,
    _Action,
    _Archive,
    _Attachment,
    _Board,
    _BoardMembership,
    _Card,
    _Stopwatch,
    _CardLabel,
    _CardMembership,
    _CardSubscription,
    _IdentityProviderUser,
    _Label,
    _List,
    _Notification,
    _Project,
    _ProjectManager,
    _Task,
    _User,
)
from utils.handlers import (
    TokenAuth, 
    PasswordAuth, 
    BaseAuth, 
    JSONHandler,
)

from utils.constants import (
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

    Examples:
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
    def __init__(self, url: str, auth: BaseAuth=None):
        if not auth:
            raise ValueError('No authentication method provided')
        
        self._url = url
        self._auth = auth
        self._create_session()

    def _create_session(self) -> None:
        self.handler = JSONHandler(self.url)
        self.handler.headers['Authorization'] = self.auth.authenticate(self.url)
        self.routes = Routes(self.handler)
    
    @property
    def auth(self) -> BaseAuth:
        return self._auth

    @auth.setter
    def auth(self, auth: BaseAuth):
        self._auth = auth
        self._create_session()

    @property
    def url(self) -> str:
        return self._url
    
    @url.setter
    def url(self, url: str):
        self._url = url
        self._create_session(self.auth)

    @property
    def projects(self) -> list[Project]:
        route = self.routes.get_project_index()
        return [
            Project(**project).bind(self.routes)
            for project in route()['items']
        ]
    
    @property
    def users(self) -> list[User]:
        route = self.routes.get_user_index()
        return [
            User(**user).bind(self.routes)
            for user in route()['items']
        ]
    
    @property
    def notifications(self) -> list[Notification]:
        route = self.routes.get_notification_index()
        return [
            Notification(**notification).bind(self.routes)
            for notification in route()['items']
        ]
    
    @property
    def project_background_images(self, NOT_IMPLEMENTED) -> list[BackgroundImage]:
        raise NotImplementedError('Getting project backgrounds is not currently supported by plankapy')

    @property
    def user_avatars(self, NOT_IMPLEMENTED) -> list[str]:
        raise NotImplementedError('Getting user avatars is not currently supported by plankapy')

    @property
    def me(self) -> User:
        route = self.routes.get_me()
        return User(**route()['item']).bind(self.routes)

    @property
    def config(self) -> JSONHandler.JSONResponse:
        route = self.routes.get_config()
        return route()['item']
    
    @overload
    def create_project(self, project: Project) -> Project: ...

    @overload
    def create_project(self, name: str, position: int=None, 
                       background: Gradient=None) -> Project: ...

    def create_project(self, *args, **kwargs) -> Project:
        overload = parse_overload(args, kwargs, model='project', 
                                  options=('name', 'position', 'background', 'backgroundImage'), 
                                  required=('name',))

        overload['position'] = set_position(overload.get('position', 0))
        if 'background' in overload:
            overload['background'] = {'name': overload['background'], 'type': 'gradient'}

        route = self.routes.post_project()
        return Project(**route(**overload)['item']).bind(self.routes)

class Project(_Project):
    
    @property
    def included(self) -> JSONHandler.JSONResponse:
        route = self.routes.get_project(id=self.id)
        return route()['included']
    
    @property
    def users(self) -> list[User]:
        return [
            User(**user).bind(self.routes)
            for user in self.included['users']
        ]
    
    @property
    def projectManagers(self) -> list[ProjectManager]:
        return [
            ProjectManager(**projectManager).bind(self.routes)
            for projectManager in self.included['projectManagers']
        ]
    
    @property
    def boardMemberships(self) -> list[BoardMembership]:
        return [
            BoardMembership(**boardMembership).bind(self.routes)
            for boardMembership in self.included['boardMemberships']
        ]

    @property
    def boards(self) -> list[Board]:
        return [
            Board(**board).bind(self.routes)
            for board in self.included['boards']
        ]
    
    @overload
    def create_board(self, board: Board) -> Board: ...

    @overload
    def create_board(self, name: str, position: int) -> Board: ...

    def create_board(self, *args, **kwargs) -> Board:
        overload = parse_overload(
            args, kwargs, 
            model='board', 
            options=('name', 'position'), 
            required=('name', 'position'))
        name = overload.get('name')
        position = overload.get('position')

        route = self.routes.post_board(projectId=self.id)
        board = Board(name=name, position=set_position(position), projectId=self.id)
        return Board(**route(**board)['item']).bind(self.routes)

    @overload
    def create_project_manager(self, user: User) -> ProjectManager: ...

    @overload
    def create_project_manager(self, userId: int) -> ProjectManager: ...

    def create_project_manager(self, *args, **kwargs) -> ProjectManager:
        overload = parse_overload(
            args, kwargs, 
            model='user', 
            options=('UserId',), 
            required=('userId',))
        userId = overload.get('userId')

        route = self.routes.post_project_manager(projectId=self.id)
        projectManager = ProjectManager(userId=userId, projectId=self.id)
        return ProjectManager(**route(**projectManager)['item']).bind(self.routes)

    def delete(self) -> None:
        """Deletes the project CANNOT BE UNDONE"""
        route = self.routes.delete_project(id=self.id)
        route()

    @overload
    def update(self, project: Project) -> Project: ...

    @overload
    def update(self, name: str=None, background: Background=None, 
               backgroundImage: BackgroundImage=None) -> Project: ...

    def update(self, *args, **kwargs) -> Project:
        overload = parse_overload(args, kwargs, model='project', 
                                  options=('name', 'background', 'backgroundImage'),
                                  noarg=self)

        route = self.routes.patch_project(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self

    def set_background_gradient(self, gradient: Gradient) -> None:
        self.update(background={'name': gradient, 'type': 'gradient'})

    def set_background_image(self, image: BackgroundImage) -> None:
        raise NotImplementedError('setting project background images is not currently supported by plankapy')

    def refresh(self) -> Project:
        """Refreshes the project data"""
        route = self.routes.get_project(id=self.id)
        try:
            self.__init__(**route()['item'])
        except HTTPError:
            raise ValueError(f'Project {self.name} with id({self.id}) not found, it was likely deleted')

class Board(_Board):

    @property
    def included(self) -> JSONHandler.JSONResponse:
        route = self.routes.get_board(id=self.id)
        return route()['included']
    
    @property
    def users(self) -> list[User]:
        return [
            User(**user).bind(self.routes)
            for user in self.included['users']
        ]
    
    @property
    def boardMemberships(self) -> list[BoardMembership]:
        return [
            BoardMembership(**boardMembership).bind(self.routes)
            for boardMembership in self.included['boardMemberships']
        ]
    
    @property
    def labels(self) -> list[Label]:
        return [
            Label(**label).bind(self.routes)
            for label in self.included['labels']
        ]
    
    @property
    def lists(self) -> list[List]:
        return [
            List(**_list).bind(self.routes)
            for _list in self.included['lists']
        ]
    
    @property
    def cards(self) -> list[Card]:
        return [
            Card(**card).bind(self.routes)
            for card in self.included['cards']
        ]
    
    @property
    def cardMemberships(self) -> list[CardMembership]:
        return [
            CardMembership(**cardMembership).bind(self.routes)
            for cardMembership in self.included['cardMemberships']
        ]
    
    @property
    def cardLabels(self) -> list[CardLabel]:
        return [
            CardLabel(**cardLabel).bind(self.routes)
            for cardLabel in self.included['cardLabels']
        ]
    
    @property
    def tasks(self) -> list[Task]:
        return [
            Task(**task).bind(self.routes)
            for task in self.included['tasks']
        ]
    
    @property
    def attachments(self) -> list[Attachment]:
        return [
            Attachment(**attachment).bind(self.routes)
            for attachment in self.included['attachments']
        ]
    
    @property
    def projects(self) -> list[Project]:
        return [
            Project(**project).bind(self.routes)
            for project in self.included['projects']
        ]

    @overload
    def create_list(self, _list: List) -> List: ...

    @overload
    def create_list(self, name: str, position: int) -> List: ...

    def create_list(self, *args, **kwargs) -> List:
        overload = parse_overload(args, kwargs, model='list', 
                                  options=('name', 'position'), 
                                  required=('name', 'position'))
        name = overload.get('name')
        position = overload.get('position')

        route = self.routes.post_list(boardId=self.id)
        _list = List(name=name, position=set_position(position), boardId=self.id)
        return List(**route(**_list)['item']).bind(self.routes)
    
    @overload
    def create_label(self, label: Label) -> Label: ...

    @overload
    def create_label(self, name: str, position: int, color: LabelColor) -> Label: ...

    def create_label(self, *args, **kwargs) -> Label:
        overload = parse_overload(args, kwargs, model='label', 
                                  options=('name', 'position', 'color'), 
                                  required=('name', 'position', 'color'))
        name = overload.get('name')
        color = overload.get('color')
        position = set_position(overload.get('position'))

        route = self.routes.post_label(boardId=self.id)
        label = Label(name=name, position=position, color=color, boardId=self.id)
        return Label(**route(**label)['item']).bind(self.routes)

    def delete(self) -> None:
        """Deletes the board CANNOT BE UNDONE"""
        route = self.routes.delete_board(id=self.id)
        route()

    @overload
    def update(self) -> Board: ...

    @overload
    def update(self, board: Board) -> Board: ...

    @overload
    def update(self, name: str=None, position: int=None) -> Board: ...

    def update(self, *args, **kwargs) -> Board:
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
        try:
            self.__init__(**route()['item'])
        except HTTPError:
            raise ValueError(f'Board {self.name} with id({self.id}) not found, it was likely deleted')

class User(_User):
    """User properties traverse the whole instance and are thereby very slow
    To get membership information, it is recommended to get the data from individual projects, boards, and cards"""
    @property
    def projects(self) -> list[Project]:
        """Returns a list of all projects the user is a member of"""
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
        """Returns a list of all boards the user is a member of"""
        return [
            boardMembership.board
            for project in self.projects
            for boardMembership in project.boardMemberships
            if boardMembership.userId == self.id
        ]
    
    @property
    def cards(self) -> list[Card]:
        """Returns a list of all cards assigned to the user in all projects"""
        return [
            cardMembership.card
            for board in self.boards
            for cardMembership in board.cardMemberships
            if cardMembership.userId == self.id
        ]
    
    @property
    def manager_of(self) -> list[Project]:
        """Returns a list of all projects the user is a manager of"""
        return [
            project
            for project in self.projects
            for manager in project.managers
            if manager.userId == self.id
        ]
    
    @property
    def notifications(self) -> list[Notification]:
        """Returns a list of all notifications for the user"""
        route = self.routes.get_notification_index()
        notifications = [
            Notification(**notification).bind(self.routes)
            for notification in route()['items']
        ]
        return [
            notification
            for notification in notifications
            if notification.userId == self.id
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
    
    def delete(self) -> None:
        """Deletes the user CANNOT BE UNDONE"""
        route = self.routes.delete_user(id=self.id)
        route()
    
    def refresh(self) -> None:
        """Refreshes the user data"""
        route = self.routes.get_user(id=self.id)
        try:
            self.__init__(**route()['item'])
        except HTTPError:
            raise ValueError(f'User {self.name} with id({self.id}) not found, it was likely deleted')

class Notification(_Notification):
    
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
    
    def delete(self) -> None:
        """Notifications can't be deleted, but they can be marked as read"""
        self.update(isRead=True)
    
    def refresh(self) -> None:
        """Refreshes the notification data"""
        route = self.routes.get_notification(id=self.id)
        try:
            self.__init__(**route()['item'])
        except HTTPError:
            raise ValueError(f'Notification with id({self.id}) not found, it was likely deleted')

class BoardMembership(_BoardMembership):
    
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
    
    def delete(self) -> None:
        """Deletes the board membership CANNOT BE UNDONE"""
        route = self.routes.delete_board_membership(id=self.id)
        route()
    
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
                return
        raise ValueError(f'Board Membership with id({self.id}) not found, it was likely deleted')
    
class Label(_Label):
    
    @property
    def board(self) -> Board:
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
    @property
    def labeledCards(self) -> list[Card]:
        return [
            cardLabel.card
            for cardLabel in self.board.cardLabels
            if cardLabel.labelId == self.id
        ]
    
    @property
    def integer_position(self) -> int:
        return get_position(self.position)
    
    @integer_position.setter
    def integer_position(self, value: int):
        self.position = set_position(value)
        self.update()
    
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
        
        if 'position' in overload:
            overload['position'] = set_position(overload['position'])
        
        route = self.routes.patch_label(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def delete(self) -> None:
        """Deletes the label CANNOT BE UNDONE"""
        route = self.routes.delete_label(id=self.id)
        route()
        
    def refresh(self) -> None:
        """Refreshes the label data"""
        for label in self.board.labels:
            if label.id == self.id:
                self.__init__(**label)
                return
        raise ValueError(f'Label: {self.name} with id({self.id}) not found, it was likely deleted')

class Action(_Action): 
    
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
    def update(self, data: dict=None, type: ActionType=None): ...
    
    def update(self, *args, **kwargs) -> Action:
        overload = parse_overload(
            args, kwargs, 
            model='action', 
            options=('data', 'type'),
            noarg=self)
        
        route = self.routes.patch_action(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self
    
    def refresh(self) -> None:
        """Refreshes the action data"""
        for action in self.card.actions:
            if action.id == self.id:
                self.__init__(**action)
                return
        raise ValueError(f'Action with id({self.id}) not found, it was likely deleted')

class Archive(_Archive): ...

class Attachment(_Attachment):
    
    @property
    def creator(self) -> User:
        user_route = self.routes.get_user(id=self.creatorUserid)
        return User(**user_route()['item']).bind(self.routes)
    
    

class Card(_Card):
    
    @property
    def list(self) -> List:
        list_route = self.routes.get_list(id=self.listId)
        return List(**list_route()['item']).bind(self.routes)
    
    @property
    def creator(self) -> User:
        user_route = self.routes.get_user(id=self.creatorUserId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def board(self) -> Board:
        board_route = self.routes.get_board(id=self.boardId)
        return Board(**board_route()['item']).bind(self.routes)
    
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
    
    @ property
    def subcribers(self) -> list[User]:
        return [
            subscription
            for subscription in self.board.cardMemberships
            if subscription.cardId == self.id
        ]
    
    @property
    def coverAttachment(self) -> Attachment:
        if self.coverAttachmentId:
            attachment_route = self.routes.get_attachment(id=self.coverAttachmentId)
            return Attachment(**attachment_route()['item']).bind(self.routes)
        return None
        
class CardLabel(_CardLabel):
    
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
        raise ValueError(f'Label with id({self.labelId}) not found, it was likely deleted')

class CardMembership(_CardMembership):
    
    @property
    def user(self) -> User:
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def card(self) -> Card:
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)

class CardSubscription(_CardSubscription): 
    
    @property
    def user(self) -> User:
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)
    
    @property
    def card(self) -> Card:
        card_route = self.routes.get_card(id=self.cardId)
        return Card(**card_route()['item']).bind(self.routes)

class IdentityUserProvider(_IdentityProviderUser):
    
    @property
    def user(self) -> User:
        user_route = self.routes.get_user(id=self.userId)
        return User(**user_route()['item']).bind(self.routes)

class List(_List):
    
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
    def create_card(self, name: str, position: int, 
                    description: str=None, dueDate: datetime=None,
                    isDueDateCompleted: bool=None,
                    stopwatch: _Stopwatch=None, boardId: int=None,
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
            required=('name', 'position'),
            noarg=self)
        
        overload['boardId'] = self.boardId
        overload['listId'] = self.id

        route = self.routes.post_card(id=self.id)
        return Card(**route(**overload)['item']).bind(self.routes)

    def sort(self, sort: SortOption) -> None:
        route = self.routes.post_sort_list(id=self.id)
        route(**{'type': ListSorts[sort]})

    def delete(self) -> None:
        """Deletes the list CANNOT BE UNDONE"""
        route = self.routes.delete_list(id=self.id)
        route()

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
        
        if 'position' in overload:
            overload['position'] = set_position(overload['position'])
        
        route = self.routes.patch_list(id=self.id)
        self.__init__(**route(**overload)['item'])
        return self

    def refresh(self) -> None:
        """Refreshes the list data"""
        for _list in self.board.lists:
            if _list.id == self.id:
                self.__init__(**_list)
                return
        raise ValueError(f'List: {self.name} with id({self.id}) not found, it was likely deleted')

class ProjectManager(_ProjectManager): ...

class Task(_Task): ...

if __name__ == '__main__':
    auth = PasswordAuth(username_or_email='demo', password='demo')
    planka = Planka('http://localhost:3000', auth=auth)