from __future__ import annotations

__all__ = ('Attachment', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Unpack
    #from models import *


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
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the Attachment was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
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


from .card import Card
from .user import User