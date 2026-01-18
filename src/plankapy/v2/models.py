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
    PlankaEndpoints,
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
    "CardLabel", #TODO
    "CardMembership", #TODO
    "Comment", #TODO
    "Config", #TODO
    "CustomField", #TODO
    "CustomFieldGroup", #TODO
    "CustomFieldValue", #TODO
    "Label", #TODO
    "List", #TODO
    "Notification", #TODO
    "NotificationService", #TODO
    "Project",
    "ProjectManager",
    "Task", #TODO
    "TaskList", #TODO
    "User",
    "Webhook", #TODO
)

_S = TypeVar('_S', bound=Mapping[str, Any])
class PlankaModel(Generic[_S]):
    """Base Planka object interface"""
    
    def __init__(self, schema: _S, endpoints: PlankaEndpoints) -> None:
        self._schema = schema
        self.endpoints = endpoints
        self.client = self.endpoints.client
        self._live_mode = False
    
    @property
    def schema(self) -> _S:
        return self._schema
    @schema.setter
    def schema(self, schema: _S) -> None:
        self._schema = schema
    
    @property
    def live_mode(self) -> bool:
        return self._live_mode
    @live_mode.setter
    def live_mode(self, enabled: bool) -> None:
        self._live_mode = enabled
    
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
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.endpoints)
    @property
    def board(self) -> Board:
        """The Board where the Action occurred"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.endpoints)
    @property
    def user(self) -> User:
        """The User who performed the Action"""
        return User(self.endpoints.getUser(self.schema['userId'])['item'], self.endpoints)
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
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.endpoints)
    @property
    def creator(self) -> User:
        """The User created the Attachment"""
        return User(self.endpoints.getUser(self.schema['creatorUserId'])['item'], self.endpoints)
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
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.endpoints)
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
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.endpoints)

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
CardType = Literal['project', 'story']

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
        return [Label(l, self.endpoints) for l in self._included['labels']]
    @property
    def cards(self) -> list[Card]:
        """Get all Cards on the Board"""
        return [Card(c, self.endpoints) for c in self._included['cards']]
    @property
    def subscribed_cards(self) -> list[Card]:
        """Get all Cards on the Board that the current User is subscribed to"""
        return [Card(sc, self.endpoints) for sc in self._included['cards'] if sc['isSubscribed']]
    @property
    def projects(self) -> list[Project]:
        """Get all Projects that the Board is associated with (use `Board.Project` instead, this is always one item)"""
        return [Project(p, self.endpoints) for p in self._included['projects']]
    @property
    def board_memberships(self) -> list[BoardMembership]:
        """Get all BoardMemberships for the Board"""
        return [BoardMembership(bm, self.endpoints) for bm in self._included['boardMemberships']]
    @property
    def lists(self) -> list[List]:
        """Get all Lists associated with the Board"""
        return [List(l, self.endpoints) for l in self._included['lists']]
    @property
    def card_memberships(self) -> list[CardMembership]:
        """Get all CardMemberships associated with the Board"""
        return [CardMembership(cm, self.endpoints) for cm in self._included['cardMemberships']]
    @property
    def card_labels(self) -> list[CardLabel]:
        """Get all CardLabels associated with the Board"""
        return [CardLabel(cl, self.endpoints) for cl in self._included['cardLabels']]
    @property
    def task_lists(self) -> list[TaskList]:
        """Get all TaskLists associated with the Board"""
        return [TaskList(tl, self.endpoints) for tl in self._included['taskLists']]
    @property
    def tasks(self) -> list[Task]:
        """Get all Tasks associated with the Board"""
        return [Task(t, self.endpoints) for t in self._included['tasks']]
    @property
    def attachments(self) -> list[Attachment]:
        """Get all Attachments associated with the Board"""
        return [Attachment(a, self.endpoints) for a in self._included['attachments']]
    @property
    def custom_field_groups(self) -> list[CustomFieldGroup]:
        """Get all CustomFieldGroups associated with the Board"""
        return [CustomFieldGroup(cfg, self.endpoints) for cfg in self._included['customFieldGroups']]
    @property
    def custom_fields(self) -> list[CustomField]:
        """Get all CustomFields associated with the Board"""
        return [CustomField(cf, self.endpoints) for cf in self._included['customFields']]
    @property
    def custom_field_values(self) -> list[CustomFieldValue]:
        """Get all CustomFieldValues associated with the Board"""
        return [CustomFieldValue(cfv, self.endpoints) for cfv in self._included['customFieldValues']]
    
    # Board props
    @property
    def subscribed(self) -> bool:
        """Whether the current user is subscribed to the Board"""
        return self.endpoints.getBoard(self.id)['item']['isSubscribed']
    
    @property
    def project_id(self) -> Project:
        """TheProject the Board belongs to"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.endpoints)
    
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


