from __future__ import annotations

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    from models import *
    from ._literals import NotificationServiceFormat

__all__ = ('NotificationService', )

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
    @url.setter
    def url(self, url: str) -> None:
        """Set the NotificationService url"""
        self.update(url=url)
    
    @property
    def format(self) -> NotificationServiceFormat: 
        """Format for notification messages"""
        return self.schema['format']
    @format.setter
    def format(self, format: NotificationServiceFormat) -> None:
        """Set the NotificationService format"""
        self.update(format=format)
    
    @property
    def created_at(self) -> datetime:
        """When the NotificationService was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the NotificationService was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
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
