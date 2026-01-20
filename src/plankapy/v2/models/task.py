from __future__ import annotations

__all__ = ('Task', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    from models import *


class Task(PlankaModel[schemas.Task]):
    """Python interface for Planka Tasks"""

    # Task props

    @property
    def task_list(self) -> TaskList:
        """The TaskList the Task belongs to"""
        return TaskList(self.endpoints.getTaskList(self.schema['taskListId'])['item'], self.session)
    @task_list.setter
    def task_list(self, task_list: TaskList) -> None:
        """Move the Task to a different TaskList"""
        self.update(taskListId=task_list.id)

    @property
    def card(self) -> Card:
        """The Card the Task is linked to"""
        return Card(self.endpoints.getCard(self.schema['linkedCardId'])['item'], self.session)

    @property
    def assignee(self) -> User | None:
        """The User assigned to the Task if there is one"""
        _usrs = [u for u in self.card.board.users if self.schema['assigneeUserId'] == u.id]
        if _usrs:
            return _usrs.pop()
        raise LookupError(f"Cannot find User: {self.schema['assigneeUserId']}")
    @assignee.setter
    def assignee(self, assignee: User | None) -> None:
        """Assign a User to the Task"""
        # TODO: Fix _build to add <Type> | None to `nullable` fields
        if assignee is not None:
            self.update(assigneeUserId=assignee.id)
        else:
            self.update(assigneeUserId=None) # type: ignore

    @property
    def position(self) -> int:
        """Position of the Task within the TaskList"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Set the position of the Task within the TaskList"""
        self.update(position=position)
        
    @property
    def name(self) -> str:
        """Name/title of the Task"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the Task name"""
        self.update(name=name)

    @property
    def is_completed(self) -> bool:
        """Whether the Task is completed"""
        return self.schema['isCompleted']
    @is_completed.setter
    def is_completed(self, is_completed: bool) -> None: 
        """Set whether the Task is completed"""
        self.update(isCompleted=is_completed)

    @property
    def created_at(self) -> datetime:
        """When the Task was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)

    @property
    def updated_at(self) -> datetime:
        """When the Task was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the Task with the Planka server"""
        _tsks = [tsk for tsk in self.task_list.tasks if tsk == self]
        if _tsks:
            self.schema = _tsks.pop().schema

    def update(self, **kwargs: Unpack[paths.Request_updateTask]):
        """Update the Task"""
        self.schema = self.endpoints.updateTask(self.id, **kwargs)['item']

    def delete(self):
        """Delete the Task"""
        self.endpoints.deleteTask(self.id)
