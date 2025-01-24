from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self, Any, Mapping, Generator
from contextlib import contextmanager

from .routes import Routes
from .constants import ActionType, BoardRole, Background, BackgroundImage

# Sentinel value for unset values since None is a valid value for responses
class _Unset: 
    """Sentinel value for unset values
    
    Note:
        Used to differentiate between None and unset values
        There are two instances of this class: `Unset` and `Required`
    """
    def __repr__(self) -> str:
        return "<Unset>"
    
Unset = _Unset()
Required = _Unset()

class Model(Mapping):
    """Implements common magic methods for all Models
    """

    @property
    def routes(self) -> Routes:
        """Get the routes for the model instance
        
        Returns:
            Routes: The routes bound to the model instance
        """
        return self._routes
    
    @routes.setter
    def routes(self, routes: Routes):
        """Set the routes for the model instance
        
        Args:
            routes (Routes): The routes to bind to the model instance
        """
        self._routes = routes

    @property
    def unique_name(self) -> str:
        """Generate a unique name for the model instance using the last 5 characters of the id
        and the name attribute
        
        Returns:
            str: The unique name for the model instance in the format {name}_{id[:-5]}
        """
        if hasattr(self, 'id') and hasattr(self, 'name'):
            return f"{self.name}_{chr(123)}{self.id[-5:]}{chr(125)}"
        
        # Default unique name if no id or name (model name and last 5 characters of hash)
        return f"{self.__class__.__name__}_{str(hash(self))[-5:]}"

    @property
    def created_at(self) -> Optional[datetime]:
        """Get the creation date of the model instance
        
        Returns:
            Optional[datetime]: The creation date of the model instance
        """
        if hasattr(self, 'createdAt'):
            return datetime.fromisoformat(self.createdAt)
    
    @property
    def updated_at(self) -> Optional[datetime]:
        """Get the last update date of the model instance
        
        Returns:
            Optional[datetime]: The last update date of the model instance
        """
        if hasattr(self, 'updatedAt'):
            return datetime.fromisoformat(self.updatedAt)

    def bind(self, routes: Routes) -> Self:
        """Bind routes to the model
        Args:
            routes (Routes): The routes to bind to the model instance
        
        Returns:
            Self for chain operations

        Example:
            ```python
            model = Model(**kwargs).bind(routes)
            ```
        """
        self.routes = routes
        return self

    def __getitem__(self, key) -> Any:
        """Get the value of an attribute
        
        Warning:
            This is an implementation detail that allows for the unpacking operations
            in the rest of the codebase, all model attributes are still directly accessible
            through `__getattribute___`

        Note:
            Returns None if the attribute is `Unset` or starts with an underscore

        Example:
            ```python
            print(model['name'])
            >>> "Model Name"

            model.name = Unset
            print(model['name'])
            >>> None
            ```
        """
        val = self.__dict__[key]
        return val if val is not Unset else None
    
    def __iter__(self):
        """Iterate over public, assigned model attribute names

        Warning:
            This is used in conjunction with `__getitem__` to unpack assigned values. 
            This allows model state to be passed as keyword arguments to functions

            Example:
                ```python
                model = Model(name="Model Name", position=1, other=Unset)

                def func(name=None, position=None):
                    return {"name": name, "position": position}
                
                print(func(**model))
                >>> {'name': 'Model Name', 'position': 1}
                ```
            Notice how only the assigned values are returned after unpacking and any Unset or 
            private attributes are skipped, This allows `None` values to be assigned during
            a `PATCH` request to delete data 

        Note:
            Skips attributes that are `Unset` or start with an underscore

        Returns:
            Iterator: The iterator of the model attributes
        
        Example:
            ```python

            # Skip Private attributes
            print(list(model.__dict__))
            >>> ['_privateattribute', 'name', 'position', 'id']

            print(list(model))
            >>> ['name', 'position', 'id'] # Skips _privateattribute

            # Skip Unset attributes
            print(model.___dict___)
            >>> {'_privateattribute': 'Private', 'name': 'Model Name', 'position': Unset, 'id': 1}
            
            items = dict(model.items())
            print(items)
            >>> {'name': 'Model Name', 'id': 1} # Skips position because it's Unset
            ```
        """
        return iter(
            k for k, v in self.__dict__.items() 
            if v is not Unset 
            and not k.startswith("_")
        )
    
    def __len__(self) -> int:
        return len([i for i in self])
    
    def __hash__(self) -> int:
        """Generate a hash for the model instance so it can be used in mappings (`dict`, `set`)
        
        Note:
            All Models are still mutable, but their ID value is unique
            
        Returns:
            int: The hash value of the model instance
        
        Example:
            ```python
            board_map = {
                Board(name="Board 1"): board.,
                Board(name="Board 2"): "Board 2"
            }
            >>> 1
            ```
        """
        if hasattr(self, 'id'):
            return int(self.id)
        
        # Default hash if no id (string of name and attributes)
        return hash(f"{self.__class__.__name__}{self.__dict__}")

    def __eq__(self, other: Model) -> bool:
        """Check if two model instances are equal
        
        Note:
            Compares the hash and class of the model instances
        
        Warning:
            Does not compare the attributes of the model instances, out of sync models
            with different attributes can still be equal, it's best to refresh the models
            before comparing.
        
        Args:
            other (Model): The other model instance to compare
        
        Returns:
            bool: True if the model instances are equal, False otherwise
        """
        return isinstance(other, self.__class__) and hash(self) == hash(other)
    
    def update(self): 
        """Update the model instance
        Note:
            Method is implemented in the child classes, but is not required
        """
        ...

    def refresh(self): 
        """"Refresh the model instance
        Note:
            Method is implemented in the child classes, but is not required
        """
        ...

    def delete(self): 
        """Delete the model instance
        Note:
            Method is implemented in the child classes, but is not required
        """
        ...

    @contextmanager
    def editor(self) -> Generator[Self, None, None]:
        """Context manager for editing the model

        Example:
            ```python
            print(model.name)
            >>> "Old Name"
            with model.editor() as m:
                m.name = "New Name"
                m.position = 1
            
            print(model.name)
            >>> "New Name"
            ```

        """
        try:
            yield self
        finally:
            self.update()


