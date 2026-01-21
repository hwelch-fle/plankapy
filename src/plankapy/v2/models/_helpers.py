from datetime import datetime, timezone
from collections.abc import Sequence
from typing import Any, Literal, Protocol

__all__ = ('dtfromiso', 'get_position', 'Position')

def dtfromiso(iso: str, default_timezone: timezone=timezone.utc) -> datetime:
    """Convert an ISO 8601 string to an offset aware datetime

    Args:
        iso (str): The ISO 8601 string to convert to a datetime
        default_timezone (timezone): The timezone to interpret the ISO string in (default: timezone.utc)

    Note:
        If the ISO 8601 timestamp contains tzinfo, that will be used. The `default_timezone` arg 
        will only be used on ISO 8601 strings that don't contain timezone info 
    """
    dt = datetime.fromisoformat(iso)
    if not dt.tzinfo:
        return dt.replace(tzinfo=default_timezone)
    return dt

def dttoiso(dt: datetime, default_timezone: timezone=timezone.utc) -> str:
    """Convert an offset aware datetime to an ISO 8601 string. 
    
    timezone check is `dt.tzinfo` -> `default_timezone`

    Args:
        dt (datetime): The datetime to convert
        default_timezone (timezone): The timezone to interpret the ISO string in (default: timezone.utc)
    """
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=default_timezone)
    return str(dt)

# Position Offset
POSITION_GAP = 65536

class HasPosition(Protocol):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.position: int

Position = Literal['top', 'bottom'] | int

def get_position(items: Sequence[HasPosition], position: Literal['top', 'bottom'] | int) -> int:
    """Get a top/bottom position"""
    if isinstance(position, int):
        return position
    if position != 'bottom':
        return 0
    return max((i.position for i in items), default=0) + POSITION_GAP