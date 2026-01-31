from __future__ import annotations

__all__ = ("PlankaModel", )

import json
import copy

from typing import Any, Self
from collections.abc import Mapping

TYPE_CHECKING = False
if TYPE_CHECKING:
    # Models take a Planka session to allow checking User permissions
    from ..interface import Planka

type Diff = dict[str, tuple[Any, Any]]

class PlankaModel[Schema: Mapping[str, Any]]:
    """Base Planka object interface"""
    
    def __init__(self, schema: Schema, session: Planka) -> None:
        self._schema = schema
        self.session = session
        self.endpoints = session.endpoints
        self.client = session.client
        self.current_role = session.current_role
        self.current_id = session.current_id
    
    @property
    def schema(self) -> Schema:
        return self._schema
    @schema.setter
    def schema(self, schema: Schema) -> None:
        self._schema = schema
    
    @property
    def id(self) -> str:
        if 'id' not in self.schema:
            # Should only happen for schemas.Config
            raise AttributeError(f'{self.__class__.__name__}: Does not have an `id` attribute')
        return self.schema['id']
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, PlankaModel):
            try:
                return (
                    self.id == other.id 
                    and self.__class__ == other.__class__ # type: ignore
                )
            except AttributeError: # handle no id case (Config)
                return False
        else:
            return super().__eq__(other)
    
    def __hash__(self) -> int:
        if 'id' not in self.schema:
            raise AttributeError(f'{self.__class__.__name__} does not have a hashable id attribute')
        return int(self.id)

    def __getitem__(self, key: str) -> Any:
        # Allow direct access to model schema cache
        return self.schema[key]

    def __setitem__(self, key: Any, val: Any) -> Any:
        # Don't allow writes to the cached values
        raise TypeError(
            f'Model attributes are read only. '
            'To update use associated property'
        )
    
    def copy(self) -> Self:
        """Create a deepcopy of the model and its associated schema.

        Note:
            Since the endpoints for both instances of the Model are the same, any 
            calls to update will restore the state and bring both copies into sync. 
            copies like this are meant more for comparing changes when running a sync 
            or update/assignemnt operation.
        
        Example:
        ```python
            >>> card_copy = card.copy()
            >>> card.name = 'Updated Name'
            >>> card_copy.name
            'Original Name'
            >>> card.name
            'Updated Name'
            >>> # This update may have had side effects
            >>> print(card_copy.diff(card))
            {'name': ('Original Name', 'Updated Name'), 'updatedAt': ('...2:00pm', '...2:45pm'), ...}
        ```
        """
        return copy.deepcopy(self)

    def diff(self, other: PlankaModel[Schema]) -> Diff:
        """Get a schema diff between two model schemas.

        Note:
            Only matching keys are diffed. Any schema keys that are not in the source schema 
            will not be checked in the target schema
        """
        return {
            k: (source, delta) 
            for k, source in self.schema
            if k in other.schema
            and (delta := other.schema[k]) 
            and delta != source
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({getattr(self, 'name', getattr(self, 'id', 'Unknown'))})"

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.schema})'          
    
    def json(self, **kwargs: Any) -> str:
        return json.dumps(self.schema, **kwargs)