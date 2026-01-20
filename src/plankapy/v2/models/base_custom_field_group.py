from __future__ import annotations

from datetime import datetime
from ._base import PlankaModel
from ._helpers import Position, dtfromiso, get_position
from ..api import paths, schemas

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    from models import *

class BaseCustomFieldGroup(PlankaModel[schemas.BaseCustomFieldGroup]):
    """Python interface for Planka BaseCustomFieldGroups"""

    # BaseCustomFieldGroup Properties
    @property
    def project(self) -> Project:
        """The Project that the BaseCustomFieldGroup is associated with"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)

    @property
    def custom_fields(self) -> list[CustomField]:
        """The CustomFields associated with the BaseCustomFieldGroup"""
        return [cf for cf in self.project.custom_fields if cf.schema['baseCustomFieldGroupId'] == self.id]

    @property
    def name(self) -> str:
        """Name/title of the base custom field group"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the name/title of the base custom field group"""
        self.update(name=name)
    
    @property
    def created_at(self) -> datetime:
        """When the base custom field group was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the base custom field group was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the BaseCustomFieldGroup with the Planka server"""
        for bcfg in self.project.base_custom_field_groups:
            if bcfg == self:
                self.schema = bcfg.schema
                
    def update(self, **base_custom_field_group: Unpack[paths.Request_updateBaseCustomFieldGroup]):
        """Update the BaseCustomFieldGroup"""
        self.endpoints.updateBaseCustomFieldGroup(self.id, **base_custom_field_group)
        
    def delete(self):
        """Delete the BaseCustomFieldGroup"""
        return self.endpoints.deleteBaseCustomFieldGroup(self.id)

    def add_field(self, field: CustomField, 
                  *, 
                  position: Position='top',
                  show_on_card: bool|None=None) -> CustomField:
        """Add an existing CustomField to the BaseGroup
        
        Args:
            field (CustomField): The existing CustomField to add
            position (Position): The position of the CustomField in the BaseCustomFieldGroup (default: `top`)
            show_on_card (bool): (default: field.show_on_front_of_card)
            
        Note:
            If a CustomField with a matching name already exists in the base group, it 
            will be returned
        """
        # Set position and 
        if show_on_card is None:
            show_on_card = field.show_on_front_of_card
        
        position = get_position(self.custom_fields, position) 
        
        # Find existing and update
        for cf in self.custom_fields:
            if cf.name != field.name:
                continue
            if cf.position != position:
                cf.position = position
            if cf.show_on_front_of_card != show_on_card:
                cf.show_on_front_of_card = show_on_card
            return cf
        
        # Create New Field
        return self.create_field(name=field.name, position=position, showOnFrontOfCard=show_on_card)

    def create_field(self, **kwargs: Unpack[paths.Request_createCustomFieldInBaseGroup]) -> CustomField:
        """Create a new CustomField in the BaseCustomFieldGroup
        
        Args:
            name (str): Name/title of the custom field
            position (int): Position of the custom field within the group
            showOnFrontOfCard (bool): Whether to show the field on the front of cards 
        """
        return CustomField(self.endpoints.createCustomFieldInBaseGroup(self.id, **kwargs)['item'], self.session)
    