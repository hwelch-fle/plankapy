"""
Utility functions for dealing with Planka objects
"""
from datetime import datetime, timedelta, timezone
from itertools import zip_longest

from pathlib import Path
from typing import Any, Protocol, TypedDict
from .models import *
from .interface import Planka

__all__ = ('due_in', 'board_to_csv', 'board_to_table', 'snapshot', )

class HasDueDate(Protocol):
    @property
    def due_date(self) -> datetime | None: ...
    
def due_in(hours: float=0, days: float=0, weeks: float=0):
    """Decorated function for use with """
    def _inner(m: HasDueDate):
        if not m.due_date:
            return False
        by = timedelta(days=days, hours=hours, weeks=weeks)
        return (m.due_date - by) <= datetime.now(tz=timezone.utc)
    return _inner

def board_to_table(board: Board) -> list[list[str]]:
    """Get a nested list/table for the board. 
    Uses `name` attributes of cards and lists
    
    Args:
        board: The board object to tablify
    
    Returns:
        A matrix of string lists with the first element being list names 
        and the remaining elements being card names from left to right    
        ```
        [
            ['list1', 'list2'],
            ['l1 c1', 'l2 c1'],
            ['l1 c2', 'l2 c2'],
            ...
        ]
        ```
    """
    headers: list[str] = board.lists.extract('name')
    list_cards: list[list[str]] = [
        lst.cards.extract('name')
        for lst in board.lists
    ]
    rows = zip_longest(*list_cards, fillvalue='')
    return [headers]+[list(row) for row in rows]

def board_to_csv(board: Board, outdir: str|Path='.', name: str|None=None):
    """Write the current board state out to a csv file

    Writes out a csv of the board state using `list.name` and `card.name` as 
    the headers and values respectively. Will match visual state of the board.
    
    Args:
        board: The board to export
        outdir: A string or Path to the outpud directory (default: `cwd`)
        name: An optional overrde for the filename (default: `board.name`)
    """
    outfile = Path(outdir) / f'{name or board.name}.csv'
    rows = board_to_table(board)
    with outfile.open('wt') as csv:
        csv.writelines(','.join(row)+'\n' for row in rows)


# System level snapshot of all schemas
from .api import schemas
class PlankaSnapshot(TypedDict):
    projects: list[schemas.Project]
    boards: list[schemas.Board]
    lists: list[schemas.List]
    cards: list[schemas.Card]
    card_labels: list[schemas.CardLabel]
    card_memberships: list[schemas.CardMembership]
    task_lists: list[schemas.TaskList]
    tasks: list[schemas.Task]
    base_custom_field_groups: list[schemas.BaseCustomFieldGroup]
    custom_field_groups: list[CustomFieldGroup]
    custom_fields: list[schemas.CustomField]
    custom_field_values: list[CustomFieldValue]
    comments: list[schemas.Comment]
    webhooks: list[schemas.Webhook]
    users: list[schemas.User]
    board_memberships: list[schemas.BoardMembership]
    project_managers: list[schemas.ProjectManager]
    labels: list[schemas.Label]
    notification_services: list[schemas.NotificationService]
    actions: list[schemas.Action]
    config: schemas.Config

def _get_schema[M: PlankaModel[Any]](models: list[M]):
    return [m.schema for m in models]

def snapshot(planka: Planka) -> PlankaSnapshot:
    """Create a dictionary snapshot of a Planka object. (MUST BE ADMIN)
    All associated schemas are dumped into a single dictionary. 

    Note:
        Since this required traversing all objecs in the system, it can be a very long process. 
        This is best run at a time when not a lot of users are interacting with the board since 
        a 5 minute snapshot could end up with sync errors if state changes over that time.

    Returns:
        A dictonary with all object schemas. Each top level key is a 
    
    Raises:
        PermissionError: If the logged in user is not an admin
    """
    if not planka.me.role == 'admin':
        raise PermissionError('Planka Snapshots can only be done by Admin users!')
    projects = planka.projects
    boards = [b for p in projects for b in p.boards]
    cards = [c for b in boards for c in b.cards]
    lists = [l for b in boards for l in b.lists]
    card_labels = [cl for b in boards for cl in b.card_labels]
    card_memberships = [cm for b in boards for cm in b.card_memberships]
    task_lists = [tl for b in boards for tl in b.task_lists]
    tasks = [t for b in boards for t in b.tasks]
    base_custom_field_groups = [bcfg for p in projects for bcfg in p.base_custom_field_groups]
    custom_field_groups = [cfg for b in boards for cfg in b.custom_field_groups]
    custom_fields = [cf for b in boards for cf in b.custom_fields]
    custom_field_values = [cfv for b in boards for cfv in b.custom_field_values]
    comments = [cm for c in cards for cm in c.comments]
    webhooks = planka.webhooks
    users = planka.users
    board_memberships = [bm for b in boards for bm in b.board_memberships]
    project_managers = [pm for p in projects for pm in p.project_managers]
    labels = [l for b in boards for l in b.labels]
    notification_services = [ns for p in projects for ns in p.notification_services]
    actions = [a for c in cards for a in c.actions]
    config = planka.config

    snap: PlankaSnapshot = {
        'projects': _get_schema(projects),
        'boards': _get_schema(boards),
        'lists': _get_schema(lists),
        'cards': _get_schema(cards),
        'card_labels': _get_schema(card_labels),
        'card_memberships': _get_schema(card_memberships),
        'task_lists': _get_schema(task_lists),
        'tasks': _get_schema(tasks),
        'base_custom_field_groups': _get_schema(base_custom_field_groups),
        'custom_field_groups': _get_schema(custom_field_groups),
        'custom_fields': _get_schema(custom_fields),
        'custom_field_values': _get_schema(custom_field_values),
        'comments': _get_schema(comments),
        'webhooks': _get_schema(webhooks),
        'users': _get_schema(users),
        'board_memberships': _get_schema(board_memberships),
        'project_managers': _get_schema(project_managers),
        'labels': _get_schema(labels),
        'notification_services': _get_schema(notification_services),
        'actions': _get_schema(actions),
        'config': config.schema
    }
    return snap

from .interface import Planka