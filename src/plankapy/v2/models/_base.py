from __future__ import annotations

__all__ = ("PlankaModel", )

import json
from typing import Any
from collections.abc import Mapping

TYPE_CHECKING = False
if TYPE_CHECKING:
    # Models take a Planka session to allow checking User permissions
    from ..interface import Planka

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
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(schema={self.__dict__})'
    
    #def __getattribute__(self, name: str) -> Any:
    #    # TODO: use `_live_mode` to force a `sync` call on attribute acces
    #    return super().__getattribute__(name)           
    
    def json(self, **kwargs: Any) -> str:
        return json.dumps(self.schema, **kwargs)