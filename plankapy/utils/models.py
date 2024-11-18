from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self

from .constants import ActionType, BoardRole, Background, BackgroundImage

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
    id: Optional[int]|_Unset=Unset
    type: Optional[ActionType]|_Unset=Required
    data: Optional[dict]|_Unset=Required
    cardid: Optional[int]|_Unset=Required
    userid: Optional[int]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class Archive(Model):
    fromModel: Optional[str]|_Unset=Required
    originalRecordid: Optional[int]|_Unset=Required
    originalRecord: Optional[dict]|_Unset=Required

@dataclass
class Attachment(Model):
    id: Optional[int]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    dirname: Optional[str]|_Unset=Required
    filename: Optional[str]|_Unset=Required
    image: Optional[dict]|_Unset=Unset
    url: Optional[str]|_Unset=Unset
    coverUrl: Optional[str]|_Unset=Unset
    creatorUserid: Optional[int]|_Unset=Unset
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class Board(Model):
    id: Optional[int]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    position: Optional[int]|_Unset=Required
    projectid: Optional[int]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class BoardMembership(Model):
    id: Optional[int]|_Unset=Unset
    role: Optional[BoardRole]|_Unset=Required
    canComment: Optional[bool]|_Unset=Unset
    boardid: Optional[int]|_Unset=Required
    userid: Optional[int]|_Unset=Required

@dataclass
class Card(Model):
    id: Optional[int]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    position: Optional[int]|_Unset=Required
    description: Optional[str]|_Unset=Unset
    dueDate: Optional[datetime]|_Unset=Unset
    isDueDateCompleted: Optional[bool]|_Unset=Unset
    stopwatch: Optional['Stopwatch']|_Unset=Unset
    boardid: Optional[int]|_Unset=Required
    listid: Optional[int]|_Unset=Required
    creatorUserid: Optional[int]|_Unset=Unset
    coverAttachmentid: Optional[int]|_Unset=Unset
    isSubscribed: Optional[bool]|_Unset=Unset

@dataclass
class Stopwatch:
    startedAt: Optional[datetime]|_Unset=Unset
    total: Optional[int]|_Unset=Unset

@dataclass
class CardLabel(Model):
    id: Optional[int]|_Unset=Unset
    cardid: Optional[int]|_Unset=Required
    labelid: Optional[int]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class CardMembership(Model):
    id: Optional[int]|_Unset=Unset
    cardid: Optional[int]|_Unset=Required
    userid: Optional[int]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class CardSubscription(Model):
    id: Optional[int]|_Unset=Unset
    cardid: Optional[int]|_Unset=Required
    userid: Optional[int]|_Unset=Required
    isPermanent: Optional[bool]|_Unset=Unset
@dataclass
class IdentityProviderUser(Model):
    id: Optional[int]|_Unset=Unset
    issuer: Optional[str]|_Unset=Unset
    sub: Optional[str]|_Unset=Unset
    userid: Optional[int]|_Unset=Required

@dataclass
class Label(Model):
    id: Optional[int]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    position: Optional[int]|_Unset=Required
    color: Optional[str]|_Unset=Required
    boardid: Optional[int]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class List(Model):
    id: Optional[int]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    position: Optional[int]|_Unset=Required
    boardid: Optional[int]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class Notification(Model): 
    id: Optional[int]|_Unset=Unset
    isRead: bool|_Unset=Required
    userid: Optional[int]|_Unset=Required
    actionid: Optional[int]|_Unset=Required
    cardid: Optional[int]|_Unset=Required
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class Project(Model):
    id: Optional[int]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    # Background overrides backgroundImage
    background: Optional[Background]|_Unset=Unset
    backgroundImage: Optional[BackgroundImage]|_Unset=Unset
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset
    
@dataclass
class ProjectManager(Model):
    id: Optional[int]|_Unset=Unset
    projectid: Optional[int]|_Unset=Required
    userid: Optional[int]|_Unset=Required

@dataclass
class Task(Model):
    id: Optional[int]|_Unset=Unset
    name: Optional[str]|_Unset=Required
    position: Optional[int]|_Unset=Required
    isCompleted: bool|_Unset=Unset
    cardid: Optional[int]|_Unset=Unset
    createdAt: Optional[datetime]|_Unset=Unset
    updatedAt: Optional[datetime]|_Unset=Unset

@dataclass
class User(Model):
    id: Optional[int]|_Unset=Unset
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