from __future__ import annotations

__all__ = ('List', )

from datetime import datetime, timedelta
from random import choice, shuffle
from ._base import PlankaModel
from ._helpers import Position, dtfromiso, dttoiso, get_position, model_list, POSITION_GAP
from ..api import schemas, paths, events
from ._literals import ListColors

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Unpack, Literal, Any
    #from models import *
    from ._literals import UserListType, ListColor, CardType


class List(PlankaModel[schemas.List]):
    """Python interface for Planka Lists"""
    
    __events__ = events.ListEvents

    # List Included
    @property
    def _included(self):
        return self.endpoints.getList(self.id)['included']
    
    @property
    @model_list
    def users(self) ->  list[User]:
        """Users associated with the List"""
        return [User(u, self.session) for u in self._included['users']]
    
    @property
    @model_list
    def cards(self) -> list[Card]:
        """Cards associated with the List"""
        return [Card(c, self.session) for c in self._included['cards']]
    
    @property
    @model_list
    def card_memberships(self) -> list[CardMembership]:
        """CardMemberships associated with the List"""
        return [CardMembership(cm, self.session) for cm in self._included['cardMemberships']]
    
    @property
    @model_list
    def card_labels(self) -> list[CardLabel]:
        """CardLabels associated with the List"""
        return [CardLabel(cl, self.session) for cl in self._included['cardLabels']]
    
    @property
    @model_list
    def task_lists(self) -> list[TaskList]:
        """TaskLists associated with the List"""
        return [TaskList(tl, self.session) for tl in self._included['taskLists']]
    
    @property
    @model_list
    def tasks(self) ->  list[Task]:
        """Tasks associated with the List"""
        return [Task(t, self.session) for t in self._included['tasks']]

    @property
    @model_list
    def attachments(self) -> list[Attachment]:
        """Attachments associated with the List"""
        return [Attachment(a, self.session) for a in self._included['attachments']]

    @property
    @model_list
    def custom_field_groups(self) ->  list[CustomFieldGroup]:
        """CustomFieldGroups associated with the List"""
        return [CustomFieldGroup(cfg, self.session) for cfg in self._included['customFieldGroups']]

    @property
    @model_list
    def custom_fields(self) ->  list[CustomField]:
        """CustomFields associated with the List"""
        return [CustomField(cf, self.session) for cf in self._included['customFields']]

    @property
    @model_list
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
    def type(self, type: UserListType) -> None:
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
    def color(self, color: ListColor | Literal['random'] | None) -> None:
        """Set the List color"""
        if color == 'random':
            color = choice(ListColors)
        self.update(color=color)

    @property    
    def created_at(self) -> datetime:
        """When the List was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the List was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
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

    def create_card(self, 
                    *,
                    name: str,
                    position: Position='bottom',
                    type: CardType='project',
                    description: str|None=None,
                    due_date: datetime|None=None,
                    due_date_completed: bool=False,
                    stopwatch_duration: timedelta|None=None,
                    stopwatch_started: datetime|Literal['now']|None=None) -> Card:
        """Create a new card in the List
        
        Args:
            name: The name of the Card
            position: The position of the card within the List
            type: The type of the card
            description: An optional description to include
            due_date: A due date for the card
            due_date_completed: If the card has been completed
            stopwatch_duration: The duration to include with the stopwatch
            stopwatch_started: The start time for the runnung stopwatch (None is paused)

        """
        args: paths.Request_createCard = {
            'name': name,
            'position': get_position(self.cards, position),
            'type': type
        }
        # Apply optionals
        if description:
            args['description'] = description
        if due_date:
            args['dueDate'] = dttoiso(due_date, default_timezone=self.session.timezone)
        if due_date_completed:
            args['isDueCompleted'] = True

        if stopwatch_duration or stopwatch_started:
            args['stopwatch'] = {}
            if stopwatch_duration:
                args['stopwatch']['total'] = int(stopwatch_duration.total_seconds())
            if stopwatch_started:
                if stopwatch_started == 'now':
                    t = datetime.now(self.session.timezone).isoformat()
                else:
                    t = dttoiso(stopwatch_started, default_timezone=self.session.timezone)
                args['stopwatch']['startedAt'] = t
        
        return Card(
            self.endpoints.createCard(\
                self.id, 
                **args)['item'], 
                self.session
            )
    
    @model_list
    def sort_cards(self, **kwargs: Unpack[paths.Request_sortList]) -> list[Card]:
        """Sort all cards in the List and return the sorted Cards"""
        return [Card(c, self.session) for c in self.endpoints.sortList(self.id, **kwargs)['included']['cards']]
    
    @model_list
    def archive_cards(self) -> list[Card]:
        """Move all cards in the List to the Board archive"""
        return [
            Card(c, self.session)
            for c in self.endpoints.moveListCards(
                self.id, 
                listId=self.board.archive_list.id
                )['included']['cards']
        ]

    def delete_cards(self) -> None:
        """Delete all Cards in the List (must be a trash list)"""
        self.endpoints.clearList(self.id)['item']
    
    @model_list
    def move_cards(self, list: List, position: Position='top') -> list[Card]:
        """Move all Cards in this List to another List"""
        cards = self.cards
        for c in self.cards:
            c.move(list, position)
        return cards

    @model_list
    def shuffle(self) -> list[Card]:
        """Shuffle the cards in the List (randomize position)"""
        cards = self.cards
        shuffle(cards)
        for pos, card in enumerate(cards, start=1):
            card.position = pos*POSITION_GAP
        return cards

    @model_list
    def sort(self, key: Callable[[Card], Any]|None=None, reverse: bool=False) -> list[Card]:
        """Sort the list using a sort function
        
        Args:
            key: The sorting function to use (default is `card.name`)
            reverse: Reverse the sort order
        
        Note:
            If sorting on fields that may have comparison errors (e.g. `due_date`) 
            make sure your sort key properly accounts for that: 
            ```python
            >>> lst.sort(lambda c: c.due_date)
            Exception ... # Can't compare NoneType and datetime
            >>> lst.sort(lambda c: c.due_date or c.created_at+timedelta(days=10000))
            [
                Card(dueDate='2026-01-20...'),
                Card(dueDate='2026-01-26...'),
                ...
            ]
            ```
        """
        if key is None:
            key = lambda c: c.name
        cards = self.cards
        cards.sort(key=key, reverse=reverse)
        for pos, card in enumerate(cards, start=1):
            card.position = pos*POSITION_GAP
        return cards

    @model_list
    def filter(self, **kwargs: Unpack[paths.Request_getCards]) -> list[Card]:
        """Apply a filter to the list"""
        return [Card(c, self.session) for c in self.endpoints.getCards(self.id, **kwargs)['items']]

    @model_list
    def filter_term(self, term: str) -> list[Card]:
        """Get cards in the list using a search filter
        
        Args:
            term: The search term to apply to the list
        """
        return self.filter(search=term)
    
    @model_list
    def filter_users(self, *users: User) -> list[Card]:
        """Get all cards in a list with chosen members
        
        Args:
            users: Varargs of Users to filter on
        """
        return self.filter(filterUserIds=','.join(u.id for u in users))
        
    @model_list
    def filter_labels(self, *labels: Label) -> list[Card]:
        """Get all cards in a list with chosen members
        
        Args:
            users: Varargs of Users to filter on
        """
        return self.filter(filterLabelIds=','.join(l.id for l in labels))
        
    
        
from .attachment import Attachment
from .board import Board
from .card import Card
from .card_label import CardLabel
from .card_membership import CardMembership
from .custom_field import CustomField
from .custom_field_group import CustomFieldGroup
from .custom_field_value import CustomFieldValue
from .label import Label
from .task import Task
from .task_list import TaskList
from .user import User