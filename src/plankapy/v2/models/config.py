from __future__ import annotations

__all__ = ('Config', )

from ._base import PlankaModel
from ..api import schemas, events


# NOTE: schemas.Config is now used for SMTP Config, App Config is now Bootstrap
class Config(PlankaModel[schemas.Bootstrap]):
    """Python interface for Planka Config"""
    
    __events__ = events.ConfigEvents

    @property
    def version(self) -> str | None:
        """Current version of the PLANKA application"""
        return self.schema.get('version')
    
    @property
    def activeUsersLimit(self) -> int | None:
        """Maximum number of active users allowed (conditionally added for admins if configured)"""
        return self.schema.get('activeUsersLimit')

    @property
    def termsLanguages(self) -> list[str] | None:
        """List of available languages for ToS"""
        return self.schema.get('termsLanguages')

    @property
    def customerPanelUrl(self) -> str | None:
        """URL to the customer management panel"""
        return self.schema.get('customerPanelUrl')

    @property
    def oidc(self) -> schemas.OIDC | None:
        """OpenID Connect configuration (null if not configured)"""
        return self.schema.get('oidc')
