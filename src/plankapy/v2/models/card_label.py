from __future__ import annotations

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas

TYPE_CHECKING = False
if TYPE_CHECKING:
    from models import *
    
class CardLabel(PlankaModel[schemas.CardLabel]):
    """Python interface for Planka CardLabels"""

    # CardLabel properties

    @property
    def card(self) -> Card:
        """The Card the Label is associated with"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)

    @property
    def label(self) -> Label:
        """The Label associated with the card"""
        _cls = [l for l in self.card.board.labels if l.id == self.schema['labelId']]
        return _cls.pop()

    @property
    def created_at(self) -> datetime:
        """When the card-label association was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the card-label association was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    def delete(self):
        """Delete the CardLabel"""
        return self.endpoints.deleteCardLabel(cardId=self.schema['cardId'], labelId=self.schema['labelId'])

