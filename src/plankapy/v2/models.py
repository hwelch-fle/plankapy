from __future__ import annotations
from collections.abc import Generator, Iterator, Mapping
from datetime import datetime
import json
from typing import (
    Any, 
    Generic, 
    Literal, 
    Self, 
    TypeVar, 
    Unpack,
)

from .api import (
    schemas,
    paths,
)

__all__ = (
    "Action",
    "Attachment",
    "BackgroundImage",
    "BaseCustomFieldGroup",
    "Board",
    "BoardMembership",
    "Card",
    "CardLabel",
    "CardMembership",
    "Comment",
    "Config",
    "CustomField",
    "CustomFieldGroup",
    "CustomFieldValue",
    "Label",
    "List",
    "Notification",
    "NotificationService",
    "Project",
    "ProjectManager",
    "Task",
    "TaskList",
    "User",
    "Webhook", #TODO
    
    # Literal tuples
    "BoardViews",
    "CardTypes",
    "BoardRoles",
    "LabelColors",
    "ListColors",
    "BackgroundGradients",
    "Languages",
    "EditorModes",
    "HomeViews",
    "ProjectOrderings",
    "TermsTypes",
    "LockableFields",
    "NotificationTypes",
)

TYPE_CHECKING = False
if TYPE_CHECKING:
    # Models take a Planka session to allow checking User permissions
    from .interface import Planka

_S = TypeVar('_S', bound=Mapping[str, Any])
class PlankaModel(Generic[_S]):
    """Base Planka object interface"""
    
    def __init__(self, schema: _S, session: Planka) -> None:
        self._schema = schema
        self.session = session
        self.endpoints = session.endpoints
        self.client = session.client
    
    @property
    def schema(self) -> _S:
        return self._schema
    @schema.setter
    def schema(self, schema: _S) -> None:
        self._schema = schema
    
    @property
    def id(self) -> str:
        if 'id' not in self.schema:
            # Should only happen for schemas.Config
            raise AttributeError(f'{self.__class__.__name__}: Does not have an `id` attribute')
        return self.schema['id']
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, PlankaModel):
            try:
                return (
                    self.id == other.id 
                    and self.__class__ == other.__class__ # type: ignore
                )
            except AttributeError: # handle no id case (Config)
                return False
        else:
            return super().__eq__(other)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(schema={self.__dict__})'
    
    #def __getattribute__(self, name: str) -> Any:
    #    # TODO: use `_live_mode` to force a `sync` call on attribute acces
    #    return super().__getattribute__(name)           
    
    def json(self, **kwargs: Any) -> str:
        return json.dumps(self.schema, **kwargs)