@dataclass(eq=False)
class Action_(Model):
    """Action Model
    
    Attributes:
        id (int): The ID of the action
        type (ActionType): The type of the action
        data (dict): The data of the action
        cardId (int): The ID of the card the action is associated with
        userId (int): The ID of the user who created the action
        createdAt (datetime): The creation date of the action
        updatedAt (datetime): The last update date of the action
    """

    id: Optional[int]=Unset
    type: Optional[ActionType]=Required
    data: Optional[dict]=Required
    cardId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class Archive_(Model):
    """Archive Model
    
    Warning:
        This model is currently unavailable in the Planka API

    Attributes:
        fromModel (str): The model the archive is from
        originalRecordId (int): The ID of the original record
        originalRecord (dict): The original record
    """

    fromModel: Optional[str]=Required
    originalRecordId: Optional[int]=Required
    originalRecord: Optional[dict]=Required

@dataclass(eq=False)
class Attachment_(Model):
    """Attachment Model
    
    Attributes:
        id (int): The ID of the attachment
        name (str): The name of the attachment
        url (str): The URL of the attachment
        cardId (int): The ID of the card the attachment is associated with
        dirname (str): The directory name of the attachment
        filename (str): The filename of the attachment
        image (dict): The image of the attachment
        url (str): The URL of the attachment
        coverUrl (str): The cover URL of the attachment
        creatorUserId (int): The ID of the user who created the attachment
        createdAt (datetime): The creation date of the attachment
        updatedAt (datetime): The last update date of the attachment
        """
    id: Optional[int]=Unset
    name: Optional[str]=Required
    dirname: Optional[str]=Required
    filename: Optional[str]=Required
    image: Optional[dict]=Unset
    url: Optional[str]=Unset
    coverUrl: Optional[str]=Unset
    creatorUserId: Optional[int]=Unset
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class Board_(Model):
    """Board Model

    Attributes:
        id (int): The ID of the board
        name (str): The name of the board
        description (str): The description of the board
        isClosed (bool): The closed status of the board
        isStarred (bool): The starred status of the board
        createdAt (datetime): The creation date of the board
        updatedAt (datetime): The last update date of the board
    """
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    projectId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class BoardMembership_(Model):
    """Board Membership Model

    Attributes:
        id (int): The ID of the board membership
        role (BoardRole): The role of the board membership
        canComment (bool): The comment permission of the board membership
        boardId (int): The ID of the board the membership is associated with
        userId (int): The ID of the user the membership is associated with
        createdAt (datetime): The creation date of the board membership
        updatedAt (datetime): The last update date of the board membership
    """
    id: Optional[int]=Unset
    role: Optional[BoardRole]=Required
    canComment: Optional[bool]=Unset
    boardId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class Card_(Model):
    """Card Model
    
    Attributes:
        id (int): The ID of the card
        name (str): The name of the card
        position (int): The position of the card
        description (str): The description of the card
        dueDate (datetime): The due date of the card
        isDueDateCompleted (bool): The due date completion status of the card
        stopwatch (_Stopwatch): The stopwatch associated with the card
        boardId (int): The ID of the board the card is associated with
        listId (int): The ID of the list the card is associated with
        creatorUserId (int): The ID of the user who created the card
        coverAttachmentId (int): The ID of the cover attachment of the card
        isSubscribed (bool): The current user's subscription status with the card
        createdAt (datetime): The creation date of the card
        updatedAt (datetime): The last update date of the card
    """
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    description: Optional[str]=Unset
    dueDate: Optional[str]=Unset
    isDueDateCompleted: Optional[bool]=Unset
    stopwatch: Optional[Stopwatch]=Unset
    boardId: Optional[int]=Required
    listId: Optional[int]=Required
    creatorUserId: Optional[int]=Unset
    coverAttachmentId: Optional[int]=Unset
    isSubscribed: Optional[bool]=Unset
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class Stopwatch(Model):
    """Stopwatch Model
    
    Note:
        The stopwatch model is not a regular interface and instead is dynamically generated on
        Access through the `Card` `.stopwatch` attribute. There is an override that intercepts
        `__getitem__` to return a `Stopwatch`. 
        
        All `Stopwatch` methods directly update the `.stopwatch` attribute of the linked `Card` 
        instance.

    Attributes:
        startedAt (datetime): The start date of the stopwatch
        total (int): The total time of the stopwatch (in seconds)
        _card (Card): The card the stopwatch is associated with (Managed by the `Card` class)
    """
    _card: Optional[Card_]=Unset
    startedAt: Optional[str]=Unset
    total: Optional[int]=Unset

    def refresh(self):
        self._card.refresh()
        self.startedAt = self._card.stopwatch.startedAt
        self.total = self._card.stopwatch.total
    
    def start_time(self) -> datetime:
        """Returns the datetime the stopwatch was started"""
        self.refresh()
        return datetime.fromisoformat(self.startedAt) if self.startedAt else None

    def start(self) -> None:
        """Starts the stopwatch"""
        self.refresh()
        if self.startedAt:
            return
        self.startedAt = datetime.now().isoformat()
        with self._card.editor():
            self._card.stopwatch = self
    
    def stop(self) -> None:
        """Stops the stopwatch"""
        self.refresh()
        if not self.startedAt:
            return
        
        now = datetime.now()
        started = datetime.fromisoformat(self.startedAt)
        self.total += int(now.timestamp() - started.timestamp())
        self.startedAt = None
        with self._card.editor():
            self._card.stopwatch = self
    
    def set(self, hours: int=0, minutes: int=0, seconds: int=0) -> None:
        """Set an amount of time for the stopwatch
        
        Args:
            hours (int): Hours to set
            minutes (int): Minutes to set
            seconds (int): Seconds to set
        """
        self.total = (hours * 3600) + (minutes * 60) + seconds
        with self._card.editor():
            self._card.stopwatch = self

    def delete(self):
        """Delete the stopwatch"""
        with self._card.editor():
            self._card.stopwatch = None

