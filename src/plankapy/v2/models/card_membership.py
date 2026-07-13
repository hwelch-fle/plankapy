from __future__ import annotations

from datetime import datetime

from ..api import events, schemas
from ._base import PlankaModel
from ._helpers import dtfromiso

# Deferred Model imports at bottom of file

__all__ = ('CardMembership', )


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
        if usr := self.card.board.users[{'id': self.schema['userId']}].dpop():
            return usr
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
