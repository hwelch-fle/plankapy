from __future__ import annotations

__all__ = ('CardMembership', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, events

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    ...
    #from models import *


class CardMembership(PlankaModel[schemas.CardMembership]):
    """Python interface for Planka CardMemberships"""

    __events__ = events.CardMembershipEvent

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
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the card membership was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    def delete(self):
        """Delete the CardMembership"""
        return self.endpoints.deleteCardMembership(userId=self.user.id, cardId=self.card.id)


from .card import Card
from .user import User