class BoardMembership(PlankaModel[schemas.BoardMembership]):
    """Python interface for Planka BoardMemberships"""


    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...


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
        return [Attachment(a, self.endpoints) for a in self._included['attachments']]
    @property
    def card_memberships(self) -> list[CardMembership]:
        """Get all CardMemberships associated with the Card"""
        return [CardMembership(cm, self.endpoints) for cm in self._included['cardMemberships']]
    @property
    def members(self) -> list[User]:
        """Get all User members associated with the Card"""
        return [User(u, self.endpoints) for u in self._included['users']]
    @property
    def labels(self) -> list[Label]:
        """Get all Labels associated with the Card"""
        _card_label_ids = [l['id'] for l in self._included['cardLabels']]
        return [l for l in self.board.labels if l.id in _card_label_ids]
    @property
    def tasks(self) -> list[Task]:
        """Get all Tasks associated with the card"""
        return [Task(t, self.endpoints) for t in self._included['tasks']]
    @property
    def task_lists(self) -> list[TaskList]:
        """Get all TaskLists associated with the Card"""
        return [TaskList(tl, self.endpoints) for tl in self._included['taskLists']]
    @property
    def custom_field_groups(self) -> list[CustomFieldGroup]:
        """Get all CustomFieldGroups associated with the Card"""
        return [CustomFieldGroup(cfg, self.endpoints) for cfg in self._included['customFieldGroups']]
    @property
    def custom_fields(self) -> list[CustomField]:
         """Get all CustomFields associated with the Card"""
         return [CustomField(cf, self.endpoints) for cf in self._included['customFields']]
    @property
    def custom_field_values(self) -> list[CustomFieldValue]:
        """Get all CustomFieldValues associated with the Card"""
        return [CustomFieldValue(cfv, self.endpoints) for cfv in self._included['customFieldValues']]
     
    # Card props
    @property
    def subscribed(self) -> bool:
        """If the current user is subscribed to the Card"""
        return self.endpoints.getCard(self.id)['item']['isSubscribed']
    @property
    def board(self) -> Board:
        """The Board the Card belongs to"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.endpoints)
    @property
    def list(self)-> List:
        """The List the Card belongs to"""
        return List(self.endpoints.getList(self.schema['listId'])['item'], self.endpoints)
    @list.setter
    def list(self, list: List) -> Self:
        """Set List the Card belongs to"""
        self.update(listId=list.id, boardId=list.board.id)
        return self

    @property
    def creator(self) -> User:
        """The User who Created the card"""
        return User(self.endpoints.getUser(self.schema['creatorUserId'])['item'], self.endpoints)
    @property
    def prevlist(self) -> List:
        """The previous List the card was in (available when in archive or trash)"""
        return List(self.endpoints.getList(self.schema['prevListId'])['item'], self.endpoints)
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
    def last_moved(self) -> datetime:
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
        """Update the Card"""
        self.schema = self.endpoints.updateCard(self.id, **card)['item']
 
    def delete(self):
        """Delete the Card"""
        return self.endpoints.deleteCard(self.id)

    def move(self, list: List) -> Self:
        """Move the card to a new list
        
        Args:
            list (List): The list to move the card to
        
        Returns:
            Self
        """
        if list.id != self.list.id:
            self.update(listId=list.id)
        return self
    
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
            a = Attachment(r['item'], self.endpoints)
        
        # Attach File
        elif isinstance(attachment, bytes):
            r = self.endpoints.createAttachment(
                self.id, 
                type='file', 
                file=str(attachment), 
                name=name or str(hash(attachment))
            )
            a =  Attachment(r['item'], self.endpoints)
        else:
            raise ValueError(f'Expected str or bytes for Attachment, got {type(attachment)}')

        # Set cover if requested
        if cover:
            self.update(coverAttachmentId=a.id)
        return a


class CardLabel(PlankaModel[schemas.CardLabel]):
    """Python interface for Planka CardLabels"""

    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...


class CardMembership(PlankaModel[schemas.CardMembership]):
    """Python interface for Planka CardMemberships"""

    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

   
class Comment(PlankaModel[schemas.Comment]):
    """Python interface for Planka Comments"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

   
