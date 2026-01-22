from __future__ import annotations

__all__ = ('Label', )

from datetime import datetime
from ._base import PlankaModel
from ._helpers import Position, dtfromiso, get_position
from ..api import schemas, paths, events

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    #from models import *
    from ._literals import LabelColor


class Label(PlankaModel[schemas.Label]):
    """Python interface for Planka Labels"""
    
    __events__ = events.LabelEvents

    @property
    def board(self) -> Board:
        """The Board the Label belongs to"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)
    
    @property
    def position(self) -> int:
        """Position of the Label within the Board"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Set the position of the Label within the Board"""
        self.update()

    @property
    def name(self) -> str:
        """Name/title of the Label"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the name/title of the Label"""
        self.update(name=name)

    @property
    def color(self) -> LabelColor: 
        """Color of the label"""
        return self.schema['color']
    @color.setter
    def color(self, color: LabelColor) -> None:
        """Set the Label color"""
        self.update(color=color)

    @property
    def created_at(self) -> datetime:
        """When the label was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the label was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
    # Special Methods
    def sync(self):
        """Sync the Label with the Planka server"""
        _lbls = [l for l in self.board.labels if l == self]
        if _lbls:
            self.schema = _lbls.pop().schema

    def update(self, **kwargs: Unpack[paths.Request_updateLabel]):
        """Update the Label"""
        self.schema = self.endpoints.updateLabel(self.id, **kwargs)['item']

    def delete(self):
        """Delete the Label"""
        return self.endpoints.deleteLabel(self.id)

    def add_to_board(self, board: Board, 
                     *, 
                     position: Position='top',
                     color: LabelColor|None=None) -> Label:
        """Add the Label to a Board or return a matching Label from the Board.
        
        Args:
            board (Board): The Board to add the Label to
            position (Position): The position of the Label within the Board (default: `top`)
            color (LabelColor | None): Optionally change the LabelColor in the new Board
        
        Returns:
            Label: The new Label or the matching Label (same color and name)
        
        Note:
            Matching is determines by name and color, if a Label matches on the board, but a color 
            override is set, a new label will be created. If the label is already on the board, the 
            input label is returned
        """
        # Don't re-add label to same board
        if board == self.board:
            return self
        
        # Don't add the Label if one with matching name and color exists
        # If a color override is set, allow the creation of a new label
        for lbl in board.labels:
            if (lbl.name, lbl.color) == (self.name, self.color) and color == self.color:
                return lbl
        
        _schema = self.schema.copy()
        _schema['boardId'] = board.id
        _schema['position'] = get_position(board.labels, position)
        
        # Update color
        if color is not None:
            _schema['color'] = color
        return Label(self.endpoints.createLabel(**_schema)['item'], self.session)

    def get_cards(self) -> list[Card]:
        """All Cards that have this Label in the Board"""
        return [
            cl.card
            for cl in self.board.card_labels
            # Avoid initializing another Label
            if cl.schema['labelId'] == self.schema['id']
        ]


from .board import Board
from .card import Card