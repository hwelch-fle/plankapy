from __future__ import annotations

__all__ = ('User', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Unpack
    from models import *
    from ._literals import (
        UserRole, 
        EditorMode, 
        HomeView, 
        Language, 
        LockableField, 
        ProjectOrdering, 
        BoardRole, 
        TermsType
    )


class User(PlankaModel[schemas.User]):
    """Python interface for Planka Users"""

    @property
    def email(self) -> str | None:
        """Email address for login and notifications (private field)"""
        return self.schema.get('email')
    @email.setter
    def email(self, email: str) -> None:
        """Set the User email (Direct assignment only allowed for Admin users)"""
        self.endpoints.updateUserEmail(self.id, email=email)

    @property
    def password(self) -> None:
        raise AttributeError(f'Passwords can only be set by Admin Users and read by nobody')
    @password.setter
    def password(self, password: str) -> None:
        """Set a User's password (Admin only)"""
        self.endpoints.updateUserPassword(self.id, password=password)

    @property
    def role(self):
        """User role defining access permissions"""
        return self.schema['role']
    @role.setter
    def role(self, role: UserRole) -> None:
        """Set the User role"""
        self.update(role=role)

    @property
    def name(self) -> str:
        """Full display name of the user"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the User's name"""
        self.update(name=name)

    @property
    def username(self) -> str:
        """Unique username for user identification"""
        return self.schema['username']
    @name.setter
    def name(self, name: str) -> None:
        """Set the User's username"""
        self.update(name=name)

    @property
    def avatar(self) -> dict[str, Any]:
        """Avatar information for the user with generated URLs"""
        return self.schema['avatar']
    @avatar.setter
    def avatar(self, avatar: Any) -> None:
        """Set the User's avatar"""
        raise NotImplementedError('Avatar setting has not been implemented') 
    
    @property
    def gravatar_url(self) -> str | None:
        """Gravatar URL for the user (conditionally added if configured)"""
        return self.schema.get('gravatarUrl')
    
    @property
    def phone(self) -> str:
        """Contact phone number"""
        return self.schema['phone']
    @phone.setter
    def phone(self, phone: str) -> None:
        """Set the User's phone"""
        self.update(phone=phone)

    @property
    def organization(self) -> str:
        """Organization or company name"""
        return self.schema['organization']
    @organization.setter
    def organization(self, organization: str) -> None:
        """Set the User's organization"""
        self.update(organization=organization)

    @property
    def language(self) -> Language | None:
        """Preferred language for user interface and notifications (personal field)"""
        return self.schema.get('language')
    @language.setter
    def language(self, language: Language) -> None:
        """Set the User's language"""
        self.update(language=language)

    @property
    def subscribe_to_own_cards(self) -> bool:
        """Whether the user subscribes to their own cards (personal field)"""
        return self.schema.get('subscribeToOwnCards', False)
    @subscribe_to_own_cards.setter
    def subscribe_to_own_cards(self, subscribe_to_own_cards: bool) -> None:
        """Set Whether the user subscribes to their own cards (personal field)"""
        self.update(subscribeToOwnCards=subscribe_to_own_cards)

    @property
    def subscribe_to_card_when_commenting(self) -> bool:
        """Whether the user subscribes to cards when commenting (personal field)"""
        return self.schema.get('subscribeToCardWhenCommenting', False)
    @subscribe_to_card_when_commenting.setter
    def subscribe_to_card_when_commenting(self, subscribe_to_card_when_commenting: bool) -> None:
        """Set whether the user subscribes to cards when commenting (personal field)"""
        self.update(subscribeToCardWhenCommenting=subscribe_to_card_when_commenting)

    @property
    def turn_off_recent_card_highlighting(self) -> bool:
        """Whether recent card highlighting is disabled (personal field)"""
        return self.schema.get('turnOffRecentCardHighlighting', False)
    @turn_off_recent_card_highlighting.setter
    def turn_off_recent_card_highlighting(self, turn_off_recent_card_highlighting: bool) -> None:
        """Set whether recent card highlighting is disabled (personal field)"""
        self.update(turnOffRecentCardHighlighting=turn_off_recent_card_highlighting)

    @property
    def enable_favorites_by_default(self) -> bool:
        """Whether favorites are enabled by default (personal field)"""
        return self.schema.get('enableFavoritesByDefault', False)
    @enable_favorites_by_default.setter
    def enable_favorites_by_default(self, enable_favorites_by_default: bool) -> None:
        """Set whether favorites are enabled by default (personal field)"""
        self.update(enableFavoritesByDefault=enable_favorites_by_default)

    @property
    def default_editor_mode(self) -> EditorMode:
        """Default markdown editor mode (personal field)"""
        return self.schema.get('defaultEditorMode', 'wysiwyg')
    @default_editor_mode.setter
    def default_editor_mode(self, default_editor_mode: EditorMode) -> None:
        """Set default markdown editor mode (personal field)"""
        self.update(defaultEditorMode=default_editor_mode)

    @property
    def default_home_view(self) -> HomeView | None:
        """Default view mode for the home page (personal field)"""
        return self.schema.get('defaultHomeView')
    @default_home_view.setter
    def default_home_view(self, default_home_view: HomeView) -> None:
        """Default view mode for the home page (personal field)"""
        self.update(defaultHomeView=default_home_view)

    @property
    def default_projects_order(self) -> ProjectOrdering | None:
        """Default sort order for projects display (personal field)"""
        return self.schema.get('defaultProjectsOrder')
    @default_projects_order.setter
    def default_projects_order(self, default_projects_order: ProjectOrdering) -> None:
        """Default sort order for projects display (personal field)"""
        self.update(defaultProjectsOrder=default_projects_order)
    
    @property
    def terms_type(self) -> TermsType:
        """Type of terms applicable to the user based on role"""
        return self.schema['termsType']
    
    @property
    def is_sso_user(self) -> bool:
        """Whether the user is SSO user (private field)"""
        return self.schema.get('isSsoUser', False)
    
    @property
    def is_deactivated(self) -> bool:
        """Whether the user account is deactivated and cannot log in"""
        return self.schema['isDeactivated']
    
    @property
    def is_default_admin(self) -> bool:
        """Whether the user is the default admin (visible only to current user or admin)"""
        return self.schema.get('isDefaultAdmin', False)
    
    @property
    def locked_field_names(self) -> list[LockableField]:
        """List of fields locked from editing (visible only to current user or admin)"""
        return self.schema.get('lockedFieldNames', [])
    
    @property
    def created_at(self) -> datetime:
        """When the user was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the user was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the User with the Planka server (Can only sync your own User)"""
        if self.id == self.session.me.id:
            self.schema = self.session.me.schema

    def update(self, **kwargs: Unpack[paths.Request_updateUser]):
        """Update the User"""
        self.schema = self.endpoints.updateUser(self.id, **kwargs)['item']

    def delete(self):
        """Delete the User"""
        return self.endpoints.deleteUser(self.id)
    
    def update_email(self, email: str, 
                     *, 
                     password: str|None=None) -> None:
        """Update the current User's email
        
        Args:
            password (str): The User's password (required if not admin)

        Raises:
            PermissionError: If the current user is not admin and attempts to set another user's password
            PermissionError: If the current user is not admin and the `password` arg is not set
            HTTPStatusError: If the password is wrong or the update operation fails
        """
        
        # Allow Admins to set user email directly or ignore password kwarg
        if self.current_role == 'admin':
            self.endpoints.updateUserEmail(self.id, email=email)
            return
        
        if self.current_id != self.id:
            raise PermissionError(f'Cannot set other User emails unless admin')
        
        if not password:
            raise PermissionError(f'User password required to update email!')
        
        self.endpoints.updateUserEmail(self.id, email=email, currentPassword=password)

    def update_password(self, 
                        *, 
                        new_password: str, 
                        current_password: str|None=None) -> None:
        """Update the User's password
        
        Args:
            new_password (str): The new password to use
            current_password (str): The User's current password (required for non-admin)
        
        Raises:
            PermissionError: If a non-admin attempts to update another user's password
            PermissionError: If a user attempts to update their own password without passing a `current_password`
            HTTPStatusError: If the password is wrong or the update operation fails
        """
        # Admins can set any User password
        if self.current_role == 'admin':
            self.endpoints.updateUserPassword(self.id, password=new_password)
            return
        
        # Users's cannot set other user's passwords
        if self.current_id != self.id:
            raise PermissionError(f"Cannot set another User's password! (must be admin)")
        
        # Password change required current password
        if not current_password:
            raise PermissionError(f'Cannot set other User passwords unless admin')

        self.endpoints.updateUserPassword(self.id, password=new_password, currentPassword=current_password)

    def add_to_card(self, card: Card) -> None:
        """Add the User to a Card
        
        Args:
            card (Card): The Card to add the user to (must be a member of the Card's Board)
        
        Raises:
            PermissionError: If the User is not a member of the Card's Board
        
        Note:
            If the User is already a Card member, no changes will be made
        """
        
        if self not in card.board.users:
            raise PermissionError(f'User is not a member of the Board')
        
        if self not in card.members:
            self.endpoints.createCardMembership(card.id, userId=self.id)
    
    def remove_from_card(self, card: Card) -> None:
        """Remove the User from a Card
        
        Args:
            card (Card): The Card to remove the User from
        
        Note:
            if the User is not a member of the Card, no change will be made
        """
        if self in card.members:
            card.remove_member(self)
    
    def add_to_board(self, board: Board, 
                     *,
                     role: BoardRole='viewer',
                     can_comment: bool=False) -> None:
        """Add the User to a board
        
        Args:
            role (Literal['viewer', 'editor']): The role of the User in the Board (default: `viewer`)
            can_comment (bool): The comment permission for the user if `role` is set to `viewer` (default: `False`)
            
        Note:
            If the User is already a Board member, but the role or comment permission are different, 
            the User role and comment permission will be updated
        """
        board.add_member(self, role=role, can_comment=can_comment)
        
    def remove_from_board(self, board: Board) -> None:
        """Remove the User from a Board
        
        Note:
            If the User is not a Board member, no change will be made
        """
        if self in board.users:
            board.remove_user(self)