class Action(PlankaModel[schemas.Action]):
    """Python interface for Planka Actions"""
    
    @property
    def created_at(self) -> datetime:
        """When the Action was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the Action was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    @property
    def card(self) -> Card:
        """The Card where the Action occurred"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def board(self) -> Board:
        """The Board where the Action occurred"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)
    
    @property
    def user(self) -> User:
        """The User who performed the Action (Raise LookupError if User is not found in Board)"""
        _usrs = [u for u in self.card.board.users if self.schema['userId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['userId']}")
    
    @property
    def data(self) -> dict[str, Any]:
        """The specific data associated with the Action (type dependant)"""
        return self.schema['data']
    
    @property
    def type(self):
        """The type of the Action"""
        return self.schema['type']

  
class Attachment(PlankaModel[schemas.Attachment]):
    """Python interface for Planka Attachments"""
    
    @property
    def name(self) -> str:
        """The name of the Attachment"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the Attachment name"""
        self.update(name=name)
    
    @property
    def created_at(self) -> datetime:
        """When the Attachment was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the Attachment was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    @property
    def card(self) -> Card:
        """The Card the Attachment belongs to"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def creator(self) -> User:
        """The User created the Attachment (Raises LookupError if User is not found in Board)"""
        _usrs = [u for u in self.card.board.users if self.schema['creatorUserId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['creatorUserId']}")
    
    @property
    def data(self) -> dict[str, Any]:
        """The specific data associated with the action (type dependant)"""
        return self.schema['data']
    
    @property
    def type(self):
        """The type of the action"""
        return self.schema['type']
    
    # Special Methods
    def sync(self) -> None:
        """Pull the latest state of the Attachment from the Planka Server"""
        # No endpoint for attachments, need to get it through the associated Card
        _new = [a for a in self.card.attachments if a.id == self.id]
        if not _new:
            raise ValueError(f'Attachment {self.id} No longer exists!')
        self.schema = _new.pop().schema

    def update(self, **attachment: Unpack[paths.Request_updateAttachment]) -> None:
        """Update the Attachment with the provided values"""
        self.schema = self.endpoints.updateAttachment(self.id, **attachment)['item']

    def delete(self):
        """Delete the Attachment"""
        return self.endpoints.deleteAttachment(self.id)
    
    def download(self) -> Iterator[bytes]:
        """Get a byte Iterator for stream downloading"""
        return self.client.get(self.schema['data']['url']).iter_bytes()

           
class BackgroundImage(PlankaModel[schemas.BackgroundImage]):
    """Python interface for Planka Background Images"""

    # BackgroundImage Properties
    @property
    def created_at(self) -> datetime:
        """When the BackgroundImage was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the BackgroundImage was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    @property
    def project(self) -> Project:
        """The Project the BackgroundImage belongs to"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)
    
    @property
    def size_in_bytes(self) -> int:
        """The size of the BackgroundImage in bytes"""
        # The Swagger schema says this is a string, but it's should be an int
        return int(self.schema['sizeInBytes'])
    
    @property
    def url(self) -> str:
        """The URL to access the BackgroundImage"""
        return self.schema['url']
    
    @property
    def thumbnails(self) -> dict[str, str]:
        """URLs for different thumbnail sizes of the background image"""
        return self.schema['thumbnailUrls']
    
    # Special Methods
    def download(self) -> Iterator[bytes]:
        """Get bytes for the full image
        
        Returns:
            (Iterator[bytes]): A byte iterator for the full image
        """
        return self.client.get(self.url).iter_bytes()
    
    def download_thumbnails(self) -> Generator[tuple[str, Iterator[bytes]]]:
        """Get byte iterators for all thumbnails
        
        Yields:
            (tuple[str, Iterator[bytes]]): A tuple containing the size key and the thumbnail byte iterator
        """
        for size, url in self.thumbnails.items():
            yield size, self.client.get(url).iter_bytes()
        
    def delete(self):
        """Delete the BackgroundImage"""
        return self.endpoints.deleteBackgroundImage(self.id)

    
class BaseCustomFieldGroup(PlankaModel[schemas.BaseCustomFieldGroup]):
    """Python interface for Planka BaseCustomFieldGroups"""

    # BaseCustomFieldGroup Properties
    @property
    def project(self) -> Project:
        """The Project that the BaseCustomFieldGroup is associated with"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)

    @property
    def name(self) -> str:
        """Name/title of the base custom field group"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the name/title of the base custom field group"""
        self.update(name=name)
    
    @property
    def created_at(self) -> datetime:
        """When the base custom field group was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the base custom field group was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    # Special Methods
    def sync(self):
        """Sync the BaseCustomFieldGroup with the Planka server"""
        for bcfg in self.project.base_custom_field_groups:
            if bcfg == self:
                self.schema = bcfg.schema
                
    def update(self, **base_custom_field_group: Unpack[paths.Request_updateBaseCustomFieldGroup]):
        """Update the BaseCustomFieldGroup"""
        self.endpoints.updateBaseCustomFieldGroup(self.id, **base_custom_field_group)
        
    def delete(self):
        """Delete the BaseCustomFieldGroup"""
        return self.endpoints.deleteBaseCustomFieldGroup(self.id)


BoardView = Literal['kanban', 'grid', 'list']
BoardViews: tuple[BoardView] = BoardView.__args__

CardType = Literal['project', 'story']
CardTypes: tuple[CardType] = CardType.__args__

BoardRole = Literal['editor', 'viewer']
BoardRoles: tuple[BoardRole] = BoardRole.__args__

class Board(PlankaModel[schemas.Board]):
    """Python interface for Planka Boards"""
    
    @property
    def url(self) -> str:
        return str(self.client.base_url.join(f'/boards/{self.id}'))
    
    # Included objects
    @property
    def _included(self):
        return self.endpoints.getBoard(self.id)['included']
    
    @property
    def labels(self) -> list[Label]:
        """Get all Labels on the Board"""
        return [Label(l, self.session) for l in self._included['labels']]
    
    @property
    def cards(self) -> list[Card]:
        """Get all active Cards on the Board (use archived_cards and trashed_cards for archived/trashed Card lists)"""
        return [Card(c, self.session) for c in self._included['cards']]
    
    @property
    def trashed_cards(self) -> list[Card]:
        """Get all Cards in the Board trash list"""
        return [Card(c, self.session) for c in self.endpoints.getCards(self.trash_list.id)['items']]
    
    @property
    def archived_cards(self) -> list[Card]:
        """Get all Cards in the Board archive list"""
        return [Card(c, self.session) for c in self.endpoints.getCards(self.archive_list.id)['items']]

    @property
    def subscribed_cards(self) -> list[Card]:
        """Get all Cards on the Board that the current User is subscribed to"""
        return [Card(sc, self.session) for sc in self._included['cards'] if sc['isSubscribed']]
    
    @property
    def projects(self) -> list[Project]:
        """Get all Projects that the Board is associated with (use `Board.Project` instead, this is always one item)"""
        return [Project(p, self.session) for p in self._included['projects']]
    
    @property
    def board_memberships(self) -> list[BoardMembership]:
        """Get all BoardMemberships for the Board"""
        return [BoardMembership(bm, self.session) for bm in self._included['boardMemberships']]
    
    @property
    def users(self) -> list[User]:
        """Get all Users on the Board"""
        return [User(u, self.session) for u in self._included['users']]

    @property
    def editors(self) -> list[User]:
        """Get all editor Users for the Board"""
        return [bm.user for bm in self.board_memberships if bm.role == 'editor']
    
    @property
    def viewers(self) -> list[User]:
        """Get all viewer Users for the Board"""
        return [bm.user for bm in self.board_memberships if bm.role == 'editor']

    @property
    def all_lists(self) -> list[List]:
        """Get all Lists associated with the Board"""
        return [List(l, self.session) for l in self._included['lists']]
    
    @property
    def card_memberships(self) -> list[CardMembership]:
        """Get all CardMemberships associated with the Board"""
        return [CardMembership(cm, self.session) for cm in self._included['cardMemberships']]
    
    @property
    def card_labels(self) -> list[CardLabel]:
        """Get all CardLabels associated with the Board"""
        return [CardLabel(cl, self.session) for cl in self._included['cardLabels']]
    
    @property
    def task_lists(self) -> list[TaskList]:
        """Get all TaskLists associated with the Board"""
        return [TaskList(tl, self.session) for tl in self._included['taskLists']]
    
    @property
    def tasks(self) -> list[Task]:
        """Get all Tasks associated with the Board"""
        return [Task(t, self.session) for t in self._included['tasks']]
    
    @property
    def attachments(self) -> list[Attachment]:
        """Get all Attachments associated with the Board"""
        return [Attachment(a, self.session) for a in self._included['attachments']]
    
    @property
    def custom_field_groups(self) -> list[CustomFieldGroup]:
        """Get all CustomFieldGroups associated with the Board"""
        return [CustomFieldGroup(cfg, self.session) for cfg in self._included['customFieldGroups']]
    
    @property
    def custom_fields(self) -> list[CustomField]:
        """Get all CustomFields associated with the Board"""
        return [CustomField(cf, self.session) for cf in self._included['customFields']]
    
    @property
    def custom_field_values(self) -> list[CustomFieldValue]:
        """Get all CustomFieldValues associated with the Board"""
        return [CustomFieldValue(cfv, self.session) for cfv in self._included['customFieldValues']]
    
    @property
    def archive_list(self) -> List:
        """Get the archive List for the Board (archive List is not a normal List!)"""
        return [l for l in self.all_lists if l.type == 'archive'].pop()
    
    @property
    def trash_list(self) -> List:
        """Get the trash List for the Board (trash List is not a normal List!)"""
        return [l for l in self.all_lists if l.type == 'trash'].pop()
    
    @property
    def active_lists(self) -> list[List]:
        """Get all active Lists for the Board"""
        return [l for l in self.all_lists if l.type == 'active']
    
    @property
    def closed_lists(self) -> list[List]:
        """Get all closed Lists for the Board"""
        return [l for l in self.all_lists if l.type == 'closed']

    # Board props
    @property
    def subscribed(self) -> bool:
        """Whether the current user is subscribed to the Board"""
        return self.endpoints.getBoard(self.id)['item']['isSubscribed']
    
    @property
    def project(self) -> Project:
        """TheProject the Board belongs to"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)
    
    @property
    def position(self) -> int:
        """Position of the Board within the Project"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Position of the Board within the Project"""
        self.update(position=position)

    @property
    def name(self) -> str:
        """Name/title of the Board"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the name/title of the Board"""
        self.update(name=name)

    @property
    def default_view(self) -> BoardView:
        """Default view for the board"""
        return self.schema['defaultView']
    @default_view.setter
    def default_view(self, default_view: BoardView) -> None:
        """Set default view for the board"""
        self.update(defaultView=default_view)

    @property
    def default_card_type(self) -> CardType:
        """Default Card type for new Cards"""
        return self.schema['defaultCardType']
    @default_card_type.setter
    def default_card_type(self, default_card_type: CardType) -> None:
        """Set default Card type for new Cards"""
        self.update(defaultCardType=default_card_type)

    @property
    def limit_card_types_to_default_one(self) -> bool:
        """Whether to limit Card types to default one"""
        return self.schema['limitCardTypesToDefaultOne']
    @limit_card_types_to_default_one.setter
    def limit_card_types_to_default_one(self, limit_card_types_to_default_one: bool) -> None:
        """Set whether to limit Card types to default one"""
        self.update(limitCardTypesToDefaultOne=limit_card_types_to_default_one)

    @property
    def always_display_card_creator(self) -> bool:
        """Whether to always display the Card creator"""
        return self.schema['alwaysDisplayCardCreator']
    @always_display_card_creator.setter
    def always_display_card_creator(self, always_display_card_creator: bool) -> None:
        """Set whether to always display the Card creator"""
        self.update(alwaysDisplayCardCreator=always_display_card_creator)

    @property
    def expand_task_lists_by_default(self) -> bool:
        """Whether to expand TaskLists by default"""
        return self.schema['expandTaskListsByDefault']
    @expand_task_lists_by_default.setter
    def expand_task_lists_by_default(self, expand_task_lists_by_default: bool) -> None:
        """Set whether to expand TaskLists by default"""
        self.update(expandTaskListsByDefault=expand_task_lists_by_default)

    @property
    def created_at(self) -> datetime:
        """When the Board was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    @property
    def updated_at(self) -> datetime:
        """When the Board was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    # Special Methods
    def sync(self) -> None:
        """Sync the Board with the Planka Server"""
        self.schema = self.endpoints.getBoard(self.id)['item']
        
    def update(self, **board: Unpack[paths.Request_updateBoard]) -> None:
        """Update the Board"""
        self.schema = self.endpoints.updateBoard(self.id, **board)['item']
        
    def delete(self):
        """Delete the Board"""
        return self.endpoints.deleteBoard(self.id)

    def create_list(self, **lst: Unpack[paths.Request_createList]) -> List:
        """Create a new List on the Board"""
        return List(self.endpoints.createList(self.id, **lst)['item'], self.session)

    def create_label(self, **lbl: Unpack[paths.Request_createLabel]) -> Label:
        """Create a new Label on the Board"""
        return Label(self.endpoints.createLabel(self.id, **lbl)['item'], self.session)
    
    def add_member(self, user: User, 
                   *,
                   role: BoardRole='viewer',
                   can_comment: bool=False) -> BoardMembership:
        """Add a User to the Board
        
        Args:
            role (Literal['viewer', 'editor']): The Role to assign to the user (default: `viewer`)
            can_comment (bool): If role is `viewer` set commenting status (default: `False`)
        """
        # Create a new membership
        if user not in self.users:
            BoardMembership(
                self.endpoints.createBoardMembership(
                    self.id, 
                    userId=user.id, 
                    role=role, 
                    canComment=can_comment)['item'], 
                self.session
            )
        
        # Get existing membership and update role different
        membership = [bm for bm in self.board_memberships if bm.user == user].pop()
        if membership.role != role:
            membership.role = role
        if membership.can_comment != can_comment:
            membership.can_comment = can_comment
        return membership
    
    def add_editor(self, user: User) -> None:
        """Add a Board editor"""
        if user not in self.users or user in self.viewers:
            self.endpoints.createBoardMembership(self.id, userId=user.id, role='editor')
        elif user in self.viewers:
            bm = [bm for bm in self.board_memberships if bm.user == user].pop()
            self.endpoints.updateBoardMembership(bm.id, role='editor')

    def add_viewer(self, user: User, *, can_comment: bool=False) -> None:
        """Add a Board viewer Set can_comment flag to True for commenting privelege"""
        if user not in self.users:
            self.endpoints.createBoardMembership(self.id, userId=user.id, role='viewer')
        elif user in self.editors:
            bm = [bm for bm in self.board_memberships if bm.user == user].pop()
            self.endpoints.updateBoardMembership(bm.id, role='viewer', canComment=can_comment)


class BoardMembership(PlankaModel[schemas.BoardMembership]):
    """Python interface for Planka BoardMemberships"""
    
    # BoardMembership properties

    @property
    def project(self) -> Project:
        """The Project the BoardMembership belongs to"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)
    
    @property
    def board(self) -> Board:
        """The Board the BoardMembership is associated with"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)
    
    @property
    def user(self) -> User:
        """The User the BoardMembership is associated with (Raises LookupError if User no longer in the Board)"""
        _usrs = [u for u in self.board.users if self.schema['userId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['userId']}")

    @property
    def role(self) -> BoardRole:
        """Role of the user in the board"""
        return self.schema['role']
    @role.setter
    def role(self, role: BoardRole) -> None:
        """Set the role of the User in the Board"""
        self.update(role=role)
    
    @property
    def can_comment(self) -> bool:
        """Whether the user can comment on cards"""
        if self.role == 'viewer':
            return self.schema['canComment']
        return True
    @can_comment.setter
    def can_comment(self, can_comment: bool) -> None:
        """Set if a viewer User can comment"""
        if self.role == 'viewer':
            self.update(canComment=can_comment)

    @property
    def created_at(self) -> datetime:
        """When the board membership was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the board membership was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    # Special Methods
    def sync(self):
        """Sync the BoardMembership with the Planka server"""
        _bms = [bm for bm in self.board.board_memberships if bm == self]
        if _bms:
            self.schema = _bms.pop().schema

    def update(self, **kwargs: Unpack[paths.Request_updateBoardMembership]) -> None:
        """Update the BoardMembership"""
        self.schema = self.endpoints.updateBoardMembership(self.id, **kwargs)['item']

    def delete(self):
        """Delete the BoardMebership"""
        return self.endpoints.deleteBoardMembership(self.id)


class Card(PlankaModel[schemas.Card]):
    """Python interface for Planka Cards"""
    
    @property
    def url(self) -> str:
        """The URL to the card"""
        return str(self.client.base_url.join(f'/cards/{self.id}'))
    
    # Included objects
    @property
    def _included(self):
        return self.endpoints.getCard(self.id)['included']
    
    @property
    def attachments(self) -> list[Attachment]:
        """Get all Attachments associated with the Card"""
        return [Attachment(a, self.session) for a in self._included['attachments']]
    
    @property
    def card_memberships(self) -> list[CardMembership]:
        """Get all CardMemberships associated with the Card"""
        return [CardMembership(cm, self.session) for cm in self._included['cardMemberships']]
    
    @property
    def users(self) -> list[User]:
        """Get all Users associated with the Card (including Creator)"""
        return [User(u, self.session) for u in self._included['users']]
    
    @property
    def members(self) -> list[User]:
        """Get all Users Assigned to the card"""
        return [cm.user for cm in self.card_memberships]
    
    @property
    def labels(self) -> list[Label]:
        """Get all Labels associated with the Card"""
        _card_label_ids = [l['id'] for l in self._included['cardLabels']]
        return [l for l in self.board.labels if l.id in _card_label_ids]
    
    @property
    def tasks(self) -> list[Task]:
        """Get all Tasks associated with the card"""
        return [Task(t, self.session) for t in self._included['tasks']]
    
    @property
    def task_lists(self) -> list[TaskList]:
        """Get all TaskLists associated with the Card"""
        return [TaskList(tl, self.session) for tl in self._included['taskLists']]
    
    @property
    def custom_field_groups(self) -> list[CustomFieldGroup]:
        """Get all CustomFieldGroups associated with the Card"""
        return [CustomFieldGroup(cfg, self.session) for cfg in self._included['customFieldGroups']]
    
    @property
    def custom_fields(self) -> list[CustomField]:
         """Get all CustomFields associated with the Card"""
         return [CustomField(cf, self.session) for cf in self._included['customFields']]
    
    @property
    def custom_field_values(self) -> list[CustomFieldValue]:
        """Get all CustomFieldValues associated with the Card"""
        return [CustomFieldValue(cfv, self.session) for cfv in self._included['customFieldValues']]
    
    @property
    def comments(self) -> list[Comment]:
        """Get all Comments on the Card"""
        return [Comment(c, self.session) for c in self.endpoints.getComments(self.id)['items']]

    @property
    def actions(self) -> list[Action]:
        """Get all Actions associated with the Card"""
        return [Action(a, self.session) for a in self.endpoints.getCardActions(self.id)['items']]

    # Card props
    @property
    def subscribed(self) -> bool:
        """If the current user is subscribed to the Card"""
        return self.endpoints.getCard(self.id)['item']['isSubscribed']
    @subscribed.setter
    def subscribed(self, subscribed: bool) -> None:
        """Set subscription status on the Card for the current User"""
        self.update(isSubscribed=subscribed)

    @property
    def board(self) -> Board:
        """The Board the Card belongs to"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)
    
    @property
    def list(self)-> List:
        """The List the Card belongs to"""
        return List(self.endpoints.getList(self.schema['listId'])['item'], self.session)
    @list.setter
    def list(self, list: List) -> Self:
        """Set List the Card belongs to"""
        self.update(listId=list.id, boardId=list.board.id)
        return self

    @property
    def creator(self) -> User:
        """The User who Created the card (Raises LookupError if User is no longer a Board Member)"""
        _usrs = [u for u in self.users if self.schema['creatorUserId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['creatorUserId']}")
    
    @property
    def prev_list(self) -> List | None:
        """The previous List the card was in (available when in archive or trash)"""
        if self.schema['prevListId']:
            return List(self.endpoints.getList(self.schema['prevListId'])['item'], self.session)
    
    @property
    def cover(self) -> Attachment | None:
        """The Attachment used as cover (None if no cover)"""
        for attachment in self.attachments:
            if attachment.id == self.schema['coverAttachmentId']:
                return attachment
            
    @cover.setter
    def cover(self, attachment: Attachment) -> None:
        """Set the Card cover"""
        if attachment.card != self:
            raise ValueError(f'Attachment ')
        self.update(coverAttachmentId=attachment.id)
    
    @property
    def type(self):
        """Type of the Card"""
        return self.schema['type']
    @type.setter
    def type(self, type: Literal['project', 'story']) -> None:
        """Set the Card type"""
        self.update(type=type)
    
    @property
    def position(self) -> int:
        """Position of the Card within the List"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Set the card position"""
        self.update(position=position)
    
    @property
    def name(self) -> str:
        """Name/title of the Card"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the Card name"""
        self.update(name=name)
    
    @property
    def description(self) -> str:
        """Detailed description of the Card"""
        return self.schema['name']
    @description.setter
    def description(self, description: str) -> None:
        """Set the Card Description"""
        self.update(description=description)
    
    @property
    def due_date(self) -> datetime:
        """Due date for the card"""
        return datetime.fromisoformat(self.schema['dueDate'])
    @due_date.setter
    def due_date(self, due_date: datetime) -> None:
        """Set the due date"""
        self.update(dueDate=due_date.isoformat())
    
    @property
    def due_date_completed(self) -> bool:
        """Whether the due date is completed"""
        return self.schema['isDueCompleted']
    @due_date_completed.setter
    def due_date_completed(self, is_completed: bool) -> None:
        """Set the due date completion status"""
        self.update(isDueCompleted=is_completed)
    
    @property
    def stopwatch(self) -> Stopwatch:
        """Stopwatch for time tracking"""
        return Stopwatch(self)
    
    @property
    def comments_count(self) -> int:
        """Total number of comments on the Card"""
        return self.schema['commentsTotal']
    @property
    def is_closed(self) -> bool:
        """Whether the Card is closed"""
        return self.schema['isClosed']
    
    @property
    def list_changed_at(self) -> datetime:
        """When the Card was last moved between Lists"""
        return datetime.fromisoformat(self.schema['listChangedAt'])
    
    @property
    def created_at(self) -> datetime:
        """When the Card was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the Card was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    # Special Methods
    def sync(self):
        """Sync the Card with the Planka server"""
        self.schema = self.endpoints.getCard(self.id)['item']
        
    def update(self, **card: Unpack[paths.Request_updateCard]):
        """Update the Card

        Note:
            dueDate can be set using iso string or datetime object
        """
        # Convert the dueDate to a iso string if a datetime is passed
        if 'dueDate' in card and isinstance(card['dueDate'], datetime):
            card['dueDate'] = card['dueDate'].isoformat()
        if 'type' not in card:
            card['type'] = self.schema['type']
        self.schema = self.endpoints.updateCard(self.id, **card)['item']
 
    def delete(self):
        """Delete the Card"""
        return self.endpoints.deleteCard(self.id)

    def move(self, list: List, position: Literal['top', 'bottom'] | int = 'top') -> Card:
        """Move the card to a new list (default to top of new list)"""

        if isinstance(position, int):
            pos = position
        elif position == 'top':
            pos = 0
        elif position == 'bottom':
            pos = max((c.position for c in list.cards), default=0)
        else:
            raise ValueError(f'position must be int or one of `top`/`bottom`')
        
        self.update(
            listId=list.id, 
            boardId=list.board.id, 
            position=pos,
        )
        return self

    def restore(self, position: Literal['top', 'bottom'] | int='top') -> Card:
        """Restore the Card from arcive/trash to its previous list"""
        if self.prev_list is not None:
            self.move(self.prev_list, position)
        return self
    
    # TODO: Handle uploading files better. See v1 implementation, but use httpx `files` streaming
    def add_attachment(self, attachment: str | bytes, *, cover: bool=False, name: str | None=None) -> Attachment:
        """Add an Attachment to the card
        
        Args:
            attachment (str | bytes): The URL or raw bytes of the attachment
            cover (bool): Set the new attachment as the cover of the card
            name (str | None): The optional name of the attachment (default is `hash()`)
            
        Returns:
            Attachment
        
        Raises:
            ValueError: If the passed attachment isn't a string or bytes 
            HTTPStatusError: If the request fails
        """
        # Attach URL
        if isinstance(attachment, str) and attachment.startswith('http'):
            r = self.endpoints.createAttachment(
                self.id, 
                type='link', 
                url=attachment, 
                name=name or str(hash(attachment))
            )
            a = Attachment(r['item'], self.session)
        
        # Attach File
        elif isinstance(attachment, bytes):
            r = self.endpoints.createAttachment(
                self.id, 
                type='file', 
                file=str(attachment), 
                name=name or str(hash(attachment))
            )
            a =  Attachment(r['item'], self.session)
        else:
            raise ValueError(f'Expected str or bytes for Attachment, got {type(attachment)}')

        # Set cover if requested
        if cover and a.type != 'link':
            self.update(coverAttachmentId=a.id)
        return a

    def get_field_values(self, *, with_groups: bool=False) -> dict[str, Any]:
        """Get a mapping of CustomFields to CustomFieldValues
        
        Args:
            with_groups (bool): If set to `True`, 
                return a nested dict with `{group: {field: value, ...}, ...}`, otherwise `{field: value ...}` (default: `False`)
        """
        if with_groups:
            return {
                cfg.name: {cfv.custom_field.name: cfv.content for cfv in cfg.custom_field_values}
                for cfg in self.custom_field_groups
            }
        else:
            return {
                cfv.custom_field.name: cfv.content
                for cfv in self.custom_field_values
            }

    def add_member(self, user: User, 
                   *, 
                   add_to_board: bool=False, 
                   role: BoardRole='viewer', 
                   can_comment: bool=False) -> CardMembership:
        """Add a User to the Card
        
        Args:
            add_to_board (bool): Add the User to the Board if they are not already a member
            role (Literal['viewer', 'editor']): If User is added to board, set role (default: `viewer`)
            can_comment (bool): If User is added as a `viewer`, set commenting status (default: `False`)
        
        Raises:
            PermissionError: If the User is not a member of the Board and `add_to_board` is `False`
        
        Note:
            Default options for adding to Board abide by least privilege so role and comment must be set 
        """
        # User is already a member
        if user in self.members:
            return [cm for cm in self.card_memberships if cm.user == user].pop()
        
        # User is not in the board
        elif user not in self.board.users:
            # Add the user to the board
            if add_to_board:
                self.board.add_member(user, role=role, can_comment=can_comment if role == 'viewer' else True)
            else:
                raise PermissionError(f'User must be added to the Board to become a Card Member')        
        return CardMembership(self.endpoints.createCardMembership(self.id, userId=user.id)['item'], self.session)

    def remove_member(self, user: User) -> None:
        """Remove a User member from the Card"""
        for cm in self.card_memberships:
            if cm.user == user:
                cm.delete()

class CardLabel(PlankaModel[schemas.CardLabel]):
    """Python interface for Planka CardLabels"""

    # CardLabel properties

    @property
    def card(self) -> Card:
        """The Card the Label is associated with"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)

    @property
    def label(self) -> Label:
        """The Label associated with the card"""
        _cls = [l for l in self.card.labels if l.id == self.id]
        if _cls:
            return _cls.pop()
        raise ValueError(f'Label no longer exists')

    @property
    def created_at(self) -> datetime:
        """When the card-label association was created"""
        return datetime.fromisoformat(self.schema['createdAt'])

    @property
    def updated_at(self) -> datetime:
        """When the card-label association was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    def delete(self):
        """Delete the CardLabel"""
        return self.endpoints.deleteCardLabel(cardId=self.card.id, labelId=self.label.id)


class CardMembership(PlankaModel[schemas.CardMembership]):
    """Python interface for Planka CardMemberships"""

    # CardMembership properties
    
    @property
    def card(self) -> Card:
        """The Card the User is a member of"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)

    @property
    def user(self) -> User:
        """The User who is a member of the Card (Raise LookupError if the User is no longer on the Board)"""
        _usrs = [u for u in self.card.board.users if self.schema['userId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['userId']}")

    @property
    def created_at(self) -> datetime:
        """When the card membership was created"""
        return datetime.fromisoformat(self.schema['createdAt'])

    @property
    def updated_at(self) -> datetime:
        """When the card membership was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    def delete(self):
        """Delete the CardMembership"""
        return self.endpoints.deleteCardMembership(userId=self.user.id, cardId=self.card.id)

   
class Comment(PlankaModel[schemas.Comment]):
    """Python interface for Planka Comments"""
    
    # Comment properties

    @property
    def card(self) -> Card:
        """The Card the Comment belongs to"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def user(self) -> User | None:
        """The User who created the Comment (Raises LookupError if the User is not a BoardMember)"""
        _usrs = [u for u in self.card.board.users if self.schema['userId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['userId']}")
    
    @property
    def text(self) -> str:
        """Content of the Comment"""
        return self.schema['text']
    
    @property
    def created_at(self) -> datetime:
        """When the comment was created"""
        return datetime.fromisoformat(self.schema['createdAt'])

    @property
    def updated_at(self) -> datetime:
        """When the comment was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    # Special Methods
    def sync(self):
        """Sync the Comment with the Planka server"""
        _cm = [cm for cm in self.card.comments if cm == self]
        if _cm:
            self.schema = _cm.pop().schema

    def update(self, **kwargs: Unpack[paths.Request_updateComments]):
        """Update the Comment (must be the comment Creator or an Admin)"""
        self.endpoints.updateComments(self.id, **kwargs)

    def delete(self):
        """Delete the Comment"""
        return self.endpoints.deleteComment(self.id)

   
class Config(PlankaModel[schemas.Config]):
    """Python interface for Planka Config"""
    
    @property
    def version(self) -> str:
        """Current version of the PLANKA application"""
        return self.schema['version']
    
    @property
    def activeUsersLimit(self) -> int | None:
        """Maximum number of active users allowed (conditionally added for admins if configured)"""
        return self.schema.get('activeUsersLimit')

    @property
    def oidc(self) -> dict[str, Any] | None:
        """OpenID Connect configuration (null if not configured)"""
        return self.schema.get('oidc')
  
class CustomField(PlankaModel[schemas.CustomField]):
    """Python interface for Planka CustomFields"""
    
    # CustomField props
    @property
    def base_custom_field_group(self) -> BaseCustomFieldGroup:
        """The BaseCustomFieldGroup the custom field belongs to"""
        return self.custom_field_group.base_custom_field_group
    
    @property
    def custom_field_group(self) -> CustomFieldGroup:
        """The CustomFieldGroup the CustomField belongs to"""
        return CustomFieldGroup(self.endpoints.getCustomFieldGroup(self.schema['customFieldGroupId'])['item'], self.session)
    
    @property
    def position(self) -> int:
        """Position of the CustomField within the CustomFieldGroup"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Set the position of the CustomField within the CustomFieldGroup"""
        self.update(position=position)

    @property
    def name(self) -> str:
        """Name/title of the custom field"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        self.update(name=name)

    @property
    def show_on_front_of_card(self) -> bool:
        """Whether to show the CustomField on the front of Cards"""
        return self.schema['showOnFrontOfCard']
    @show_on_front_of_card.setter
    def show_on_front_of_card(self, show_on_front_of_card: bool) -> None:
        """Set Wwether to show the CustomField on the front of Cards"""
        self.update(showOnFrontOfCard=show_on_front_of_card)

    @property
    def created_at(self) -> datetime:
        """When the custom field was created"""
        return datetime.fromisoformat(self.schema['createdAt'])

    @property
    def updated_at(self) -> datetime:
        """When the custom field was last updated"""
        return datetime.fromisoformat(self.schema['createdAt'])

    # Special Methods
    def sync(self):
        """Sync the CustomField with the Planka server"""

    def update(self, **kwargs: Unpack[paths.Request_updateCustomField]):
        """Update the CustomField"""
        self.schema = self.endpoints.updateCustomField(self.id, **kwargs)['item']
    
    def delete(self):
        """Delete the CustomField"""
        self.endpoints.deleteCustomField(self.id)

   
class CustomFieldGroup(PlankaModel[schemas.CustomFieldGroup]):
    """Python interface for Planka CustomFieldGroups"""
    
    # CustomFieldGroup included

    @property
    def _included(self):
        return self.endpoints.getCustomFieldGroup(self.id)['included']

    @property
    def custom_fields(self) -> list[CustomField]:
        return [CustomField(cf, self.session) for cf in self._included['customFields']]

    @property
    def custom_field_values(self) -> list[CustomFieldValue]:
        return [CustomFieldValue(cfv, self.session) for cfv in self._included['customFieldValues']]

    # CustomFieldGroup props

    @property
    def board(self) -> Board:
        """The Board the CustomFieldGroup belongs to"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)
    
    @property
    def card(self) -> Card:
        """The Card the CustomFieldGroup belongs to"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def base_custom_field_group(self) -> BaseCustomFieldGroup:
        """The BaseCustomFieldGroup used as a template"""
        _bcfgs = [bcfg for bcfg in self.board.project.base_custom_field_groups if bcfg.id == self.schema['baseCustomFieldGroupId']]
        return _bcfgs.pop()
    
    @property
    def position(self) -> int:
        """Position of the CustomFieldGroup within the Board/Card"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Set the CustomFieldGroup position within the Board/Card"""
        self.update(position=position) 

    @property
    def name(self) -> str:
        """Name/title of the CustomFieldGroup"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the CustomFieldGroup name"""
        self.update(name=name)

    @property
    def created_at(self) -> datetime:
        """When the CustomFieldGroup was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the CustomFieldGroup was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    # Special Methods
    def sync(self):
        """Sync the CustomFieldGroup with the Planka server"""
        self.schema = self.endpoints.getCustomFieldGroup(self.id)['item']
    
    def update(self, **kwargs: Unpack[paths.Request_updateCustomFieldGroup]):
        """Update the CustomFieldGroup"""
        self.schema = self.endpoints.updateCustomFieldGroup(self.id, **kwargs)['item']

    def delete(self):
        """Delete the CustomFieldGroup"""
        return self.endpoints.deleteCustomFieldGroup(self.id)

  
class CustomFieldValue(PlankaModel[schemas.CustomFieldValue]):
    """Python interface for Planka CustomFieldValues"""
    
    # CustomFieldValue props

    @property
    def card(self) -> Card:
        """The Card the CustomFieldValue belongs to"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def custom_field_group(self) -> CustomFieldGroup:
        """The CustomFieldGroup the CustomFieldValue belongs to"""
        return CustomFieldGroup(self.endpoints.getCustomFieldGroup(self.schema['customFieldGroupId'])['item'], self.session)

    @property
    def custom_field(self) -> CustomField:
        """The CustomField the CustomFieldValue belongs to"""
        _cfs = [cf for cf in self.custom_field_group.custom_fields if cf.id == self.schema['customFieldId']]
        return _cfs.pop()

    @property
    def content(self) -> str:
        """Content/value of the custom field"""
        return self.schema['content']
    @content.setter
    def content(self, content: str) -> None:
        """Set the content value of the CustomFieldValue"""
        self.update(content=content)

    @property
    def created_at(self) -> datetime:
        """When the CustomFieldValue was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the CustomFieldValue was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    # Special Methods
    def sync(self):
        """Sync the CustomFieldValue with the Planka server"""
        _cfvs = [cfv for cfv in self.card.custom_field_values if cfv.id == self.id]
        if _cfvs:
            self.schema = _cfvs.pop().schema

    def update(self, **kwargs: Unpack[paths.Request_updateCustomFieldValue]):
        """Update the CustomFieldValue"""
        self.schema = self.endpoints.updateCustomFieldValue(
            cardId=self.schema['cardId'],
            customFieldGroupId=self.schema['customFieldGroupId'],
            customFieldId=self.schema['customFieldId'],
            **kwargs)['item']
    
    def delete(self):
        """Delete the CustomFieldValue"""
        self.endpoints.deleteCustomFieldValue(
            cardId=self.schema['cardId'],
            customFieldGroupId=self.schema['customFieldGroupId'],
            customFieldId=self.schema['customFieldId'],
        )

LabelColor = Literal[
    'muddy-grey', 'autumn-leafs', 'morning-sky', 'antique-blue', 
    'egg-yellow', 'desert-sand', 'dark-granite', 'fresh-salad', 
    'lagoon-blue', 'midnight-blue', 'light-orange', 'pumpkin-orange', 
    'light-concrete', 'sunny-grass', 'navy-blue', 'lilac-eyes', 
    'apricot-red', 'orange-peel', 'silver-glint', 'bright-moss', 
    'deep-ocean', 'summer-sky', 'berry-red', 'light-cocoa', 'grey-stone', 
    'tank-green', 'coral-green', 'sugar-plum', 'pink-tulip', 'shady-rust', 
    'wet-rock', 'wet-moss', 'turquoise-sea', 'lavender-fields', 'piggy-red', 
    'light-mud', 'gun-metal', 'modern-green', 'french-coast', 'sweet-lilac', 
    'red-burgundy', 'pirate-gold',
]
LabelColors: tuple[LabelColor] = LabelColor.__args__

class Label(PlankaModel[schemas.Label]):
    """Python interface for Planka Labels"""
    
    @property
    def board(self) -> Board:
        """The Board the Label belongs to"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)
    
    @property
    def position(self) -> int:
        """Position of the Label within the Board"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Set the position of the Label within the Board"""
        self.update()

    @property
    def name(self) -> str:
        """Name/title of the Label"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the name/title of the Label"""
        self.update(name=name)

    @property
    def color(self) -> LabelColor: 
        """Color of the label"""
        return self.schema['color']
    @color.setter
    def color(self, color: LabelColor) -> None:
        """Set the Label color"""
        self.update(color=color)

    @property
    def created_at(self) -> datetime:
        """When the label was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the label was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    # Special Methods
    def sync(self):
        """Sync the Label with the Planka server"""
        _lbls = [l for l in self.board.labels if l == self]
        if _lbls:
            self.schema = _lbls.pop().schema

    def update(self, **kwargs: Unpack[paths.Request_updateLabel]):
        """Update the Label"""
        self.schema = self.endpoints.updateLabel(self.id, **kwargs)['item']

    def delete(self):
        """Delete the Label"""
        return self.endpoints.deleteLabel(self.id)


ListColor = Literal[
    'berry-red', 'pumpkin-orange', 'lagoon-blue', 'pink-tulip', 
    'light-mud', 'orange-peel', 'bright-moss', 'antique-blue', 
    'dark-granite', 'turquoise-sea',
]
ListColors: tuple[ListColor] = ListColor.__args__

class List(PlankaModel[schemas.List]):
    """Python interface for Planka Lists"""
    
    # List Included
    @property
    def _included(self):
        return self.endpoints.getList(self.id)['included']
    @property
    def users(self) ->  list[User]:
        """Users associated with the List"""
        return [User(u, self.session) for u in self._included['users']]
    
    @property
    def cards(self) -> list[Card]:
        """Cards associated with the List"""
        return [Card(c, self.session) for c in self._included['cards']]
    
    @property
    def card_memberships(self) -> list[CardMembership]:
        """CardMemberships associated with the List"""
        return [CardMembership(cm, self.session) for cm in self._included['cardMemberships']]
    
    @property
    def card_labels(self) -> list[CardLabel]:
        """CardLabels associated with the List"""
        return [CardLabel(cl, self.session) for cl in self._included['cardLabels']]
    
    @property
    def task_lists(self) -> list[TaskList]:
        """TaskLists associated with the List"""
        return [TaskList(tl, self.session) for tl in self._included['taskLists']]
    
    @property
    def tasks(self) ->  list[Task]:
        """Tasks associated with the List"""
        return [Task(t, self.session) for t in self._included['tasks']]

    @property
    def attachments(self) -> list[Attachment]:
        """Attachments associated with the List"""
        return [Attachment(a, self.session) for a in self._included['attachments']]

    @property
    def custom_field_groups(self) ->  list[CustomFieldGroup]:
        """CustomFieldGroups associated with the List"""
        return [CustomFieldGroup(cfg, self.session) for cfg in self._included['customFieldGroups']]

    @property
    def custom_fields(self) ->  list[CustomField]:
        """CustomFields associated with the List"""
        return [CustomField(cf, self.session) for cf in self._included['customFields']]

    @property
    def custom_field_values(self) -> list[CustomFieldValue]:
        """CustomFieldValues associated with the List"""
        return [CustomFieldValue(cfv, self.session) for cfv in self._included['customFieldValues']]

    # List Properties
    @property
    def board(self) -> Board:
        """The Board the List belongs to"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)
    
    @property
    def type(self): 
        """Type/status of the list"""
        return self.schema['type']
    @type.setter
    # ['archive', 'trash'] are system types and cannot be set
    def type(self, type: Literal['active', 'closed']) -> None:
        """Set the List type"""
        self.update(type=type)
    
    @property 
    def position(self) -> int:
        """Position of the List within the Board"""
        return self.schema['position']

    @property
    def name(self) -> str:
        """Name/title of the List"""
        return self.schema['name']
    
    @property
    def color(self) -> ListColor:
        """Color for the List"""
        return self.schema['color']
    @color.setter
    def color(self, color: ListColor | None) -> None:
        """Set the List color"""
        self.update(color=color)

    @property    
    def created_at(self) -> datetime:
        """When the List was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the List was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    # Special Methods
    def sync(self):
        """Sync the List with the Planka server"""
        self.schema = self.endpoints.getList(self.id)['item']
    
    def update(self, **list: Unpack[paths.Request_updateList]):
        """Update the List"""
        self.endpoints.updateList(self.id, **list)
    
    def delete(self):
        """Delete the List"""
        return self.endpoints.deleteList(self.id)

    def create_card(self, **crd: Unpack[paths.Request_createCard]) -> Card:
        """Create a new card in the List"""
        return Card(self.endpoints.createCard(self.id, **crd)['item'], self.session)
    
    def sort_cards(self, **kwargs: Unpack[paths.Request_sortList]) -> list[Card]:
        """Sort all cards in the List and return the sorted Cards"""
        return [Card(c, self.session) for c in self.endpoints.sortList(self.id, **kwargs)['included']['cards']]
    
    def archive_cards(self) -> None:
        """Move all cards in the List to the Board archive"""
        if self.type != 'closed':
            raise TypeError(f'List {self.name} in Board {self.board.name} is type: {self.type}, must be a `closed` type')
        self.endpoints.moveListCards(self.id, listId=self.board.archive_list.id)['item']

    def delete_cards(self) -> None:
        """Delete all Cards in the List (must be a trash list)"""
        if self.type != 'trash':
            raise TypeError(f'Only trash type lists can be deleted')
        self.endpoints.clearList(self.id)['item']
    
    def move_cards(self, list: List, position: Literal['top', 'bottom'] | int='top') -> None:
        """Move all Cards in this List to another List"""
        for c in self.cards:
            c.move(list, position)

NotificationType = Literal['moveCard', 'commentCard', 'addMemberToCard', 'mentionInComment']
NotificationTypes: tuple[NotificationType] = NotificationType.__args__

class Notification(PlankaModel[schemas.Notification]):
    """Python interface for Planka Notifications"""
    
    # Notification included
    @property
    def _included(self):
        return self.endpoints.getNotification(self.id)['included']
    
    @property
    def users(self) -> list[User]:
        """All Users associated with the Notification"""
        return [User(u, self.session) for u in self._included['users']]
    
    # Notification props
    @property
    def user(self) -> User:
        """The User who receives the Notification"""
        return [u for u in self.users if self.schema['userId'] == u.id].pop()
    
    @property
    def creator(self) -> User:
        """The User who created the Notification"""
        return [u for u in self.users if self.schema['creatorUserId'] == u.id].pop()
        
    @property
    def board(self) -> Board:
        """The Board associated with the Notification (denormalized)"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)
    
    @property
    def card(self) -> Card:
        """The Card associated with the Notification"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def comment(self) -> Comment:
        """The Comment associated with the Notification"""
        return [c for c in self.card.comments if c.id == self.schema['commentId']].pop()
    
    @property
    def action(self) -> Action:
        """The Action associated with the Notification"""
        return [a for a in self.card.actions if a.id == self.schema['actionId']].pop()
        
    @property
    def type(self) -> NotificationType:
        """Type of the Notification"""
        return self.schema['type']
    
    @property
    def data(self) -> dict[str, Any]:
        """Notification specific data (varies by type)"""
        return self.schema['data']
        
    @property
    def is_read(self) -> bool:
        """Whether the Notification has been read"""
        return self.schema['isRead']
    @is_read.setter
    def is_read(self, is_read: bool) -> None:
        """Set the read status of the Notification"""
        self.update(isRead=is_read)
    
    @property
    def created_at(self) -> datetime:
        """When the Notification was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the Notification was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    # Special Methods
    def sync(self):
        """Sync the Notification with the Planka server"""
        self.schema = self.endpoints.getNotification(self.id)['item']
 
    def update(self, **kwargs: Unpack[paths.Request_updateNotification]) -> None:
        """Update the Notification"""
        self.schema = self.endpoints.updateNotification(self.id, **kwargs)['item']

NotificationServiceFormat = Literal['text', 'markdown', 'html']
NotificationServiceFormats: tuple[NotificationServiceFormat] = NotificationServiceFormat.__args__
  
class NotificationService(PlankaModel[schemas.NotificationService]):
    """Python interface for Planka NotificationServices"""
        
    # NotificationService props
    
    @property
    def user(self) -> User:
        """The User the NotificationService is associated with"""
        return [u for u in self.board.users if self.schema['userId'] == u.id].pop()
    
    @property
    def board(self) -> Board:
        """The Board the NotificationService is associated with"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)

    @property
    def url(self) -> str:
        """URL endpoint for Notifications"""
        return self.schema['url']
    
    @property
    def format(self) -> NotificationServiceFormat: 
        """Format for notification messages"""
        return self.schema['format']
    
    @property
    def created_at(self) -> datetime:
        """When the NotificationService was created"""
        return datetime.fromisoformat(self.schema['createdAt'])

    @property
    def updated_at(self) -> datetime:
        """When the NotificationService was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    # Special Methods
    def sync(self):
        """Sync the NotificationService with the Planka server"""
        _nss = [ns for ns in self.board.project.notification_services if ns == self]
        if _nss:
            self.schema = _nss.pop().schema
        
    def update(self, **kwargs: Unpack[paths.Request_updateNotificationService]):
        """Update the NotificationService"""
        self.schema = self.endpoints.updateNotificationService(self.id, **kwargs)['item']
    
    def delete(self):
        """Delete the NotificationService"""
        self.endpoints.deleteNotificationService(self.id)

# Valid Gradients
BackgroundGradient = Literal[
    'old-lime', 'ocean-dive', 'tzepesch-style', 'jungle-mesh', 
    'strawberry-dust', 'purple-rose', 'sun-scream', 'warm-rust', 
    'sky-change', 'green-eyes', 'blue-xchange', 'blood-orange', 
    'sour-peel', 'green-ninja', 'algae-green', 'coral-reef', 
    'steel-grey', 'heat-waves', 'velvet-lounge', 'purple-rain', 
    'blue-steel', 'blueish-curve', 'prism-light', 'green-mist', 
    'red-curtain'
]
BackgroundGradients = BackgroundGradient.__args__

class Project(PlankaModel[schemas.Project]):
    """Python interface for Planka Projects"""
    
    # Project Included
    @property
    def _included(self):
        return self.endpoints.getProject(self.id)['included']
    
    @property
    def users(self) -> list[User]:
        """Get Users associated with the Project"""
        return [User(u, self.session) for u in self._included['users']]
    @property
    def managers(self) -> list[ProjectManager]:
        """Get project manager Users associated with the Project"""
        return [ProjectManager(pm, self.session) for pm in self._included['projectManagers']]
    @property
    def background_images(self) -> list[BackgroundImage]:
        """Get BackgroundImages associated with the Project"""
        return [BackgroundImage(bgi, self.session) for bgi in self._included['backgroundImages']]
    @property
    def base_custom_field_groups(self) -> list[BaseCustomFieldGroup]:
        """Get BaseCustomFieldGroups associated with the Project"""
        return [BaseCustomFieldGroup(bcfg, self.session) for bcfg in self._included['baseCustomFieldGroups']]
    @property
    def boards(self) -> list[Board]:
        """Get Boards associated with the Project"""
        return [Board(b, self.session) for b in self._included['boards']]
    @property
    def board_memberships(self) -> list[BoardMembership]:
        """Get BoardMemberships associated with the Project"""
        return [BoardMembership(bm, self.session) for bm in self._included['boardMemberships']]
    @property
    def custom_fields(self) -> list[CustomField]:
        """Get CustomFields associated with the Project"""
        return [CustomField(cf, self.session) for cf in self._included['customFields']]
    @property
    def notification_services(self) -> list[NotificationService]:
        """Get NotificationServices associated with the Project"""
        return [NotificationService(ns, self.session) for ns in self._included['notificationServices']]
    
    # Project Properties
    @property
    def favorite(self) -> bool:
        """Whether the project is in the current User's favorites"""
        return self.endpoints.getProject(self.id)['item']['isFavorite']
    @favorite.setter
    def favorite(self, is_favorite: bool) -> None:
        """Set/Unset the Project in the current User's favorites"""
        self.update(isFavorite=is_favorite)
        
    @property
    def owner(self) -> User:
        """The User who owns the project (Raises LookupError if the User cannot be found)"""
        _usrs = [u for u in self.users if self.schema['ownerProjectManagerId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find user: {self.schema['ownerProjectManagerId']}")

    @property
    def background_image(self) -> BackgroundImage | None:
        """The current BackgroundImage of the Project"""
        bgis = [bgi for bgi in self.background_images if bgi.id == self.schema['backgroundImageId']]
        if not bgis:
            return None
        return bgis.pop()
    @background_image.setter
    def background_image(self, background_image: BackgroundImage | None) -> None:
        """Set the Project BackgroundImage"""
        if background_image is None:
            self.remove_background()
        else:
            self.update(backgroundImageId=background_image.id, backgroundType='image')
    
    @property
    def name(self) -> str:
        """Name/title of the Project"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the Project name"""
        self.update(name=name)
        
    @property
    def description(self) -> str:
        """Detailed description of the Project"""
        return self.schema['description']
    @description.setter
    def description(self, description: str) -> None:
        """Set the Project description"""
        self.update(description=description)
    
    @property
    def background_type(self):
        """Type of background for the project"""
        return self.schema['backgroundType']
    @background_type.setter
    def background_type(self, type: Literal['gradient', 'image']):
        """Set the background type"""
        self.update(backgroundType=type)
        
    @property
    def background_gradient(self) -> BackgroundGradient | None:
        """Gradient background for the project"""
        return self.schema['backgroundGradient']
    @background_gradient.setter
    def background_gradient(self, gradient: BackgroundGradient | None) -> None:
        """Set the Project background gradient"""
        if gradient is None:
            self.remove_background()
        else:
            self.update(backgroundGradient=gradient, backgroundType='gradient')
    
    @property
    def hidden(self) -> bool:
        """Whether the project is hidden"""
        return self.schema['isHidden']
    @hidden.setter
    def hidden(self, is_hidden: bool) -> None:
        """Set/Unset the Project as hidden"""
        self.update(isHidden=is_hidden)
    
    @property
    def created_at(self) -> datetime:
        """When the project was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the project was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    # Special Methods
    def sync(self):
        self.schema = self.endpoints.getProject(self.id)['item']
        
    def update(self, **project: Unpack[paths.Request_updateProject]) -> None:
        """Update the Project"""
        self.schema = self.endpoints.updateProject(self.id, **project)['item']
        
    def delete(self) -> None:
        """Delete the Project"""
        self.endpoints.deleteProject(self.id)
    
    def add_project_manager(self, user: User) -> ProjectManager:
        """Add a User to the Project as a ProjectManager"""
        return ProjectManager(self.endpoints.createProjectManager(self.id, userId=user.id)['item'], self.session)
    
    def remove_background(self) -> None:
        """Reset the Project background to the default grey"""
        self.update(backgroundType=None) # type: ignore

    def remove_project_manager(self, project_manager: ProjectManager | User) -> None:
        """Remove a ProjectManager from the Project"""
        if isinstance(project_manager, User):
            # Get the ProjectManager object for the User
            for pm in self.managers:
                if pm.user == project_manager:
                    project_manager = pm
                    break
            else:
                # If User not in managers, do nothing
                return
        
        if project_manager.project == self:
            # Only delete ProjectManager if it is for this Project
            # Defer deletion to the ProjectManager object
            project_manager.delete()

    def create_board(self, **board: Unpack[paths.Request_createBoard]) -> Board:
        """Create a new Board in the Project"""
        return Board(self.endpoints.createBoard(self.id, **board)['item'], self.session)

    def create_base_custom_field_group(self, **bcfg: Unpack[paths.Request_createBaseCustomFieldGroup]) -> BaseCustomFieldGroup:
        """Create a BaseCustomFieldGroup in the Project"""
        return BaseCustomFieldGroup(self.endpoints.createBaseCustomFieldGroup(self.id, **bcfg)['item'], self.session)


class ProjectManager(PlankaModel[schemas.ProjectManager]):
    """Python interface for Planka ProjectManagers"""
    
    # ProjectManager Properties
    @property
    def project(self) -> Project:
        """The Project associated with the ProjectManager"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)
    @property
    def user(self) -> User:
        """The User assigned as ProjectManager (Raises LookupError if the User cannot be found)"""
        _usrs = [u for u in self.project.users if self.schema['userId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['userId']}")
    
    @property
    def created_at(self) -> datetime:
        """When the ProjectManager was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the ProjectManager was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])
    
    # Special Methods
    def sync(self):
        """Sync the ProjectManager with the Planka server"""
        pms = self.project.managers
        for pm in pms:
            if pm.id == self.id:
                self.schema = pm.schema
                
    def delete(self):
        self.endpoints.deleteProjectManager(self.id)

   
class Task(PlankaModel[schemas.Task]):
    """Python interface for Planka Tasks"""

    # Task props

    @property
    def task_list(self) -> TaskList:
        """The TaskList the Task belongs to"""
        return TaskList(self.endpoints.getTaskList(self.schema['taskListId'])['item'], self.session)
    @task_list.setter
    def task_list(self, task_list: TaskList) -> None:
        """Move the Task to a different TaskList"""
        self.update(taskListId=task_list.id)

    @property
    def card(self) -> Card:
        """The Card the Task is linked to"""
        return Card(self.endpoints.getCard(self.schema['linkedCardId'])['item'], self.session)

    @property
    def assignee(self) -> User | None:
        """The User assigned to the Task if there is one"""
        _usrs = [u for u in self.card.board.users if self.schema['assigneeUserId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['assigneeUserId']}")
    @assignee.setter
    def assignee(self, assignee: User | None) -> None:
        """Assign a User to the Task"""
        # TODO: Fix _build to add <Type> | None to `nullable` fields
        if assignee is not None:
            self.update(assigneeUserId=assignee.id)
        else:
            self.update(assigneeUserId=None) # type: ignore

    @property
    def position(self) -> int:
        """Position of the Task within the TaskList"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Set the position of the Task within the TaskList"""

    @property
    def name(self) -> str:
        """Name/title of the Task"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the Task name"""
        self.update(name=name)

    @property
    def is_completed(self) -> bool:
        """Whether the Task is completed"""
        return self.schema['isCompleted']
    @is_completed.setter
    def is_completed(self, is_completed: bool) -> None: 
        """Set whether the Task is completed"""
        self.update(isCompleted=is_completed)

    @property
    def created_at(self) -> datetime:
        """When the Task was created"""
        return datetime.fromisoformat(self.schema['createdAt'])

    @property
    def updated_at(self) -> datetime:
        """When the Task was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    # Special Methods
    def sync(self):
        """Sync the Task with the Planka server"""
        _tsks = [tsk for tsk in self.task_list.tasks if tsk == self]
        if _tsks:
            self.schema = _tsks.pop().schema

    def update(self, **kwargs: Unpack[paths.Request_updateTask]):
        """Update the Task"""
        self.schema = self.endpoints.updateTask(self.id, **kwargs)['item']

    def delete(self):
        """Delete the Task"""
        self.endpoints.deleteTask(self.id)

 
class TaskList(PlankaModel[schemas.TaskList]):
    """Python interface for Planka TaskLists"""
    
    # TaskList included

    @property
    def _included(self):
        return self.endpoints.getTaskList(self.id)['included']
    
    @property
    def tasks(self) -> list[Task]:
        """All Tasks associated with the TaskList"""
        return [Task(t, self.session) for t in self._included['tasks']]

    # TaskList props

    @property
    def card(self) -> Card:
        """The Card the TaskList belongs to"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def position(self) -> int:
        """Position of the TaskList within the Card"""
        return self.schema['position']
    @position.setter
    def positon(self, position: int) -> None:
        """Set the TaskList position within the Card"""
        self.update(position=position)

    @property
    def name(self) -> str:
        """Name/title of the TaskList"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the TaskList"""
        self.update(name=name)

    @property
    def show_on_front_of_card(self) -> bool:
        """Whether to show the TaskList on the front of the Card"""
        return self.schema['showOnFrontOfCard']
    @show_on_front_of_card.setter
    def show_on_front_of_card(self, show_on_front_of_card: bool) -> None:
        """Set whether to show TaskList on the front of the Card"""

    @property
    def hide_completed_tasks(self) -> bool:
        """Whether to hide completed Tasks"""
        return self.schema['hideCompletedTasks']
    @hide_completed_tasks.setter
    def hide_completed_tasks(self, hide_completed_tasks: bool) -> None:
        """Set whether to hide completed Tasks"""
        self.update(hideCompletedTasks=hide_completed_tasks)

    @property
    def created_at(self) -> datetime:
        """When the TaskList was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the TaskList was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    # Special Methods
    def sync(self):
        """Sync the TaskList with the Planka server"""
        self.schema = self.endpoints.getTaskList(self.id)['item']

    def update(self, **kwargs: Unpack[paths.Request_updateTaskList]):
        """Update the TaskList"""
        self.schema = self.endpoints.updateTaskList(self.id, **kwargs)['item']

    def delete(self):
        """Delete the TaskList"""
        self.endpoints.deleteTaskList(self.id)

    def add_task(self, name: str, *, 
                 is_completed: bool=False, 
                 position: Literal['top', 'bottom'] | int='bottom') -> Task:
        """Create a new Task in the TaskList"""
        if not isinstance(position, int):
            if position == 'top':
                position = 0
            else:
                # Find nest slot for 'bottom' (or any other invalid option)
                position = max((t.position for t in self.tasks), default=0) + 1

        return Task(self.endpoints.createTask(
                self.id, 
                linkedCardId=self.card.id, 
                name=name, 
                position=position, 
                isCompleted=is_completed
            )['item'], 
            self.session
        )


# User Literals
Language = Literal[
    'ar-YE', 'bg-BG', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US', 
    'es-ES', 'et-EE', 'fa-IR', 'fi-FI', 'fr-FR', 'hu-HU', 'id-ID', 'it-IT', 
    'ja-JP', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 
    'sk-SK', 'sr-Cyrl-RS', 'sr-Latn-RS', 'sv-SE', 'tr-TR', 'uk-UA', 'uz-UZ', 
    'zh-CN', 'zh-TW',
]
Languages: tuple[Language] = Language.__args__

EditorMode = Literal['wysiwyg', 'markup']
EditorModes: tuple[EditorMode] = EditorMode.__args__

HomeView = Literal['gridProjects', 'groupedProjects']
HomeViews: tuple[HomeView] = HomeView.__args__

ProjectOrdering = Literal['byDefault', 'alphabetically', 'byCreationTime']
ProjectOrderings: tuple[ProjectOrdering] = ProjectOrdering.__args__

TermsType = Literal['general', 'extended']
TermsTypes: tuple[TermsType] = TermsType.__args__

LockableField = Literal['email', 'password', 'name']
LockableFields: tuple[LockableField] = LockableField.__args__

class User(PlankaModel[schemas.User]):
    """Python interface for Planka Users"""

    @property
    def email(self) -> str | None:
        """Email address for login and notifications (private field)"""
        return self.schema.get('email')
    @email.setter
    def email(self, email: str) -> None:
        """Set the User email (Direct assignment only allowed for Admin users)"""
        self.endpoints.updateUserEmail(self.id, email=email)

    @property
    def password(self) -> None:
        raise AttributeError(f'Passwords can only be set by Admin Users and read by nobody')
    @password.setter
    def password(self, password: str) -> None:
        """Set a User's password (Admin only)"""
        self.endpoints.updateUserPassword(self.id, password=password)

    @property
    def role(self):
        """User role defining access permissions"""
        return self.schema['role']
    @role.setter
    def role(self, role: Literal['admin', 'projectOwner', 'boardUser']) -> None:
        """Set the User role"""
        self.update(role=role)

    @property
    def name(self) -> str:
        """Full display name of the user"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the User's name"""
        self.update(name=name)

    @property
    def username(self) -> str:
        """Unique username for user identification"""
        return self.schema['username']
    @name.setter
    def name(self, name: str) -> None:
        """Set the User's username"""
        self.update(name=name)

    @property
    def avatar(self) -> dict[str, Any]:
        """Avatar information for the user with generated URLs"""
        return self.schema['avatar']
    @avatar.setter
    def avatar(self, avatar: Any) -> None:
        """Set the User's avatar"""
        raise NotImplementedError('Avatar setting has not been implemented') 
    
    @property
    def gravatar_url(self) -> str | None:
        """Gravatar URL for the user (conditionally added if configured)"""
        return self.schema.get('gravatarUrl')
    
    @property
    def phone(self) -> str:
        """Contact phone number"""
        return self.schema['phone']
    @phone.setter
    def phone(self, phone: str) -> None:
        """Set the User's phone"""
        self.update(phone=phone)

    @property
    def organization(self) -> str:
        """Organization or company name"""
        return self.schema['organization']
    @organization.setter
    def organization(self, organization: str) -> None:
        """Set the User's organization"""
        self.update(organization=organization)

    @property
    def language(self) -> Language | None:
        """Preferred language for user interface and notifications (personal field)"""
        return self.schema.get('language')
    @language.setter
    def language(self, language: Language) -> None:
        """Set the User's language"""
        self.update(language=language)

    @property
    def subscribe_to_own_cards(self) -> bool:
        """Whether the user subscribes to their own cards (personal field)"""
        return self.schema.get('subscribeToOwnCards', False)
    @subscribe_to_own_cards.setter
    def subscribe_to_own_cards(self, subscribe_to_own_cards: bool) -> None:
        """Set Whether the user subscribes to their own cards (personal field)"""
        self.update(subscribeToOwnCards=subscribe_to_own_cards)

    @property
    def subscribe_to_card_when_commenting(self) -> bool:
        """Whether the user subscribes to cards when commenting (personal field)"""
        return self.schema.get('subscribeToCardWhenCommenting', False)
    @subscribe_to_card_when_commenting.setter
    def subscribe_to_card_when_commenting(self, subscribe_to_card_when_commenting: bool) -> None:
        """Set whether the user subscribes to cards when commenting (personal field)"""
        self.update(subscribeToCardWhenCommenting=subscribe_to_card_when_commenting)

    @property
    def turn_off_recent_card_highlighting(self) -> bool:
        """Whether recent card highlighting is disabled (personal field)"""
        return self.schema.get('turnOffRecentCardHighlighting', False)
    @turn_off_recent_card_highlighting.setter
    def turn_off_recent_card_highlighting(self, turn_off_recent_card_highlighting: bool) -> None:
        """Set whether recent card highlighting is disabled (personal field)"""
        self.update(turnOffRecentCardHighlighting=turn_off_recent_card_highlighting)

    @property
    def enable_favorites_by_default(self) -> bool:
        """Whether favorites are enabled by default (personal field)"""
        return self.schema.get('enableFavoritesByDefault', False)
    @enable_favorites_by_default.setter
    def enable_favorites_by_default(self, enable_favorites_by_default: bool) -> None:
        """Set whether favorites are enabled by default (personal field)"""
        self.update(enableFavoritesByDefault=enable_favorites_by_default)

    @property
    def default_editor_mode(self) -> EditorMode:
        """Default markdown editor mode (personal field)"""
        return self.schema.get('defaultEditorMode', 'wysiwyg')
    @default_editor_mode.setter
    def default_editor_mode(self, default_editor_mode: EditorMode) -> None:
        """Set default markdown editor mode (personal field)"""
        self.update(defaultEditorMode=default_editor_mode)

    @property
    def default_home_view(self) -> HomeView | None:
        """Default view mode for the home page (personal field)"""
        return self.schema.get('defaultHomeView')
    @default_home_view.setter
    def default_home_view(self, default_home_view: HomeView) -> None:
        """Default view mode for the home page (personal field)"""
        self.update(defaultHomeView=default_home_view)

    @property
    def default_projects_order(self) -> ProjectOrdering | None:
        """Default sort order for projects display (personal field)"""
        return self.schema.get('defaultProjectsOrder')
    @default_projects_order.setter
    def default_projects_order(self, default_projects_order: ProjectOrdering) -> None:
        """Default sort order for projects display (personal field)"""
        self.update(defaultProjectsOrder=default_projects_order)
    
    @property
    def terms_type(self) -> TermsType:
        """Type of terms applicable to the user based on role"""
        return self.schema['termsType']
    
    @property
    def is_sso_user(self) -> bool:
        """Whether the user is SSO user (private field)"""
        return self.schema.get('isSsoUser', False)
    
    @property
    def is_deactivated(self) -> bool:
        """Whether the user account is deactivated and cannot log in"""
        return self.schema['isDeactivated']
    
    @property
    def is_default_admin(self) -> bool:
        """Whether the user is the default admin (visible only to current user or admin)"""
        return self.schema.get('isDefaultAdmin', False)
    
    @property
    def locked_field_names(self) -> list[LockableField]:
        """List of fields locked from editing (visible only to current user or admin)"""
        return self.schema.get('lockedFieldNames', [])
    
    @property
    def created_at(self) -> datetime:
        """When the user was created"""
        return datetime.fromisoformat(self.schema['createdAt'])
    
    @property
    def updated_at(self) -> datetime:
        """When the user was last updated"""
        return datetime.fromisoformat(self.schema['updatedAt'])

    # Special Methods
    def sync(self):
        """Sync the User with the Planka server (Can only sync your own User)"""
        if self.id == self.session.me.id:
            self.schema = self.session.me.schema

    def update(self, **kwargs: Unpack[paths.Request_updateUser]):
        """Update the User"""
        self.schema = self.endpoints.updateUser(self.id, **kwargs)['item']

    def delete(self):
        """Delete the User"""
        return self.endpoints.deleteUser(self.id)
    
    def update_email(self, email: str, *, password: str|None=None) -> None:
        """Update the current User's email (requires password)"""
        # Allow Admins to set user email directly or ignore password kwarg
        if not password:
            self.endpoints.updateUserEmail(self.id, email=email)
        else:
            self.endpoints.updateUserEmail(self.id, email=email, currentPassword=password)

    def update_password(self, *, new_password: str, current_password: str|None=None) -> None:
        """Update the current User's password (requires current password)"""
        # Allow Admins to set user passwords by ignoring current password
        # or setting password property directly
        if not current_password:
            self.endpoints.updateUserPassword(self.id, password=new_password)
        else:
            self.endpoints.updateUserPassword(self.id, password=new_password, currentPassword=current_password)

    def add_to_card(self, card: Card) -> None:
        """Add the User to a Card"""
        self.endpoints.createCardMembership(card.id, userId=self.id)
    
    def add_to_board(self, board: Board, role: BoardRole, *, can_comment: bool=False) -> None:
        """Add the User to a board"""
        if self not in board.users:
            self.endpoints.createBoardMembership(board.id, userId=self.id, role=role, canComment=can_comment)
        _existing_membership = [bm for bm in board.board_memberships if bm.user == self].pop()
        if _existing_membership.role != role or _existing_membership.can_comment != can_comment:
            if role == 'viewer':
                _existing_membership.update(role=role, canComment=can_comment)
            else:
                _existing_membership.update(role=role)


class Webhook(PlankaModel[schemas.Webhook]):
    """Python interface for Planka Webhooks"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

  
# Special Interfaces
class Stopwatch:
    """Python interface for Planka Stopwatches"""

    def __init__(self, card: Card) -> None:
        self.card = card
        if not card.schema['stopwatch']:
            # Add a stopwatch
            ...
    
    def start(self) -> datetime: ...
    def stop(self) -> datetime: ...
    def duration(self) -> int: ...
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...