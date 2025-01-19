from dataclasses import dataclass
from datetime import datetime
try:
    from typing import Optional, Self, Any, Mapping
except ImportError:
    from typing import Optional
    Self = object

from .routes import Route
from .constants import ActionType, BoardRole, Background, BackgroundImage

__all__ = [
    'Action',
    'Archive',
    'Attachment',
    'Board',
    'BoardMembership',
    'Card',
    'Stopwatch',
    'CardLabel',
    'CardMembership',
    'CardSubscription',
    'IdentityProviderUser',
    'Label',
    'List',
    'Notification',
    'Project',
    'ProjectManager',
    'Task',
    'User',
]

# Sentinal value for unset values since None is a valid value for responses
class _Unset: 
    def __repr__(self) -> str:
        return f"<Unset>"
    
Unset = _Unset()
Required = _Unset()

# Base class for all models
# TODO: Set up as a Mapping so models can be ** unpacked into POST, PUT, and PATCH routes
class Model(Mapping):
    """Implements common magic methods for all Models"""
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create a new instance of the class from a dictionary"""
        if not set(data.keys()).issubset(cls.__annotations__.keys()):
            raise ValueError(f"Invalid attributes for {cls.__name__}: {list(data.keys() - cls.__annotations__.keys())}")
        return cls(**data)
    
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
    
    def bind_route(self, route: Route):
        """Bind a route to the model
        Args:
            route (Route): The route to bind to the model instance
        """
        self.route = route

    def __getitem__(self, key) -> Any:
        val = self.__dict__[key]
        return val if val is not Unset else None
    
    def __iter__(self):
        return iter(k for k, v in self.__dict__.items() if v is not Unset)
    
    def __len__(self) -> int:
        return len(i for i in self)

@dataclass
class Action(Model):
    id: Optional[int]=Unset
    type: Optional[ActionType]=Required
    data: Optional[dict]=Required
    cardId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass
class Archive(Model):
    fromModel: Optional[str]=Required
    originalRecordId: Optional[int]=Required
    originalRecord: Optional[dict]=Required

@dataclass
class Attachment(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    dirname: Optional[str]=Required
    filename: Optional[str]=Required
    image: Optional[dict]=Unset
    url: Optional[str]=Unset
    coverUrl: Optional[str]=Unset
    creatorUserid: Optional[int]=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass
class Board(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    projectId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass
class BoardMembership(Model):
    id: Optional[int]=Unset
    role: Optional[BoardRole]=Required
    canComment: Optional[bool]=Unset
    boardId: Optional[int]=Required
    userId: Optional[int]=Required

@dataclass
class Card(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    description: Optional[str]=Unset
    dueDate: Optional[datetime]=Unset
    isDueDateCompleted: Optional[bool]=Unset
    stopwatch: Optional['Stopwatch']=Unset
    boardId: Optional[int]=Required
    listId: Optional[int]=Required
    creatorUserId: Optional[int]=Unset
    coverAttachmentId: Optional[int]=Unset
    isSubscribed: Optional[bool]=Unset

@dataclass
class Stopwatch:
    startedAt: Optional[datetime]=Unset
    total: Optional[int]=Unset

@dataclass
class CardLabel(Model):
    id: Optional[int]=Unset
    cardId: Optional[int]=Required
    labelId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass
class CardMembership(Model):
    id: Optional[int]=Unset
    cardId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass
class CardSubscription(Model):
    id: Optional[int]=Unset
    cardId: Optional[int]=Required
    userId: Optional[int]=Required
    isPermanent: Optional[bool]=Unset

@dataclass
class IdentityProviderUser(Model):
    id: Optional[int]=Unset
    issuer: Optional[str]=Unset
    sub: Optional[str]=Unset
    userId: Optional[int]=Required

@dataclass
class Label(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    color: Optional[str]=Required
    boardId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass
class List(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    boardId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass
class Notification(Model): 
    id: Optional[int]=Unset
    isRead: bool=Required
    userId: Optional[int]=Required
    actionId: Optional[int]=Required
    cardId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass
class Project(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    # Background overrides backgroundImage
    background: Optional[Background]=Unset
    backgroundImage: Optional[BackgroundImage]=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset
    
@dataclass
class ProjectManager(Model):
    id: Optional[int]=Unset
    projectId: Optional[int]=Required
    userId: Optional[int]=Required

@dataclass
class Task(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    isCompleted: bool=Unset
    cardId: Optional[int]=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass
class User(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    username: Optional[str]=Unset
    email: Optional[str]=Required
    language: Optional[str]=Unset
    organization: Optional[str]=Unset
    phone: Optional[str]=Unset
    avatarURL: Optional[str]=Unset
    isAdmin: bool=Unset
    isDeletionLocked: bool=Unset
    isLocked: bool=Unset
    isRoleLocked: bool=Unset
    isUsernameLocked: bool=Unset
    subscribeToOwnCards: bool=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset
    deletedAt: Optional[datetime]=Unset