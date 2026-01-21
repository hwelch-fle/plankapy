from __future__ import annotations

__all__ = ('Board', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Unpack
    #from models import *
    from ._literals import CardType, BoardRole, BoardView


class Board(PlankaModel[schemas.Board]):
    """Python interface for Planka Boards"""
    
    @property
    def url(self) -> str:
        return str(self.client.base_url.join(f'/boards/{self.id}'))
    
    # Included objects
    @property
    def _included(self):
        return self.endpoints.getBoard(self.id)['included']
    
    @property
    def labels(self) -> list[Label]:
        """Get all Labels on the Board"""
        return [Label(l, self.session) for l in self._included['labels']]
    
    @property
    def cards(self) -> list[Card]:
        """Get all active Cards on the Board (use archived_cards and trashed_cards for archived/trashed Card lists)"""
        return [Card(c, self.session) for c in self._included['cards']]
    
    @property
    def trashed_cards(self) -> list[Card]:
        """Get all Cards in the Board trash list"""
        return [Card(c, self.session) for c in self.endpoints.getCards(self.trash_list.id)['items']]
    
    @property
    def archived_cards(self) -> list[Card]:
        """Get all Cards in the Board archive list"""
        return [Card(c, self.session) for c in self.endpoints.getCards(self.archive_list.id)['items']]

    @property
    def subscribed_cards(self) -> list[Card]:
        """Get all Cards on the Board that the current User is subscribed to"""
        return [Card(sc, self.session) for sc in self._included['cards'] if sc['isSubscribed']]
    
    @property
    def projects(self) -> list[Project]:
        """Get all Projects that the Board is associated with (use `Board.Project` instead, this is always one item)"""
        return [Project(p, self.session) for p in self._included['projects']]
    
    @property
    def board_memberships(self) -> list[BoardMembership]:
        """Get all BoardMemberships for the Board"""
        return [BoardMembership(bm, self.session) for bm in self._included['boardMemberships']]
    
    @property
    def users(self) -> list[User]:
        """Get all Users on the Board"""
        return [User(u, self.session) for u in self._included['users']]

    @property
    def editors(self) -> list[User]:
        """Get all editor Users for the Board"""
        return [bm.user for bm in self.board_memberships if bm.role == 'editor']
    
    @property
    def viewers(self) -> list[User]:
        """Get all viewer Users for the Board"""
        return [bm.user for bm in self.board_memberships if bm.role == 'editor']

    @property
    def all_lists(self) -> list[List]:
        """Get all Lists associated with the Board"""
        return [List(l, self.session) for l in self._included['lists']]
    
    @property
    def card_memberships(self) -> list[CardMembership]:
        """Get all CardMemberships associated with the Board"""
        return [CardMembership(cm, self.session) for cm in self._included['cardMemberships']]
    
    @property
    def card_labels(self) -> list[CardLabel]:
        """Get all CardLabels associated with the Board"""
        return [CardLabel(cl, self.session) for cl in self._included['cardLabels']]
    
    @property
    def task_lists(self) -> list[TaskList]:
        """Get all TaskLists associated with the Board"""
        return [TaskList(tl, self.session) for tl in self._included['taskLists']]
    
    @property
    def tasks(self) -> list[Task]:
        """Get all Tasks associated with the Board"""
        return [Task(t, self.session) for t in self._included['tasks']]
    
    @property
    def attachments(self) -> list[Attachment]:
        """Get all Attachments associated with the Board"""
        return [Attachment(a, self.session) for a in self._included['attachments']]
    
    @property
    def custom_field_groups(self) -> list[CustomFieldGroup]:
        """Get all CustomFieldGroups associated with the Board"""
        return [CustomFieldGroup(cfg, self.session) for cfg in self._included['customFieldGroups']]
    
    @property
    def custom_fields(self) -> list[CustomField]:
        """Get all CustomFields associated with the Board"""
        return [CustomField(cf, self.session) for cf in self._included['customFields']]
    
    @property
    def custom_field_values(self) -> list[CustomFieldValue]:
        """Get all CustomFieldValues associated with the Board"""
        return [CustomFieldValue(cfv, self.session) for cfv in self._included['customFieldValues']]
    
    @property
    def archive_list(self) -> List:
        """Get the archive List for the Board (archive List is not a normal List!)"""
        return [l for l in self.all_lists if l.type == 'archive'].pop()
    
    @property
    def trash_list(self) -> List:
        """Get the trash List for the Board (trash List is not a normal List!)"""
        return [l for l in self.all_lists if l.type == 'trash'].pop()
    
    @property
    def active_lists(self) -> list[List]:
        """Get all active Lists for the Board"""
        return [l for l in self.all_lists if l.type == 'active']
    
    @property
    def closed_lists(self) -> list[List]:
        """Get all closed Lists for the Board"""
        return [l for l in self.all_lists if l.type == 'closed']

    # Board props
    @property
    def subscribed(self) -> bool:
        """Whether the current user is subscribed to the Board"""
        return self.endpoints.getBoard(self.id)['item']['isSubscribed']
    
    @property
    def project(self) -> Project:
        """TheProject the Board belongs to"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)
    
    @property
    def position(self) -> int:
        """Position of the Board within the Project"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Position of the Board within the Project"""
        self.update(position=position)

    @property
    def name(self) -> str:
        """Name/title of the Board"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the name/title of the Board"""
        self.update(name=name)

    @property
    def default_view(self) -> BoardView:
        """Default view for the board"""
        return self.schema['defaultView']
    @default_view.setter
    def default_view(self, default_view: BoardView) -> None:
        """Set default view for the board"""
        self.update(defaultView=default_view)

    @property
    def default_card_type(self) -> CardType:
        """Default Card type for new Cards"""
        return self.schema['defaultCardType']
    @default_card_type.setter
    def default_card_type(self, default_card_type: CardType) -> None:
        """Set default Card type for new Cards"""
        self.update(defaultCardType=default_card_type)

    @property
    def limit_card_types_to_default_one(self) -> bool:
        """Whether to limit Card types to default one"""
        return self.schema['limitCardTypesToDefaultOne']
    @limit_card_types_to_default_one.setter
    def limit_card_types_to_default_one(self, limit_card_types_to_default_one: bool) -> None:
        """Set whether to limit Card types to default one"""
        self.update(limitCardTypesToDefaultOne=limit_card_types_to_default_one)

    @property
    def always_display_card_creator(self) -> bool:
        """Whether to always display the Card creator"""
        return self.schema['alwaysDisplayCardCreator']
    @always_display_card_creator.setter
    def always_display_card_creator(self, always_display_card_creator: bool) -> None:
        """Set whether to always display the Card creator"""
        self.update(alwaysDisplayCardCreator=always_display_card_creator)

    @property
    def expand_task_lists_by_default(self) -> bool:
        """Whether to expand TaskLists by default"""
        return self.schema['expandTaskListsByDefault']
    @expand_task_lists_by_default.setter
    def expand_task_lists_by_default(self, expand_task_lists_by_default: bool) -> None:
        """Set whether to expand TaskLists by default"""
        self.update(expandTaskListsByDefault=expand_task_lists_by_default)

    @property
    def created_at(self) -> datetime:
        """When the Board was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    @property
    def updated_at(self) -> datetime:
        """When the Board was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
    # Special Methods
    def sync(self) -> None:
        """Sync the Board with the Planka Server"""
        self.schema = self.endpoints.getBoard(self.id)['item']
        
    def update(self, **board: Unpack[paths.Request_updateBoard]) -> None:
        """Update the Board"""
        self.schema = self.endpoints.updateBoard(self.id, **board)['item']
        
    def delete(self):
        """Delete the Board"""
        return self.endpoints.deleteBoard(self.id)

    def create_list(self, **lst: Unpack[paths.Request_createList]) -> List:
        """Create a new List on the Board"""
        return List(self.endpoints.createList(self.id, **lst)['item'], self.session)

    def remove_list(self, list: List) -> None:
        """Remove a List from the Board
        
        Args:
            list (List): The list to remove (must be associated with the Board and not `trash` or `archive`)
        """
        if list in self.active_lists:
            list.delete()

    def create_label(self, **lbl: Unpack[paths.Request_createLabel]) -> Label:
        """Create a new Label on the Board"""
        return Label(self.endpoints.createLabel(self.id, **lbl)['item'], self.session)
    
    def remove_label(self, label: Label) -> None:
        """Remove a Label from the Board
        
        Args:
            label (Label): The Label to remove (must be associated with the board)
        """
        if label in self.labels:
            label.delete()
    
    def add_member(self, user: User, 
                   *,
                   role: BoardRole='viewer',
                   can_comment: bool=False) -> BoardMembership:
        """Add a User to the Board
        
        Args:
            user (User): The User to add
            role (Literal['viewer', 'editor']): The Role to assign to the user (default: `viewer`)
            can_comment (bool): If role is `viewer` set commenting status (default: `False`)
        """
        # Create a new membership
        if user not in self.users:
            BoardMembership(
                self.endpoints.createBoardMembership(
                    self.id, 
                    userId=user.id, 
                    role=role, 
                    canComment=can_comment)['item'], 
                self.session
            )
        
        # Get existing membership and update role different
        membership = [bm for bm in self.board_memberships if bm.user == user].pop()
        if membership.role != role:
            membership.role = role
        if membership.can_comment != can_comment:
            membership.can_comment = can_comment
        return membership
    
    def add_members(self, users: Sequence[User], 
                    *,
                    role: BoardRole='viewer',
                    can_comment: bool=False) -> list[BoardMembership]:
        """Add a Users to the Board
        
        Args:
            users (Sequence[User]): The Users to add
            role (Literal['viewer', 'editor']): The Role to assign to the user (default: `viewer`)
            can_comment (bool): If role is `viewer` set commenting status (default: `False`)
            
        Returns:
            list[BoardMembership]
        """
        return [
            self.add_member(
                user,
                role=role,
                can_comment=can_comment,
            )
            for user in users
        ]
    
    def add_editor(self, user: User) -> BoardMembership:
        """Add a Board editor
        
        Args:
            user (User): The User to add as an editor
            
        Returns:
            BoardMembership
        """
        return self.add_member(user, role='editor', can_comment=True)

    def add_editors(self, users: Sequence[User]) -> list[BoardMembership]:
        """Add Board editors
        
        Args:
            users (Sequence[User]): The Users to add as editors
            
        Returns:
            list[BoardMembership]
        """
        return [self.add_editor(user) for user in users]

    def add_viewer(self, user: User, *, can_comment: bool=False) -> BoardMembership:
        """Add a Board viewer
        
        Args:
            user (User): The User to add as a viewer
            can_comment (bool): Whether the viewer User can comment on cards
            
        Returns:
            BoardMembership
        """
        return self.add_member(user, role='viewer', can_comment=can_comment)

    def add_viewers(self, users: Sequence[User], *, can_comment: bool=False) -> list[BoardMembership]:
        """Add a Board viewer
        
        Args:
            users (Sequence[User]): The Users to add as viewers
            can_comment (bool): Whether the viewer Users can comment on cards
            
        Returns:
            list[BoardMembership]
        """
        return [self.add_viewer(user, can_comment=can_comment) for user in users]

    def remove_user(self, user: User) -> None:
        """Remove a User from the Board
        
        Note:
            If the User is not a member, no change will be made
        """
        if user in self.users:
            [bm for bm in self.board_memberships if bm.user == user].pop().delete()
    
    def remove_users(self, users: Sequence[User]) -> None:
        """Remove Users from the Board
        
        Note:
            If a User is not a member, no change will be made
        """
        for user in users:
            self.remove_user(user)

from .project import Project
from .user import User
from .card import Card
from .board_membership import BoardMembership
from .custom_field import CustomField
from .list import List
from .label import Label
from .card_label import CardLabel
from .card_membership import CardMembership
from .custom_field import CustomField
from .custom_field_group import CustomFieldGroup
from .custom_field_value import CustomFieldValue
from .task import Task
from .task_list import TaskList
from .attachment import Attachment