from datetime import datetime, timezone
from collections.abc import Sequence
from functools import wraps
from typing import (
    Any, 
    Callable, 
    Literal, 
    Protocol, 
    SupportsIndex, 
    overload,
)

from ._base import PlankaModel

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
"""Base position gap for all `positon` fields `(1 == POSITION_GAP*1, 2 == POSITON_GAP*2, ...)`"""

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

class QueryList[M](list[M]):
    @overload
    def __getitem__(self, key: SupportsIndex) -> M: ...
    """Index the list normally"""
    @overload
    def __getitem__(self, key: slice[Any, Any, Any]) -> list[M]: ...
    """Slice the list normally"""
    @overload
    def __getitem__(self, key: dict[str, Any]) -> list[M]: ...
    """Filter the list using a schema filter"""
    @overload
    def __getitem__(self, key: Callable[[M], bool]) -> list[M]: ...
    """Filter the list using a functional filter"""
    def __getitem__(self, key: Any) -> M | list[M]:
        match key:
            case SupportsIndex():
                return self[key]
            case slice():
                return self[key]
            case dict():
                return [
                    i for i in self 
                    if i.schema.keys() <= key.keys() 
                    and all(i.schema[k] == key[k] for k in key) # type: ignore
                ]
            case Callable():
                return [i for i in self if key(i)]
            case _:
                raise ValueError(f'{type(key)} not supported for indexing')

    def dpop[D](self, index: SupportsIndex=-1, *, default: D=None) -> M | D:
        """pop but accept a `default` argument"""
        try:
            return super().pop()
        except IndexError:
            return default
        

def queryable[T](func: Callable[[Any], list[T]]):
    """Wrapper that turns a list property into a QueryList"""
    @wraps(func)
    def _wrapper(self: Any) -> QueryList[T]:
        return QueryList(func(self))
    return _wrapper