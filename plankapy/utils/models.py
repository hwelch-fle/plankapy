from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self

from constants import ActionType, Background, BackgroundImage

# Sentinal value for unset values since None is a valid value
# For responses
class _Unset: 
    def __repr__(self) -> str:
        return f"<Unset>"
    
Unset = _Unset()


# Base class for all models
class Model:
    """Implements common magic methods for all Models"""
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create a new instance of the class from a dictionary"""
        if not set(data.keys()).issubset(cls.__annotations__):
            raise ValueError(f"Invalid attributes for {cls.__name__}: {list(data.keys() - cls.__annotations__.keys())}")
        return cls(**data)
    
    def __iter__(self):
        return iter(self.__dict__.items())
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value
        
    def __len__(self):
        """Return the number of set values"""
        return len([v for v in self.__dict__.values() if v is not Unset])

@dataclass
class Action(Model):
    id: str|_Unset=Unset
    createdAt: datetime|_Unset=Unset
    updatedAt: datetime|_Unset=Unset
    type: ActionType|_Unset=Unset
    data: dict|_Unset=Unset
    cardId: str|_Unset=Unset
    userId: str|_Unset=Unset

@dataclass
class Archive(Model):
    fromModel: str|_Unset=Unset
    originalRecordId: str|_Unset=Unset
    originalRecord: dict|_Unset=Unset

@dataclass
class Attachment(Model): ...

@dataclass
class Board(Model):
    createdAt: datetime|_Unset=Unset
    id: str|_Unset=Unset
    name: str|_Unset=Unset
    position: int|_Unset=Unset
    projectId: str|_Unset=Unset
    updatedAt: datetime|_Unset=Unset

@dataclass
class BoardMembership(Model): ...

@dataclass
class Card(Model): ...

@dataclass
class CardLabel(Model): ...

@dataclass
class CardMembership(Model): ...

@dataclass
class CardSubscription(Model): ...

@dataclass
class IdentityProviderUser(Model): ...

@dataclass
class Label(Model):
    id: str|_Unset=Unset
    createdAt: datetime|_Unset=Unset
    updatedAt: datetime|_Unset=Unset
    position: int|_Unset=Unset
    name: str|_Unset=Unset
    color: str|_Unset=Unset
    boardId: str|_Unset=Unset

@dataclass
class List(Model):
    id: str|_Unset=Unset
    createdAt: datetime|_Unset=Unset
    updatedAt: datetime|_Unset=Unset
    position: int|_Unset=Unset
    name: str|_Unset=Unset
    boardId: str|_Unset=Unset

@dataclass
class Notification(Model): 
    id: str|_Unset=Unset
    createdAt: datetime|_Unset=Unset
    updatedAt: datetime|_Unset=Unset
    isRead: bool|_Unset=Unset
    userID: str|_Unset=Unset
    actionID: str|_Unset=Unset
    cardID: str|_Unset=Unset

@dataclass
class Project(Model):
    # Background overrides backgroundImage
    background: Background|_Unset=Unset
    backgroundImage: BackgroundImage|_Unset=Unset
    createdAt: datetime|_Unset=Unset
    id: str|_Unset=Unset
    name: str|_Unset=Unset
    updatedAt: datetime|_Unset=Unset

@dataclass
class ProjectManager(Model): ...

@dataclass
class Task(Model):
    id: str|_Unset=Unset
    createdAt: datetime|_Unset=Unset
    updatedAt: datetime|_Unset=Unset
    position: int|_Unset=Unset
    name: str|_Unset=Unset
    isCompleted: bool|_Unset=Unset
    cardId: str|_Unset=Unset

@dataclass
class User(Model):
    avatarURL: str|_Unset=Unset
    createdAt: datetime|_Unset=Unset
    deletedAt: datetime|_Unset=Unset
    email: str|_Unset=Unset
    id: str|_Unset=Unset
    isAdmin: bool|_Unset=Unset
    isDeletionLocked: bool|_Unset=Unset
    isLocked: bool|_Unset=Unset
    isRoleLocked: bool|_Unset=Unset
    isUsernameLocked: bool|_Unset=Unset
    language: str|_Unset=Unset
    name: str|_Unset=Unset
    organization: str|_Unset=Unset
    phone: str|_Unset=Unset
    subscribeToOwnCards: bool|_Unset=Unset
    updatedAt: datetime|_Unset=Unset
    username: str|_Unset=Unset