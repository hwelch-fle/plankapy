from __future__ import annotations

__all__ = ('Project', )

from pathlib import Path
from httpx import HTTPStatusError
from datetime import datetime
from ._base import PlankaModel
from ._helpers import Position, dtfromiso, get_position, model_list
from ..api import schemas, paths, events

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    #from models import *
    from ._literals import BackgroundGradient, BackgroundType, BoardImportType


class Project(PlankaModel[schemas.Project]):
    """Python interface for Planka Projects"""
    
    __events__ = events.ProjectEvents

    # Project Included
    
    @property
    def _included(self):
        return self.endpoints.getProject(self.id)['included']
    
    @property
    @model_list
    def users(self) -> list[User]:
        """Get Users associated with the Project"""
        return [User(u, self.session) for u in self._included['users']]
    
    @property
    @model_list
    def project_managers(self) -> list[ProjectManager]:
        """Get project manager Users associated with the Project"""
        return [ProjectManager(pm, self.session) for pm in self._included['projectManagers']]
    
    @property
    @model_list
    def background_images(self) -> list[BackgroundImage]:
        """Get BackgroundImages associated with the Project"""
        return [BackgroundImage(bgi, self.session) for bgi in self._included['backgroundImages']]
    
    @property
    @model_list
    def base_custom_field_groups(self) -> list[BaseCustomFieldGroup]:
        """Get BaseCustomFieldGroups associated with the Project"""
        return [BaseCustomFieldGroup(bcfg, self.session) for bcfg in self._included['baseCustomFieldGroups']]
    
    @property
    @model_list
    def boards(self) -> list[Board]:
        """Get Boards associated with the Project"""
        return [Board(b, self.session) for b in self._included['boards']]
    
    @property
    @model_list
    def board_memberships(self) -> list[BoardMembership]:
        """Get BoardMemberships associated with the Project"""
        return [BoardMembership(bm, self.session) for bm in self._included['boardMemberships']]
    
    @property
    @model_list
    def custom_fields(self) -> list[CustomField]:
        """Get CustomFields associated with the Project"""
        return [CustomField(cf, self.session) for cf in self._included['customFields']]
    
    @property
    @model_list
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
    def owner(self) -> User | None:
        """The User who owns the project (Raises LookupError if the User cannot be found)"""
        _usrs = [pm for pm in self.project_managers if self.schema['ownerProjectManagerId'] == pm.id]
        if _usrs:
            return _usrs.pop().user
        #return User(self.endpoints.getUser(self.schema['ownerProjectManagerId'])['item'], self.session)

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
    
    def update_background_image(self, background: BackgroundImage | Path | str | bytes | None) -> BackgroundImage | None:
        """Update the Project Background Image,
        
        Only Admins and ProjectManagers can update the Background Image
        
        Args:
            background (BackgroundImage | Path | str | bytes | None): Existing Image or filepath/url or raw bytes or None to unset
            
        Returns:
            (BackgroundImage | None): If a backround image was set or created
        """
        # Force a PermissionError early if this user isn't the current user or an admin
        if self.id != self.session.current_id and self.session.current_role != 'admin':
            self.endpoints.createBackgroundImage(self.id, **{'file': b'NO_PERMISSION'})
        
        if background is None:
            self.remove_background()
            return

        if isinstance(background, BackgroundImage):
            # Assign the image if it is in this project
            if background in self.background_images:
                self.background_image = background
            
            # Re-Upload to this project
            else:
                self.update_background_image(background.url)
            return background

        if isinstance(background, Path):
            # Convert Path to a string so it can be handled normally
            background = str(background.resolve())

        # Deferred import of mimetypes that is only used here
        # This function takes so long anyways so the import delay 
        # isn't noticable
        import mimetypes
        
        # Handle filepath or URL
        mime_type = None
        if isinstance(background, str):
            # Guess URL file type
            if background.startswith('http'):
                mime_type, *_ = mimetypes.guess_type(background)
                mime_type = mime_type or 'application/octet-stream'
                try:
                    req = self.client.get(background)
                    req.raise_for_status()
                    background = req.content
                except HTTPStatusError as status_error:
                    status_error.add_note(f'Unable to download attachment from {background}')
                    raise
            # Guess local file type
            # And read Bytes
            else:
                mime_type, *_ = mimetypes.guess_file_type(background)
                mime_type = mime_type or 'application/octet-stream'
                background = open(background, 'rb').read()
        
        mime_type = mime_type or 'application/octet-stream'
        return BackgroundImage(
            self.endpoints.createBackgroundImage(
                self.id, 
                file=bytes(background), 
                mime_type=mime_type,
            )['item'],
            self.session
        )
    
    def remove_background(self) -> None:
        """Reset the Project background to the default grey"""
        self.update(backgroundType=None)

    def remove_project_manager(self, project_manager: ProjectManager | User) -> None:
        """Remove a ProjectManager from the Project"""
        if isinstance(project_manager, User):
            # Get the ProjectManager object for the User
            for pm in self.project_managers:
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

    def create_board(self, 
                     *, 
                     name: str, 
                     position: Position | int ='top') -> Board:
        """Create a new Board in the Project
        
        Args:
            name: The name of the Board
            position: The position of the board within the project
        """
        return Board(
            self.endpoints.createBoard(
                self.id, 
                name=name, 
                position=get_position(self.boards, position)
            )['item'], 
            self.session
        )

    def import_board(self, 
                     *, 
                     name: str, 
                     import_file: bytes, 
                     position: Position | int='top', 
                     import_type: BoardImportType='trello',
                     request_id: str|None=None) -> Board:
        """Import a board from a file (currently supports trello imports only)
        
        Args:
            name: The name of the imported Board
            position: The position of the imported Board within the Project
            import_type: The type of the Bord import (currently `trello` only)
            request_id: An optional request ID for tracking upload progress (default: `now in iso8601`)
        """
        return Board(
            self.endpoints.createBoard(
                self.id,
                name=name,
                position=get_position(self.boards, position),
                importType=import_type,
                importFile=import_file,
                requestId=request_id or datetime.now().isoformat(),
            )['item'],
            self.session
        )

    def create_base_custom_field_group(self, 
                                       *, 
                                       name: str) -> BaseCustomFieldGroup:
        """Create a BaseCustomFieldGroup in the Project
        
        Args:
            name: The name of the new BaseCustomFieldGroup
        """
        return BaseCustomFieldGroup(
            self.endpoints.createBaseCustomFieldGroup(
                self.id, 
                name=name,
            )['item'], 
            self.session
        )


from .board import Board
from .user import User
from .project_manager import ProjectManager
from .background_image import BackgroundImage
from .base_custom_field_group import BaseCustomFieldGroup
from .board_membership import BoardMembership
from .custom_field import CustomField
from .notification_service import NotificationService