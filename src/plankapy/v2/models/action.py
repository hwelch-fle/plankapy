from __future__ import annotations

from datetime import datetime
from typing import Any

from ..api import events, schemas
from ._base import PlankaModel
from ._helpers import dtfromiso

# Deferred Model imports at bottom of file

__all__ = ('Action', )


class Action(PlankaModel[schemas.Action]):
    """Python interface for Planka Actions"""

    __events__ = events.ActionEvents

    @property
    def created_at(self) -> datetime:
        """When the Action was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the Action was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

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
        if usr := self.card.board.users[{'id': self.schema['userId']}].dpop():
            return usr
        raise LookupError(f"Cannot find User: {self.schema['userId']}")

    @property
    def data(self) -> dict[str, Any]:
        """The specific data associated with the Action (type dependant)"""
        return self.schema['data']

    @property
    def type(self):
        """The type of the Action"""
        return self.schema['type']

    # Special Methods
    def sync(self) -> None:
        """Sync the Action with the Planka server"""
        self.schema = self.card.actions[self].dpop(default=self).schema


from .board import Board
from .card import Card
from .user import User
