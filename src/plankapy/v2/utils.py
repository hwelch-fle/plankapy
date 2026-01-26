"""
Utility functions for dealing with Planka objects
"""
from itertools import zip_longest

from pathlib import Path
from .models import *

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