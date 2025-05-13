"""Pythonic wrapper for Plankanban API"""

__version__ = "2.2.2"

# flake8: noqa 
# imports elevate these objects to the root module

from .interfaces import (
    Planka,
    Project,
    User,
    Notification,
    Board,
    Label,
    Action,
    Archive,
    Attachment,
    Card,
    CardLabel,
    CardMembership,
    CardSubscription,
    IdentityUserProvider,
    List,
    ProjectManager,
    Task,
    QueryableList,
)

from .handlers import (
    BaseAuth,
    PasswordAuth,
    TokenAuth,
    HTTPOnlyAuth,
)

from .constants import (
    LabelColor,
    Gradient,
    ListSorts,
    SortOption,
    Background,
    BackgroundImage,
    BoardRole,
)

# Allow access to submodules
from . import helpers, constants, handlers, interfaces, models, routes