class Config(PlankaModel[schemas.Config]):
    """Python interface for Planka Config"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

  
class CustomField(PlankaModel[schemas.CustomField]):
    """Python interface for Planka CustomFields"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

   
class CustomFieldGroup(PlankaModel[schemas.CustomFieldGroup]):
    """Python interface for Planka CustomFieldGroups"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

  
class CustomFieldValue(PlankaModel[schemas.CustomFieldValue]):
    """Python interface for Planka CustomFieldValues"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

   
class Label(PlankaModel[schemas.Label]):
    """Python interface for Planka Labels"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...


ListColor = Literal[
    'berry-red', 'pumpkin-orange', 'lagoon-blue', 'pink-tulip', 
    'light-mud', 'orange-peel', 'bright-moss', 'antique-blue', 
    'dark-granite', 'turquoise-sea',
]
class List(PlankaModel[schemas.List]):
    """Python interface for Planka Lists"""
    
    # List Included
    @property
    def _included(self):
        return self.endpoints.getList(self.id)['included']
    @property
    def users(self) ->  list[User]:
        """Users associated with the List"""
        return [User(u, self.endpoints) for u in self._included['users']]
    
    @property
    def cards(self) -> list[Card]:
        """Cards associated with the List"""
        return [Card(c, self.endpoints) for c in self._included['cards']]
    
    @property
    def cardMemberships(self) -> list[CardMembership]:
        """CardMemberships associated with the List"""
        return [CardMembership(cm, self.endpoints) for cm in self._included['cardMemberships']]
    
    @property
    def cardLabels(self) -> list[CardLabel]:
        """CardLabels associated with the List"""
        return [CardLabel(cl, self.endpoints) for cl in self._included['cardLabels']]
    
    @property
    def taskLists(self) -> list[TaskList]: ...
    @property
    def tasks(self) ->  list[Task]: ...
    @property
    def attachments(self) -> list[Attachment]: ...
    @property
    def customFieldGroups(self) ->  list[CustomFieldGroup]: ...
    @property
    def customFields(self) ->  list[CustomField]: ...
    @property
    def customFieldValues(self) -> list[CustomFieldValue]: ...
    
    # List Properties
    @property
    def board(self) -> Board:
        """The Board the List belongs to"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.endpoints)
    
    @property
    def type(self): 
        """Type/status of the list"""
        return self.schema['type']
    @type.setter
    # Possibly ['archive', 'trash'] ?
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
    def color(self, color: ListColor) -> None:
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

  
class Notification(PlankaModel[schemas.Notification]):
    """Python interface for Planka Notifications"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

  
class NotificationService(PlankaModel[schemas.NotificationService]):
    """Python interface for Planka NotificationServices"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

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

