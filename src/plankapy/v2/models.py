from __future__ import annotations
from typing import TypedDict, Literal, Required, Any

JSON = dict[str, Any]
ActionType = Literal[
    "createCard",
    "moveCard",
    "addMemberToCard",
    "removeMemberFromCard",
    "completeTask",
    "uncompleteTask",
]

AttachmentType = Literal[
    "file",
    "link",
]

BoardView = Literal[
    "kanban",
    "grid",
    "list",
]

BoardImportType = Literal["trello",]

CardType = Literal[
    "project",
    "story",
]


class Action(TypedDict, total=False):
    id: str
    type: Required[ActionType]
    data: Required[JSON]
    cardId: Required[Card]
    boardId: Board
    userId: User


class Attachment(TypedDict, total=False):
    id: str
    type: Required[AttachmentType]
    data: Required[JSON]
    name: Required[str]
    cardId: Required[Card]
    creatorUserId: User


class BackgroundImage(TypedDict, total=False):
    id: str
    extension: Required[str]
    size: Required[str]
    uploadedFileId: Required[UploadedFile]
    projectId: Required[Project]


class BaseCustomFieldGroup(TypedDict, total=False):
    id: str
    name: Required[str]
    projectId: Required[Project]


class Board(TypedDict, total=False):
    id: str
    position: Required[int]
    name: Required[str]
    defaultView: Required[BoardView]  # default: `kanban`
    defaultCardType: Required[CardType]  # default: `project`
    limitCardTypesToDefaultOne: Required[bool]  # default: `False`
    alwaysDisplayCardCreator: Required[bool]  # default: `False`
    expandTaskListsByDefault: Required[bool]  # default: `False`
    projectId: Required[Project]
    memberUsers: list[User]  # through: BoardMembership
    lists: list[List]  # via: list['boardId']
    labels: list[Label]  # via: label['boardId']


class BoardMembership(TypedDict, total=False): ...


class BoardSubscription(TypedDict, total=False): ...


class Card(TypedDict, total=False): ...


class CardLabel(TypedDict, total=False): ...


class CardMembership(TypedDict, total=False): ...


class CardSubscription(TypedDict, total=False): ...


class Comment(TypedDict, total=False): ...


class Config(TypedDict, total=False): ...


class CustomField(TypedDict, total=False): ...


class CustomFieldGroup(TypedDict, total=False): ...


class CustomFieldValue(TypedDict, total=False): ...


class IdentityProviderUser(TypedDict, total=False): ...


class Label(TypedDict, total=False): ...


class List(TypedDict, total=False): ...


class Notification(TypedDict, total=False): ...


class NotificationService(TypedDict, total=False): ...


class Project(TypedDict, total=False): ...


class ProjectFavorite(TypedDict, total=False): ...


class ProjectManager(TypedDict, total=False): ...


class Session(TypedDict, total=False): ...


class StorageUsage(TypedDict, total=False): ...


class Task(TypedDict, total=False): ...


class TaskList(TypedDict, total=False): ...


class UploadedFile(TypedDict, total=False): ...


class User(TypedDict, total=False): ...


class Webhook(TypedDict, total=False): ...
