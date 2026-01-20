from __future__ import annotations

__all__ = ('Action', )

from datetime import datetime

from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from models import *


class Action(PlankaModel[schemas.Action]):
    """Python interface for Planka Actions"""
    
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
        _usrs = [u for u in self.card.board.users if self.schema['userId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['userId']}")
    
    @property
    def data(self) -> dict[str, Any]:
        """The specific data associated with the Action (type dependant)"""
        return self.schema['data']
    
    @property
    def type(self):
        """The type of the Action"""
        return self.schema['type']