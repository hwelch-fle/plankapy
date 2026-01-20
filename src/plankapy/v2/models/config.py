from __future__ import annotations

__all__ = ('Config', )

from ._base import PlankaModel
from ..api import schemas

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from models import *


class Config(PlankaModel[schemas.Config]):
    """Python interface for Planka Config"""
    
    @property
    def version(self) -> str:
        """Current version of the PLANKA application"""
        return self.schema['version']
    
    @property
    def activeUsersLimit(self) -> int | None:
        """Maximum number of active users allowed (conditionally added for admins if configured)"""
        return self.schema.get('activeUsersLimit')

    @property
    def oidc(self) -> dict[str, Any] | None:
        """OpenID Connect configuration (null if not configured)"""
        return self.schema.get('oidc')
