from __future__ import annotations

__all__ = ('Comment', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths, events

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    #from models import *


class Comment(PlankaModel[schemas.Comment]):
    """Python interface for Planka Comments"""
    
    __events__ = events.CommentEvent

    # Comment properties

    @property
    def card(self) -> Card:
        """The Card the Comment belongs to"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def user(self) -> User:
        """The User who created the Comment"""
        return self.card.board.users[self.schema['userId']]
    
    @property
    def text(self) -> str:
        """Content of the Comment"""
        return self.schema['text']
    
    @property
    def created_at(self) -> datetime:
        """When the comment was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the comment was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

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


from .card import Card
from .user import User