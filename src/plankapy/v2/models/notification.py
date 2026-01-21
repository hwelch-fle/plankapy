from __future__ import annotations

__all__ = ('Notification', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Unpack
    #from models import *
    from ._literals import NotificationType


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
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the Notification was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
    # Special Methods
    def sync(self):
        """Sync the Notification with the Planka server"""
        self.schema = self.endpoints.getNotification(self.id)['item']
 
    def update(self, **kwargs: Unpack[paths.Request_updateNotification]) -> None:
        """Update the Notification"""
        self.schema = self.endpoints.updateNotification(self.id, **kwargs)['item']


from .action import Action
from .board import Board
from .card import Card
from .comment import Comment
from .user import User