from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self

from constants import ActionType, Background, BackgroundImage

# Sentinal value for unset values since None is a valid value for responses
class _Unset: 
    def __repr__(self) -> str:
        return f"<Unset>"
    
Unset = _Unset()
Required = _Unset()

# Base class for all models
class Model:
    """Implements common magic methods for all Models"""
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create a new instance of the class from a dictionary"""
        if not set(data.keys()).issubset(cls.__annotations__):
            raise ValueError(f"Invalid attributes for {cls.__name__}: {list(data.keys() - cls.__annotations__.keys())}")
        return cls(**data)
    
    def __str__(self) -> str:
        if hasattr(self, 'name'):
            return self.name
        elif hasattr(self, 'id'):
            return self.id
        return f"<{self.__class__.__name__}>"
    
    def __iter__(self):
        return iter(self.__dict__.items())
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value
        
    def __len__(self):
        """Return the number of set values"""
        return len([v for v in self.__dict__.values() if v is not Unset])
    
    def validate(self) -> bool:
        """Check if all required fields are set
        Raises:
            ValueError: If a required field or fields notset
        """
        required = []
        for key, value in self.__dict__.items():
            if value is Required:
                required.append(key)
        if required:
            raise ValueError(f"Required field(s) {required} not set")
        return True

@dataclass
class Action(Model):
    id: Optional[str]|_Unset=Unset
    type: Optional[ActionType]|_Unset=Required
    data: Optional[dict]|_Unset=Required
    cardId: Optional[str]|_Unset=Required
    userId: Optional[str]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class Archive(Model):
    fromModel: Optional[str]|_Unset=Required
    originalRecordId: Optional[str]|_Unset=Required
    originalRecord: Optional[dict]|_Unset=Required

@dataclass
class Attachment(Model):
    id: Optional[str]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    dirname: Optional[str]|_Unset=Required
    filename: Optional[str]|_Unset=Required
    image: Optional[dict]|_Unset=Unset
    url: Optional[str]|_Unset=Unset
    coverUrl: Optional[str]|_Unset=Unset
    creatorUserId: Optional[str]|_Unset=Unset
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class Board(Model):
    id: Optional[str]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    position: Optional[int]|_Unset=Required
    projectId: Optional[str]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

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
    id: Optional[str]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    position: Optional[int]|_Unset=Required
    color: Optional[str]|_Unset=Required
    boardId: Optional[str]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class List(Model):
    id: Optional[str]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    position: Optional[int]|_Unset=Required
    boardId: Optional[str]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class Notification(Model): 
    id: Optional[str]|_Unset=Unset
    isRead: bool|_Unset=Required
    userID: Optional[str]|_Unset=Required
    actionID: Optional[str]|_Unset=Required
    cardID: Optional[str]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class Project(Model):
    id: Optional[str]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    # Background overrides backgroundImage
    background: Optional[Background]|_Unset=Unset
    backgroundImage: Optional[BackgroundImage]|_Unset=Unset
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset
    
@dataclass
class ProjectManager(Model): ...

@dataclass
class Task(Model):
    id: Optional[str]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    position: Optional[int]|_Unset=Required
    isCompleted: bool|_Unset=Unset
    cardId: Optional[str]|_Unset=Unset
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class User(Model):
    id: Optional[str]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    username: Optional[str]|_Unset=Unset
    email: Optional[str]|_Unset=Required
    language: Optional[str]|_Unset=Unset
    organization: Optional[str]|_Unset=Unset
    phone: Optional[str]|_Unset=Unset
    avatarURL: Optional[str]|_Unset=Unset
    isAdmin: bool|_Unset=Unset
    isDeletionLocked: bool|_Unset=Unset
    isLocked: bool|_Unset=Unset
    isRoleLocked: bool|_Unset=Unset
    isUsernameLocked: bool|_Unset=Unset
    subscribeToOwnCards: bool|_Unset=Unset
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset
    deletedAt: Optional[datetime]|_Unset=Unset