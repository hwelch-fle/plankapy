from __future__ import annotations

__all__ = ('BaseCustomFieldGroup', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import Position, dtfromiso, get_position, model_list
from ..api import paths, schemas, events

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    #from models import *


class BaseCustomFieldGroup(PlankaModel[schemas.BaseCustomFieldGroup]):
    """Python interface for Planka BaseCustomFieldGroups"""

    __events__ = events.BaseCustomFieldGroupEvents

    # BaseCustomFieldGroup Properties
    @property
    def project(self) -> Project:
        """The Project that the BaseCustomFieldGroup is associated with"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)

    @property
    @model_list
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
            field: The existing CustomField to add
            position: The position of the new Field
            show_on_card: Override the input Field's show state
            
        Note:
            If a CustomField with a matching name already exists in the base group, it 
            will be returned
        """

        if (cf := self.custom_fields[field].dpop()):
            flds = ('name', 'position', 'showOnFrontOfCard')
            cf.update(**{k: field[k] for k in flds if cf[k] != field[k]})
            return cf
        
        return self.create_field(
            field.name, 
            position=position, 
            show_on_card=show_on_card or field.show_on_front_of_card
        )
        
        
    def create_field(self, 
                     name: str, 
                     *,
                     position: Position='top', 
                     show_on_card: bool=False) -> CustomField:
        """Create a new CustomField in the BaseCustomFieldGroup
        
        Args:
            name: Name/title of the custom field
            position: Position of the custom field within the group
            show_on_card: Whether to show the field on the front of cards 
        """
        return CustomField(
            self.endpoints.createCustomFieldInBaseGroup(
                self.id, 
                name=name,
                position=get_position(self.custom_fields, position),
                showOnFrontOfCard=show_on_card,
                )['item'], 
            self.session
        )


from .project import Project
from .custom_field import CustomField