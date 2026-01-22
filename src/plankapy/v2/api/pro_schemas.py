from __future__ import annotations

from typing import Literal, NotRequired, TypedDict
from . import schemas

__all__ = (
    "Card",
)

class Card(schemas.Card):
    isDraft: NotRequired[bool]
    locationName: NotRequired[str]
    locationCoordinates: NotRequired[tuple[float, float]]
    recurrence: NotRequired[Recurrence]
    recurrenceDestination: NotRequired[Literal['firstActiveList', 'firstList', 'inbox']]
    recurrenceDueDateOffset: NotRequired[str]
    skipDuplicateRecurrence: NotRequired[bool]
    recurrenceStartedAt: NotRequired[str]
    lastRecurredAt: NotRequired[str]
    startDate: NotRequired[str]
    sourceList: NotRequired[str]
    sourceLabels: NotRequired[list[str]]
    sourceId: NotRequired[str]
    coverLinkAttachmentId: NotRequired[str]
    
class Recurrence(TypedDict):
    time: str
    interval: int
    timezone: str
    frequency: Literal['daily', 'weekly', 'monthly', 'yearly']