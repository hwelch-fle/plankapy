from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self, Any, Mapping
from contextlib import contextmanager

from .routes import Routes
from .constants import ActionType, BoardRole, Background, BackgroundImage

# Sentinel value for unset values since None is a valid value for responses
class _Unset: 
    def __repr__(self) -> str:
        return "<Unset>"
    
Unset = _Unset()
Required = _Unset()

class Model(Mapping):
    """Implements common magic methods for all Models"""

    @property
    def routes(self) -> Routes:
        return self._routes
    
    @routes.setter
    def routes(self, routes: Routes):
        self._routes = routes

    @property
    def unique_name(self) -> str:
        """Generate a unique name for the model instance using the last 5 characters of the id
        and the name attribute
        
        Returns:
            str: The unique name for the model instance in the format {name}_{id[:-3]}
        """
        if hasattr(self, 'id') and hasattr(self, 'name'):
            return f"{self.name}_{chr(123)}{self.id[-5:]}{chr(125)}"
        
        # Default unique name if no id or name (model name and last 5 characters of hash)
        return f"{self.__class__.__name__}_{str(hash(self))[-5:]}"

    def bind(self, routes: Routes) -> Self:
        """Bind routes to the model
        Args:
            routes (Routes): The routes to bind to the model instance
        
        Returns:
            Self for chain operations
        """
        self.routes = routes
        return self

    def __getitem__(self, key) -> Any:
        val = self.__dict__[key]
        return val if val is not Unset else None
    
    def __iter__(self):
        return iter(
            k for k, v in self.__dict__.items() 
            if v is not Unset 
            and not k.startswith("_") # 
        )
    
    def __len__(self) -> int:
        return len([i for i in self])
    
    def __hash__(self) -> int:
        if hasattr(self, 'id'):
            return int(self.id)
        
        # Default hash if no id (string of name and attributes)
        return hash(f"{self.__class__.__name__}{self.__dict__}")
    
    def update(self): ...

    @contextmanager
    def editor(self):
        """Context manager for editing the model

        Example:
        ```python
        with model.editor() as m:
            m.name = "New Name"
            m.position = 1
        ```
        """
        try:
            yield
        finally:
            self.update()

    def refresh(self): ...

@dataclass(eq=False)
class _Action(Model):
    id: Optional[int]=Unset
    type: Optional[ActionType]=Required
    data: Optional[dict]=Required
    cardId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _Archive(Model):
    fromModel: Optional[str]=Required
    originalRecordId: Optional[int]=Required
    originalRecord: Optional[dict]=Required

@dataclass(eq=False)
class _Attachment(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    dirname: Optional[str]=Required
    filename: Optional[str]=Required
    image: Optional[dict]=Unset
    url: Optional[str]=Unset
    coverUrl: Optional[str]=Unset
    creatorUserId: Optional[int]=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _Board(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    projectId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _BoardMembership(Model):
    id: Optional[int]=Unset
    role: Optional[BoardRole]=Required
    canComment: Optional[bool]=Unset
    boardId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _Card(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    description: Optional[str]=Unset
    dueDate: Optional[datetime]=Unset
    isDueDateCompleted: Optional[bool]=Unset
    stopwatch: Optional[_Stopwatch]=Unset
    boardId: Optional[int]=Required
    listId: Optional[int]=Required
    creatorUserId: Optional[int]=Unset
    coverAttachmentId: Optional[int]=Unset
    isSubscribed: Optional[bool]=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _Stopwatch:
    startedAt: Optional[datetime]=Unset
    total: Optional[int]=Unset

@dataclass(eq=False)
class _CardLabel(Model):
    id: Optional[int]=Unset
    cardId: Optional[int]=Required
    labelId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _CardMembership(Model):
    id: Optional[int]=Unset
    cardId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _CardSubscription(Model):
    id: Optional[int]=Unset
    cardId: Optional[int]=Required
    userId: Optional[int]=Required
    isPermanent: Optional[bool]=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _IdentityProviderUser(Model):
    id: Optional[int]=Unset
    issuer: Optional[str]=Unset
    sub: Optional[str]=Unset
    userId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _Label(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    color: Optional[str]=Required
    boardId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _List(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    boardId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _Notification(Model): 
    id: Optional[int]=Unset
    isRead: bool=Required
    userId: Optional[int]=Required
    actionId: Optional[int]=Required
    cardId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _Project(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    # Background overrides backgroundImage
    background: Optional[Background]=Unset
    backgroundImage: Optional[BackgroundImage]=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset
    
@dataclass(eq=False)
class _ProjectManager(Model):
    id: Optional[int]=Unset
    projectId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _Task(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    isCompleted: bool=Unset
    cardId: Optional[int]=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset

@dataclass(eq=False)
class _User(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    username: Optional[str]=Unset
    email: Optional[str]=Required
    language: Optional[str]=Unset
    organization: Optional[str]=Unset
    phone: Optional[str]=Unset
    avatarUrl: Optional[str]=Unset
    isAdmin: bool=Unset
    isDeletionLocked: bool=Unset
    isLocked: bool=Unset
    isRoleLocked: bool=Unset
    isUsernameLocked: bool=Unset
    subscribeToOwnCards: bool=Unset
    createdAt: Optional[datetime]=Unset
    updatedAt: Optional[datetime]=Unset
    deletedAt: Optional[datetime]=Unset