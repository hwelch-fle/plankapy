from dataclasses import dataclass
from datetime import datetime

@dataclass
class Action: ...

@dataclass
class Archive: ...

@dataclass
class Attachment: ...

@dataclass
class Board:
    # Included
    attachments: list['Attachment']
    boardMemberships: list['BoardMembership']
    cardLabels: list['CardLabel']
    cards: list['Card']
    labels: list['Label']
    lists: list['List']
    projects: list['Project']
    tasks: list['Task']
    users: list['User']

    # Fields
    createdAt: datetime
    id: str
    name: str
    position: int
    projectId: str
    updatedAt: datetime

@dataclass
class BoardMembership: ...

@dataclass
class Card: ...

@dataclass
class CardLabel: ...

@dataclass
class CardMembership: ...

@dataclass
class CardSubscription: ...

@dataclass
class IdentityProviderUser: ...

@dataclass
class Label: ...

@dataclass
class List: ...

@dataclass
class Notification: ...

@dataclass
class Project:
    # Included
    boardMemberships: list['BoardMembership']
    boards: list['Board']
    projectManagers: list['User']
    users: list['User']

    # Fields
    background: str
    backgroundImage: str
    createdAt: datetime
    id: str
    name: str
    updatedAt: datetime

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'
    

@dataclass
class ProjectManager: ...

@dataclass
class Session: ...

@dataclass
class Task: ...

@dataclass
class User:
    # Fields
    avatarURL: str
    createdAt: datetime
    deletedAt: datetime
    email: str
    id: str
    isAdmin: bool
    isDeletionLocked: bool
    isLocked: bool
    isRoleLocked: bool
    isUsernameLocked: bool
    language: str
    name: str
    organization: str
    phone: str
    subscribeToOwnCards: bool
    updatedAt: datetime
    username: str