class Project(PlankaModel[schemas.Project]):
    """Python interface for Planka Projects"""
    
    # Project Included
    @property
    def _included(self):
        return self.endpoints.getProject(self.id)['included']
    
    @property
    def users(self) -> list[User]:
        """Get Users associated with the Project"""
        return [User(u, self.endpoints) for u in self._included['users']]
    @property
    def managers(self) -> list[ProjectManager]:
        """Get project manager Users associated with the Project"""
        return [ProjectManager(pm, self.endpoints) for pm in self._included['projectManagers']]
    @property
    def background_images(self) -> list[BackgroundImage]:
        """Get BackgroundImages associated with the Project"""
        return [BackgroundImage(bgi, self.endpoints) for bgi in self._included['backgroundImages']]
    @property
    def base_custom_field_groups(self) -> list[BaseCustomFieldGroup]:
        """Get BaseCustomFieldGroups associated with the Project"""
        return [BaseCustomFieldGroup(bcfg, self.endpoints) for bcfg in self._included['baseCustomFieldGroups']]
    @property
    def boards(self) -> list[Board]:
        """Get Boards associated with the Project"""
        return [Board(b, self.endpoints) for b in self._included['boards']]
    @property
    def board_memberships(self) -> list[BoardMembership]:
        """Get BoardMemberships associated with the Project"""
        return [BoardMembership(bm, self.endpoints) for bm in self._included['boardMemberships']]
    @property
    def custom_fields(self) -> list[CustomField]:
        """Get CustomFields associated with the Project"""
        return [CustomField(cf, self.endpoints) for cf in self._included['customFields']]
    @property
    def notification_services(self) -> list[NotificationService]:
        """Get NotificationServices associated with the Project"""
        return [NotificationService(ns, self.endpoints) for ns in self._included['notificationServices']]
    
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
        """The User who owns the project"""
        return User(self.endpoints.getUser(self.schema['ownerProjectManagerId'])['item'], self.endpoints)

    @property
    def background_image(self) -> BackgroundImage | None:
        """The current BackgroundImage of the Project"""
        bgis = [bgi for bgi in self.background_images if bgi.id == self.schema['backgroundImageId']]
        if not bgis:
            return None
        return bgis.pop()
    @background_image.setter
    def background_image(self, background_image: BackgroundImage) -> None:
        """Set the Project BackgroundImage"""
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
    def background_gradient(self, gradient: BackgroundGradient) -> None:
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
        return ProjectManager(self.endpoints.createProjectManager(self.id, userId=user.id)['item'], self.endpoints)
    
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
        return Board(self.endpoints.createBoard(self.id, **board)['item'], self.endpoints)

    def create_base_custom_field_group(self, **bcfg: Unpack[paths.Request_createBaseCustomFieldGroup]) -> BaseCustomFieldGroup:
        """Create a BaseCustomFieldGroup in the Project"""
        return BaseCustomFieldGroup(self.endpoints.createBaseCustomFieldGroup(self.id, **bcfg)['item'], self.endpoints)
    
class ProjectManager(PlankaModel[schemas.ProjectManager]):
    """Python interface for Planka ProjectManagers"""
    
    # ProjectManager Properties
    @property
    def project(self) -> Project:
        """The Project associated with the ProjectManager"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.endpoints)
    @property
    def user(self) -> User:
        """The User assigned as ProjectManager"""
        return User(self.endpoints.getUser(self.schema['userId'])['item'], self.endpoints)
    
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
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...

 
class TaskList(PlankaModel[schemas.TaskList]):
    """Python interface for Planka TaskLists"""
    
    # Special Methods
    def sync(self): ...
    def update(self): ...
    def delete(self): ...


# User Literals
Language = Literal[
    'ar-YE', 'bg-BG', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US', 
    'es-ES', 'et-EE', 'fa-IR', 'fi-FI', 'fr-FR', 'hu-HU', 'id-ID', 'it-IT', 
    'ja-JP', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 
    'sk-SK', 'sr-Cyrl-RS', 'sr-Latn-RS', 'sv-SE', 'tr-TR', 'uk-UA', 'uz-UZ', 
    'zh-CN', 'zh-TW',
]
EditorMode = Literal['wysiwyg', 'markup']
HomeView = Literal['gridProjects', 'groupedProjects']
ProjectOrdering = Literal['byDefault', 'alphabetically', 'byCreationTime']
TermsType = Literal['general', 'extended']
LockableField = Literal['email', 'password', 'name']

class User(PlankaModel[schemas.User]):
    """Python interface for Planka Users"""

    @property
    def email(self) -> str | None:
        """Email address for login and notifications (private field)"""
        return self.schema.get('email')
    @email.setter
    def email(self, email: str|None) -> None:
        """Set the User email"""
        self.update()

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
    def termsType(self) -> TermsType:
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
        """Sync the User with the Planka server"""
        self.schema = self.endpoints.getUser(self.id)['item']

    def update(self, **kwargs: Unpack[paths.Request_updateUser]):
        """Update the User"""
        self.schema = self.endpoints.updateUser(self.id, **kwargs)['item']

    def delete(self):
        """Delete the User"""
        return self.endpoints.deleteUser(self.id)


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