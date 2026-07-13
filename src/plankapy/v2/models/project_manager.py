from __future__ import annotations

from datetime import datetime

from ..api import events, schemas
from ._base import PlankaModel
from ._helpers import dtfromiso

# Deferred Model imports at bottom of file

__all__ = ('ProjectManager', )


class ProjectManager(PlankaModel[schemas.ProjectManager]):
    """Python interface for Planka ProjectManagers"""

    __events__ = events.ProjectManagerEvents

    # ProjectManager Properties

    @property
    def project(self) -> Project:
        """The Project associated with the ProjectManager"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)

    @property
    def user(self) -> User:
        """The User assigned as ProjectManager (Raises LookupError if the User cannot be found)"""
        if usr := self.project.users[{'id': self.schema['userId']}].dpop():
            return usr
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
        pms = self.project.project_managers
        for pm in pms:
            if pm.id == self.id:
                self.schema = pm.schema

    def delete(self):
        self.endpoints.deleteProjectManager(self.id)


from .project import Project
from .user import User
