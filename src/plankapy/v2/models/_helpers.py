"""
Helper objects for implemented model classes
"""
from __future__ import annotations

from datetime import datetime, timezone
from collections.abc import Sequence, Callable, Mapping
from functools import wraps
from typing import (
    Any, 
    Literal,
    ParamSpec,
    Protocol, 
    SupportsIndex,
    TypeVar, 
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

def match[M: PlankaModel[Any]](item: M, pred: Callable[[M], bool] | M) -> bool:
    """Evaluate a Callable on the item if provided, else evaluate equality
    
    Note:
        predicate functions are not checked for validity, the value will be passed 
        directly and exceptions will be raised if the predicate raises one
    """
    if isinstance(pred, Callable):
        return pred(item)
    return item == pred


# Type declarations for the filter indexing options available to a ModelList
type FilterFunc[M, *P] = Callable[[M,*P], bool]
type KeyFilter[T, *P] = dict[str, Callable[[T, *P], bool]]
type Id = str
type ModelListIndexable[T, M] = SupportsIndex | slice | KeyFilter[T] | dict[str, Any] | Id | FilterFunc[M] | M

class ModelList[M: PlankaModel[Mapping[str, Any]]](list[M]):
    @overload
    def __getitem__(self, key: SupportsIndex) -> M: ...
    """Index the list normally"""
    @overload
    def __getitem__(self, key: slice) -> ModelList[M]: ...
    """Slice the list normally"""
    @overload
    def __getitem__[T](self, key: KeyFilter[T]) -> ModelList[M]: ...
    """Filter the list using a schema filter (allows function evaluation of schema value)"""
    @overload
    def __getitem__(self, key: dict[str, Any]) -> ModelList[M]: ...
    @overload
    def __getitem__(self, key: Id) -> M: ...
    @overload
    def __getitem__(self, key: FilterFunc[M]) -> ModelList[M]: ...
    """Filter the list using a functional filter"""
    @overload
    def __getitem__(self, key: M) -> ModelList[M]: ...
    """Allow getting all models in the ModelList that match the input model"""
    def __getitem__[T](self, key: ModelListIndexable[T, M]) -> M | ModelList[M]:
        match key:
            case SupportsIndex():
                return super().__getitem__(key)
            case slice():
                return ModelList(super().__getitem__(key))
            case str():
                return [i for i in self if i.id == key].pop()
            case dict():
                return ModelList(
                    i for i in self
                    if key.keys() <= i.schema.keys()
                    and all(match(i.schema[k], key[k]) for k in key)
                )
            case PlankaModel():
                return ModelList(i for i in self if i == key)
            case Callable():
                return ModelList(i for i in self if key(i))
            case _:
                raise ValueError(f'{type(key)} not supported for indexing')

    def dpop[D](self, index: SupportsIndex=-1, *, default: D=None) -> M | D:
        """pop but accept a `default` argument"""
        try:
            return super().pop(index)
        except IndexError:
            return default
    
    @overload
    def extract(self, key: str, /) -> list[Any]: ...
    @overload
    def extract(self, *keys: str) -> list[tuple[Any, ...]]: ...
    def extract(self, *keys: str) -> list[tuple[Any, ...] | Any]:
        """Extract values from the items in the ModelList
        
        Args:
            keys: The schema key to extract
        """
        if len(keys) == 1:
            return [i[keys[0]] for i in self]
        return [tuple(i[key] for key in keys) for i in self]

    def ids(self) -> list[str]:
        """A list of model ids"""
        return [i.id for i in self]
    
    def format(self, func: Callable[[M], str]) -> list[str]:
        """Apply a format function to all items in the ModelList
        
        Args:
            func: A function that takes a model and returns a string
        """
        return [func(i) for i in self]
    

P = ParamSpec('P')
T = TypeVar('T', bound=PlankaModel[Any])
def queryable(func: Callable[P, list[T]]) -> Callable[P, ModelList[T]]:
    """Wrapper that turns a list property into a ModelList"""
    @wraps(func)
    def _wrapper(*args: Any, **kwargs: Any) -> ModelList[T]:
        return ModelList(func(*args, **kwargs))
    return _wrapper
