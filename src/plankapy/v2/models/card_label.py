from __future__ import annotations

from datetime import datetime

from ..api import events, schemas
from ._base import PlankaModel
from ._helpers import dtfromiso

# Deferred Model imports at bottom of file

__all__ = ('CardLabel', )


class CardLabel(PlankaModel[schemas.CardLabel]):
    """Python interface for Planka CardLabels"""

    __events__ = events.CardLabelEvents

    # CardLabel properties

    @property
    def card(self) -> Card:
        """The Card the Label is associated with"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)

    @property
    def label(self) -> Label:
        """The Label associated with the card"""
        return self.card.board.labels[self.schema['labelId']]

    @property
    def created_at(self) -> datetime:
        """When the card-label association was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the card-label association was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the CardLabel with the Planka server"""
        self.schema = self.card.board.card_labels[self].dpop(default=self).schema

    def delete(self):
        """Delete the CardLabel"""
        return self.endpoints.deleteCardLabel(cardId=self.schema['cardId'], labelId=self.schema['labelId'])


from .card import Card
from .label import Label
