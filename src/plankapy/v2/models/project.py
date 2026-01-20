from __future__ import annotations

__all__ = ('Project', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    from models import *
    from ._literals import BackgroundGradient, BackgroundType


class Project(PlankaModel[schemas.Project]):
    """Python interface for Planka Projects"""
    
    # Project Included
    @property
    def _included(self):
        return self.endpoints.getProject(self.id)['included']
    
    @property
    def users(self) -> list[User]:
        """Get Users associated with the Project"""
        return [User(u, self.session) for u in self._included['users']]
    @property
    def managers(self) -> list[ProjectManager]:
        """Get project manager Users associated with the Project"""
        return [ProjectManager(pm, self.session) for pm in self._included['projectManagers']]
    @property
    def background_images(self) -> list[BackgroundImage]:
        """Get BackgroundImages associated with the Project"""
        return [BackgroundImage(bgi, self.session) for bgi in self._included['backgroundImages']]
    @property
    def base_custom_field_groups(self) -> list[BaseCustomFieldGroup]:
        """Get BaseCustomFieldGroups associated with the Project"""
        return [BaseCustomFieldGroup(bcfg, self.session) for bcfg in self._included['baseCustomFieldGroups']]
    @property
    def boards(self) -> list[Board]:
        """Get Boards associated with the Project"""
        return [Board(b, self.session) for b in self._included['boards']]
    @property
    def board_memberships(self) -> list[BoardMembership]:
        """Get BoardMemberships associated with the Project"""
        return [BoardMembership(bm, self.session) for bm in self._included['boardMemberships']]
    @property
    def custom_fields(self) -> list[CustomField]:
        """Get CustomFields associated with the Project"""
        return [CustomField(cf, self.session) for cf in self._included['customFields']]
    @property
    def notification_services(self) -> list[NotificationService]:
        """Get NotificationServices associated with the Project"""
        return [NotificationService(ns, self.session) for ns in self._included['notificationServices']]
    
    # Project Properties
    @property
    def favorite(self) -> bool:
        """Whether the project is in the current User's favorites"""
        return self.endpoints.getProject(self.id)['item']['isFavorite']
    @favorite.setter
    def favorite(self, is_favorite: bool) -> None:
        """Set/Unset the Project in the current User's favorites"""
        self.update(isFavorite=is_favorite)
        
    @property
    def owner(self) -> User:
        """The User who owns the project (Raises LookupError if the User cannot be found)"""
        _usrs = [u for u in self.users if self.schema['ownerProjectManagerId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find user: {self.schema['ownerProjectManagerId']}")

    @property
    def background_image(self) -> BackgroundImage | None:
        """The current BackgroundImage of the Project"""
        bgis = [bgi for bgi in self.background_images if bgi.id == self.schema['backgroundImageId']]
        if not bgis:
            return None
        return bgis.pop()
    @background_image.setter
    def background_image(self, background_image: BackgroundImage | None) -> None:
        """Set the Project BackgroundImage"""
        if background_image is None:
            self.remove_background()
        else:
            self.update(backgroundImageId=background_image.id, backgroundType='image')
    
    @property
    def name(self) -> str:
        """Name/title of the Project"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the Project name"""
        self.update(name=name)
        
    @property
    def description(self) -> str:
        """Detailed description of the Project"""
        return self.schema['description']
    @description.setter
    def description(self, description: str) -> None:
        """Set the Project description"""
        self.update(description=description)
    
    @property
    def background_type(self):
        """Type of background for the project"""
        return self.schema['backgroundType']
    @background_type.setter
    def background_type(self, type: BackgroundType):
        """Set the background type"""
        self.update(backgroundType=type)
        
    @property
    def background_gradient(self) -> BackgroundGradient | None:
        """Gradient background for the project"""
        return self.schema['backgroundGradient']
    @background_gradient.setter
    def background_gradient(self, gradient: BackgroundGradient | None) -> None:
        """Set the Project background gradient"""
        if gradient is None:
            self.remove_background()
        else:
            self.update(backgroundGradient=gradient, backgroundType='gradient')
    
    @property
    def hidden(self) -> bool:
        """Whether the project is hidden"""
        return self.schema['isHidden']
    @hidden.setter
    def hidden(self, is_hidden: bool) -> None:
        """Set/Unset the Project as hidden"""
        self.update(isHidden=is_hidden)
    
    @property
    def created_at(self) -> datetime:
        """When the project was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the project was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
    # Special Methods
    def sync(self):
        self.schema = self.endpoints.getProject(self.id)['item']
        
    def update(self, **project: Unpack[paths.Request_updateProject]) -> None:
        """Update the Project"""
        self.schema = self.endpoints.updateProject(self.id, **project)['item']
        
    def delete(self) -> None:
        """Delete the Project"""
        self.endpoints.deleteProject(self.id)
    
    def add_project_manager(self, user: User) -> ProjectManager:
        """Add a User to the Project as a ProjectManager"""
        return ProjectManager(self.endpoints.createProjectManager(self.id, userId=user.id)['item'], self.session)
    
    def remove_background(self) -> None:
        """Reset the Project background to the default grey"""
        self.update(backgroundType=None) # type: ignore

    def remove_project_manager(self, project_manager: ProjectManager | User) -> None:
        """Remove a ProjectManager from the Project"""
        if isinstance(project_manager, User):
            # Get the ProjectManager object for the User
            for pm in self.managers:
                if pm.user == project_manager:
                    project_manager = pm
                    break
            else:
                # If User not in managers, do nothing
                return
        
        if project_manager.project == self:
            # Only delete ProjectManager if it is for this Project
            # Defer deletion to the ProjectManager object
            project_manager.delete()

    def create_board(self, **board: Unpack[paths.Request_createBoard]) -> Board:
        """Create a new Board in the Project"""
        return Board(self.endpoints.createBoard(self.id, **board)['item'], self.session)

    def create_base_custom_field_group(self, **bcfg: Unpack[paths.Request_createBaseCustomFieldGroup]) -> BaseCustomFieldGroup:
        """Create a BaseCustomFieldGroup in the Project"""
        return BaseCustomFieldGroup(self.endpoints.createBaseCustomFieldGroup(self.id, **bcfg)['item'], self.session)

