from __future__ import annotations

__all__ = ('CustomField', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths, events

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    from models import *


class CustomField(PlankaModel[schemas.CustomField]):
    """Python interface for Planka CustomFields"""
    
    __events__ = events.CustomFieldEvents

    # CustomField props
    
    @property
    def base_custom_field_group(self) -> BaseCustomFieldGroup:
        """The BaseCustomFieldGroup the custom field belongs to"""
        return self.custom_field_group.base_custom_field_group
    
    @property
    def custom_field_group(self) -> CustomFieldGroup:
        """The CustomFieldGroup the CustomField belongs to"""
        return CustomFieldGroup(self.endpoints.getCustomFieldGroup(self.schema['customFieldGroupId'])['item'], self.session)
    
    @property
    def position(self) -> int:
        """Position of the CustomField within the CustomFieldGroup"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Set the position of the CustomField within the CustomFieldGroup"""
        self.update(position=position)

    @property
    def name(self) -> str:
        """Name/title of the custom field"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        self.update(name=name)

    @property
    def show_on_front_of_card(self) -> bool:
        """Whether to show the CustomField on the front of Cards"""
        return self.schema['showOnFrontOfCard']
    @show_on_front_of_card.setter
    def show_on_front_of_card(self, show_on_front_of_card: bool) -> None:
        """Set Wwether to show the CustomField on the front of Cards"""
        self.update(showOnFrontOfCard=show_on_front_of_card)

    @property
    def created_at(self) -> datetime:
        """When the custom field was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the custom field was last updated"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the CustomField with the Planka server"""

    def update(self, **kwargs: Unpack[paths.Request_updateCustomField]):
        """Update the CustomField"""
        self.schema = self.endpoints.updateCustomField(self.id, **kwargs)['item']
    
    def delete(self):
        """Delete the CustomField"""
        self.endpoints.deleteCustomField(self.id)


from .base_custom_field_group import BaseCustomFieldGroup
from .custom_field import CustomField
from .custom_field_group import CustomFieldGroup