@dataclass(eq=False)
class CardLabel_(Model):
    """Card Label Model
    
    Attributes:
        id (int): The ID of the card label
        cardId (int): The ID of the card the label is associated with
        labelId (int): The ID of the label the card is associated with
        createdAt (datetime): The creation date of the card label
        updatedAt (datetime): The last update date of the card label
    """
    id: Optional[int]=Unset
    cardId: Optional[int]=Required
    labelId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class CardMembership_(Model):
    """Card Membership Model

    Attributes:
        id (int): The ID of the card membership
        cardId (int): The ID of the card the membership is associated with
        userId (int): The ID of the user the membership is associated with
        createdAt (datetime): The creation date of the card membership
        updatedAt (datetime): The last update date of the card membership
    """
    id: Optional[int]=Unset
    cardId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class CardSubscription_(Model):
    id: Optional[int]=Unset
    cardId: Optional[int]=Required
    userId: Optional[int]=Required
    isPermanent: Optional[bool]=Unset
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class IdentityProviderUser_(Model):
    id: Optional[int]=Unset
    issuer: Optional[str]=Unset
    sub: Optional[str]=Unset
    userId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class Label_(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    color: Optional[str]=Required
    boardId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class List_(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    boardId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class Notification_(Model): 
    id: Optional[int]=Unset
    isRead: bool=Required
    userId: Optional[int]=Required
    actionId: Optional[int]=Required
    cardId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class Project_(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    # Background overrides backgroundImage
    background: Optional[Background]=Unset
    backgroundImage: Optional[BackgroundImage]=Unset
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset
    
@dataclass(eq=False)
class ProjectManager_(Model):
    id: Optional[int]=Unset
    projectId: Optional[int]=Required
    userId: Optional[int]=Required
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class Task_(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    position: Optional[int]=Required
    isCompleted: bool=Unset
    cardId: Optional[int]=Unset
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset

@dataclass(eq=False)
class User_(Model):
    id: Optional[int]=Unset
    name: Optional[str]=Required
    username: Optional[str]=Unset
    email: Optional[str]=Required
    language: Optional[str]=Unset
    organization: Optional[str]=Unset
    phone: Optional[str]=Unset
    avatarUrl: Optional[str]=Unset
    isSso: Optional[bool]=Unset
    isAdmin: bool=Unset
    isDeletionLocked: bool=Unset
    isLocked: bool=Unset
    isRoleLocked: bool=Unset
    isUsernameLocked: bool=Unset
    subscribeToOwnCards: bool=Unset
    createdAt: Optional[str]=Unset
    updatedAt: Optional[str]=Unset
    deletedAt: Optional[str]=Unset