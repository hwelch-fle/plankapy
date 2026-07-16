from __future__ import annotations

from datetime import datetime
from typing import Unpack

from ..api import events, schemas, typ
from ._base import PlankaModel
from ._helpers import Position, dtfromiso, get_position, model_list

# Deferred Model imports at bottom of file

__all__ = ('CustomFieldGroup', )


class CustomFieldGroup(PlankaModel[schemas.CustomFieldGroup]):
    """Python interface for Planka CustomFieldGroups"""

    __events__ = events.CustomFieldGroupEvents

    # CustomFieldGroup included

    @property
    def _included(self):
        return self.endpoints.getCustomFieldGroup(self.id)['included']

    @property
    @model_list
    def custom_fields(self) -> list[CustomField]:
        return [CustomField(cf, self.session) for cf in self._included['customFields']]

    @property
    @model_list
    def custom_field_values(self) -> list[CustomFieldValue]:
        return [CustomFieldValue(cfv, self.session) for cfv in self._included['customFieldValues']]

    # CustomFieldGroup props

    @property
    def board(self) -> Board:
        """The Board the CustomFieldGroup belongs to"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)

    @property
    def card(self) -> Card:
        """The Card the CustomFieldGroup belongs to"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)

    @property
    def base_custom_field_group(self) -> BaseCustomFieldGroup | None:
        """The BaseCustomFieldGroup used as a template"""
        return self.board.project.base_custom_field_groups[{'id': self.schema['baseCustomFieldGroupId']}].dpop()

    @property
    def position(self) -> int:
        """Position of the CustomFieldGroup within the Board/Card"""
        return self.schema['position']

    @position.setter
    def position(self, position: int) -> None:
        """Set the CustomFieldGroup position within the Board/Card"""
        self.update(position=position)

    @property
    def name(self) -> str:
        """Name/title of the CustomFieldGroup"""
        return self.schema['name']

    @name.setter
    def name(self, name: str) -> None:
        """Set the CustomFieldGroup name"""
        self.update(name=name)

    @property
    def created_at(self) -> datetime:
        """When the CustomFieldGroup was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the CustomFieldGroup was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the CustomFieldGroup with the Planka server"""
        self.schema = self.endpoints.getCustomFieldGroup(self.id)['item']

    def update(self, **kwargs: Unpack[typ.Request_updateCustomFieldGroup]):
        """Update the CustomFieldGroup"""
        self.schema = self.endpoints.updateCustomFieldGroup(self.id, **kwargs)['item']

    def delete(self):
        """Delete the CustomFieldGroup"""
        return self.endpoints.deleteCustomFieldGroup(self.id)

    def add_to_card(self, card: Card) -> CustomFieldGroup:
        """Add the CustomFieldGroup to a Card

        Args:
            card (Card): The Card to add the CustomFieldGroup to
        """
        # Replace the Current cardId with the ID of the Card we are adding to
        schema = self.schema.copy()
        schema['cardId'] = card.id
        return CustomFieldGroup(self.endpoints.createCardCustomFieldGroup(**schema)['item'], self.session)

    def make_base_group(self, project: Project) -> BaseCustomFieldGroup:
        """Convert a CustomFieldGroup into a BaseCustomFieldGroup for a Project or Board

        Args:
            project (Project): The project to add the BaseCustomFieldGroup to

        Returns:
            BaseCustomFieldGroup: The new BaseCustomFieldGroup
        """
        return BaseCustomFieldGroup(self.endpoints.createBaseCustomFieldGroup(project.id, name=self.name)['item'], self.session)

    def add_field(self, name: str,
                  *,
                  position: Position = 'top',
                  show_on_card: bool = False) -> CustomField:
        """Add a Field to the CustomFieldGroup

        Args:
            name (str): The name of the Field to add
            position (Position): The position of the field within the group (default: `top`)
            show_on_card (bool): Show the field on the Card front (default: `False`)

        Returns:
            CustomField: If the Field aleady exists, that Field is returned
        """
        # Return existing field
        if existing_field := self.custom_fields[{'name': name}].dpop():
            return existing_field

        return CustomField(
            self.endpoints.createCustomFieldInGroup(
                self.id,
                name=name,
                position=get_position(self.custom_fields, position),
                showOnFrontOfCard=show_on_card,
            )['item'], self.session
        )

    def add_fields(self,
                   *names: str,
                   position: Position = 'top',
                   show_on_card: bool = False) -> list[CustomField]:
        """Add fields to the CustomFieldGroup

        Args:
            *names (str): Varargs of the names to add
            position (Position): The position of the field within the group (default: `top`)
            show_on_card (bool): Show the field on the Card front (default: `False`)

        Returns:
            list[CustomField] : The fields added

        Note:
            Field positions will be calculated in the order passed
        """
        return [
            self.add_field(name=name, position=position, show_on_card=show_on_card)
            for name in names
        ]

    def remove_field(self, field: CustomField) -> None:
        """Remove the field from the CustomFieldGroup

        Args:
            field (CustomField): The CustomField to remove (must be in this Group)
        """
        if field in self.custom_fields:
            field.delete()


from .base_custom_field_group import BaseCustomFieldGroup
from .board import Board
from .card import Card
from .custom_field import CustomField
from .custom_field_value import CustomFieldValue
from .project import Project
