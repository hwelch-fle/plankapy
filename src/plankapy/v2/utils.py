"""
Utility functions for dealing with Planka objects
"""
from datetime import datetime, timedelta, timezone
from itertools import zip_longest

from pathlib import Path
from typing import Protocol
from .models import *

__all__ = ('due_in', 'board_to_csv', )

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

def board_to_csv(board: Board, outdir: str|Path='.'):
    outfile = Path(outdir) / f'{board.name}.csv'
    headers: list[str] = board.lists.extract('name')
    list_cards: list[list[str]] = [
        lst.cards.extract('name')
        for lst in board.lists
    ]
    pivot = zip_longest(*list_cards, fillvalue='')
    with outfile.open('wt') as of:
        of.write(','.join(headers)+'\n')
        of.writelines(','.join(row)+'\n' for row in pivot)