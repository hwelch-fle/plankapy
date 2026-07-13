from __future__ import annotations

from datetime import datetime
from typing import Unpack

from ..api import events, schemas, typ
from ._base import PlankaModel
from ._helpers import dtfromiso
from ._literals import BoardRole

# Deferred Model imports at bottom of file

__all__ = ('BoardMembership', )


class BoardMembership(PlankaModel[schemas.BoardMembership]):
    """Python interface for Planka BoardMemberships"""

    __events__ = events.BoardMembershipEvents

    # BoardMembership properties

    @property
    def project(self) -> Project:
        """The Project the BoardMembership belongs to"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)

    @property
    def board(self) -> Board:
        """The Board the BoardMembership is associated with"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)

    @property
    def user(self) -> User:
        """The User the BoardMembership is associated with

        Raises:
            LookupError: User no longer in the Board
        """
        if usr := self.board.users[{'userId': self.user.id}].dpop():
            return usr
        raise LookupError(f"Cannot find User: {self.schema['userId']}")

    @property
    def role(self) -> BoardRole:
        """Role of the user in the board"""
        return self.schema['role']

    @role.setter
    def role(self, role: BoardRole) -> None:
        """Set the role of the User in the Board"""
        self.update(role=role)

    @property
    def can_comment(self) -> bool:
        """Whether the user can comment on cards"""
        if self.role == 'viewer':
            return self.schema['canComment']
        return True

    @can_comment.setter
    def can_comment(self, can_comment: bool) -> None:
        """Set if a viewer User can comment"""
        if self.role == 'viewer':
            self.update(canComment=can_comment)

    @property
    def created_at(self) -> datetime:
        """When the board membership was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the board membership was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the BoardMembership with the Planka server"""
        if bms := self.board.board_memberships[{'id': self.id}].dpop(default=self):
            self.schema = bms.schema

    def update(self, **kwargs: Unpack[typ.Request_updateBoardMembership]) -> None:
        """Update the BoardMembership"""
        self.schema = self.endpoints.updateBoardMembership(self.id, **kwargs)['item']

    def delete(self):
        """Delete the BoardMebership"""
        return self.endpoints.deleteBoardMembership(self.id)


from .board import Board
from .project import Project
from .user import User
