from __future__ import annotations

__all__ = ('TaskList', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import Position, dtfromiso, get_position, model_list
from ..api import schemas, paths, events

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    #from models import *


class TaskList(PlankaModel[schemas.TaskList]):
    """Python interface for Planka TaskLists"""
    
    __events__ = events.TaskListEvents

    # TaskList included

    @property
    def _included(self):
        return self.endpoints.getTaskList(self.id)['included']
    
    @property
    @model_list
    def tasks(self) -> list[Task]:
        """All Tasks associated with the TaskList"""
        return [Task(t, self.session) for t in self._included['tasks']]

    # TaskList props

    @property
    def card(self) -> Card:
        """The Card the TaskList belongs to"""
        return Card(self.endpoints.getCard(self.schema['cardId'])['item'], self.session)
    
    @property
    def position(self) -> int:
        """Position of the TaskList within the Card"""
        return self.schema['position']
    @position.setter
    def positon(self, position: int) -> None:
        """Set the TaskList position within the Card"""
        self.update(position=position)

    @property
    def name(self) -> str:
        """Name/title of the TaskList"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the TaskList"""
        self.update(name=name)

    @property
    def show_on_front_of_card(self) -> bool:
        """Whether to show the TaskList on the front of the Card"""
        return self.schema['showOnFrontOfCard']
    @show_on_front_of_card.setter
    def show_on_front_of_card(self, show_on_front_of_card: bool) -> None:
        """Set whether to show TaskList on the front of the Card"""

    @property
    def hide_completed_tasks(self) -> bool:
        """Whether to hide completed Tasks"""
        return self.schema['hideCompletedTasks']
    @hide_completed_tasks.setter
    def hide_completed_tasks(self, hide_completed_tasks: bool) -> None:
        """Set whether to hide completed Tasks"""
        self.update(hideCompletedTasks=hide_completed_tasks)

    @property
    def created_at(self) -> datetime:
        """When the TaskList was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the TaskList was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the TaskList with the Planka server"""
        self.schema = self.endpoints.getTaskList(self.id)['item']

    def update(self, **kwargs: Unpack[paths.Request_updateTaskList]):
        """Update the TaskList"""
        self.schema = self.endpoints.updateTaskList(self.id, **kwargs)['item']

    def delete(self):
        """Delete the TaskList"""
        self.endpoints.deleteTaskList(self.id)

    def add_task(self, name: str, *, 
                 is_completed: bool=False, 
                 position: Position='top',
                 linked_card: Card|None=None) -> Task:
        """Create a new Task in the TaskList
        
        Args:
            name (str): The name of the task
            is_completed (bool): Is the task completed or not (default: `False`)
            position (Position | int): Position of the task in the TaskList (default: `top`)
            linked_card (Card|None): Optional Card to link the Task to (default: `None`)
        """
        args = { # type: ignore
            'name': name,
            'position': get_position(self.tasks, position),
            'isCompleted': is_completed
        }
        if linked_card is not None:
            args['linkedCardId'] = linked_card.id

        return Task(
            self.endpoints.createTask(
                self.id, 
                **args, # type: ignore
                )['item'],  
            self.session
        )


from .card import Card
from .task import Task