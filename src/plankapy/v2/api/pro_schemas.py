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


class Project(schemas.Project):
    backgroundStockImage: str
    backgroundFilter: Literal['TBD']
    backgroundFilterStrength: int


class Board(schemas.Board):
    type: Literal['TBD']
    canGuestsSeeOtherGuests: bool
    setCoverAttachmentsVisibleToGuestsAutomatically: bool
    setCoverLinkAttachmentsVisibleToGuestsAutomatically: bool
    startWithEmptyBoard: bool
    notice: str
    isNoticeEnabled: bool


class List(schemas.List):
    # Added a `recurring` list type
    type: Literal['active', 'closed', 'archive', 'trash', 'recurring'] # type: ignore


class User(schemas.User):
    hideIdentityFromGuests: bool

    # Added `guest?`
    role: Literal['admin', 'projectOwner', 'boardUser', 'guest'] # type: ignore
    canBeUsedByWorkers: bool
    canBeUsedByGuests: bool


class CustomFieldGroup(schemas.CustomFieldGroup):
    canBeUsedByWorkers: bool
    isVisibleToGuests: bool


class BoardMembership(schemas.BoardMembership):
    hideIdentityFromGuests: bool
    canSeeOnlyAssignedCards: bool | None
    canAccessInbox: bool | None
    canCreateCards: bool | None
    canInteractWithGuests: bool | None
    canUseInbox: bool | None
    # Different from canComment?
    canUseComments: bool | None


class Attachment(schemas.Attachment):
    isVisibleToGuests: bool


class Comment(schemas.Comment):
    userRoleSummary: str
    isIdentityHiddenFromGuests: bool | None
    isPinned: bool