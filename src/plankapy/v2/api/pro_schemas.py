from __future__ import annotations

from typing import Literal, NotRequired, TypedDict
from . import schemas

__all__ = (
    "Card",
)

class Card(schemas.Card):
    isDraft: bool
    locationName: str
    locationCoordinates: tuple[float, float]
    recurrence: Recurrence
    recurrenceDestination: Literal['firstActiveList', 'firstList', 'inbox']
    recurrenceDueDateOffset: str
    skipDuplicateRecurrence: bool
    recurrenceStartedAt: str
    lastRecurredAt: str
    startDate: str
    sourceList: str
    sourceLabels: list[str]
    sourceId: str
    coverLinkAttachmentId: str
    
class Recurrence(TypedDict):
    time: str
    interval: int
    timezone: str
    frequency: Literal['daily', 'weekly', 'monthly', 'yearly']