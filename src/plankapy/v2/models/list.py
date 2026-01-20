from __future__ import annotations

from datetime import datetime
from ._base import PlankaModel
from ._helpers import Position, dtfromiso
from ..api import schemas, paths

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    from models import *
    from ._literals import UserListType, ListColor

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
    def color(self, color: ListColor | None) -> None:
        """Set the List color"""
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
    
    def move_cards(self, list: List, position: Position='top') -> None:
        """Move all Cards in this List to another List"""
        for c in self.cards:
            c.move(list, position)
