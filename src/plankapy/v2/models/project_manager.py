from __future__ import annotations

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas

TYPE_CHECKING = False
if TYPE_CHECKING:
    from models import *

__all__ = ('ProjectManager', )

class ProjectManager(PlankaModel[schemas.ProjectManager]):
    """Python interface for Planka ProjectManagers"""
    
    # ProjectManager Properties
    @property
    def project(self) -> Project:
        """The Project associated with the ProjectManager"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)
    @property
    def user(self) -> User:
        """The User assigned as ProjectManager (Raises LookupError if the User cannot be found)"""
        _usrs = [u for u in self.project.users if self.schema['userId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['userId']}")
    
    @property
    def created_at(self) -> datetime:
        """When the ProjectManager was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the ProjectManager was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
    # Special Methods
    def sync(self):
        """Sync the ProjectManager with the Planka server"""
        pms = self.project.managers
        for pm in pms:
            if pm.id == self.id:
                self.schema = pm.schema
                
    def delete(self):
        self.endpoints.deleteProjectManager(self.id)
