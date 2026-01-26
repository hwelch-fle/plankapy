from __future__ import annotations

__all__ = ('CustomFieldValue', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths, events

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    #from models import *


class CustomFieldValue(PlankaModel[schemas.CustomFieldValue]):
    """Python interface for Planka CustomFieldValues"""
    
    __events__ = events.CustomFieldValueEvents

    # CustomFieldValue props

    @property
    def card(self) -> Card:
        """The Card the CustomFieldValue belongs to"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def custom_field_group(self) -> CustomFieldGroup:
        """The CustomFieldGroup the CustomFieldValue belongs to"""
        return CustomFieldGroup(self.endpoints.getCustomFieldGroup(self.schema['customFieldGroupId'])['item'], self.session)

    @property
    def custom_field(self) -> CustomField:
        """The CustomField the CustomFieldValue belongs to"""
        _cfs = [cf for cf in self.custom_field_group.custom_fields if cf.id == self.schema['customFieldId']]
        return _cfs.pop()

    @property
    def content(self) -> str:
        """Content/value of the custom field"""
        return self.schema['content']
    @content.setter
    def content(self, content: str) -> None:
        """Set the content value of the CustomFieldValue"""
        self.update(content=content)

    @property
    def created_at(self) -> datetime:
        """When the CustomFieldValue was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the CustomFieldValue was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the CustomFieldValue with the Planka server"""
        _cfvs = [cfv for cfv in self.card.custom_field_values if cfv.id == self.id]
        if _cfvs:
            self.schema = _cfvs.pop().schema

    def update(self, **kwargs: Unpack[paths.Request_updateCustomFieldValue]):
        """Update the CustomFieldValue"""
        self.schema = self.endpoints.updateCustomFieldValue(
            cardId=self.schema['cardId'],
            customFieldGroupId=self.schema['customFieldGroupId'],
            customFieldId=self.schema['customFieldId'],
            **kwargs)['item']
    
    def delete(self):
        """Delete the CustomFieldValue"""
        self.endpoints.deleteCustomFieldValue(
            cardId=self.schema['cardId'],
            customFieldGroupId=self.schema['customFieldGroupId'],
            customFieldId=self.schema['customFieldId'],
        )


from .card import Card
from .custom_field import CustomField
from .custom_field_group import CustomFieldGroup
