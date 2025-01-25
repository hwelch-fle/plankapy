"""Pythonic wrapper for Plankanban API"""

# TODO: Audit codebase and try to remove superfluous new feature imports
# To allow for plankapy to run on python<=3.11, ideally target >=3.8 (?)

# TODO: Package into a docker container and deploy on release to GHCR
# This will allow installation of a valid Plankapy container alongside
# A planka container meaning all requests will be running on loopback/localhost

# TODO: See if plankapy could be shipped in the official Planka container


__version__ = "2.0.1"

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
)

from .handlers import (
    BaseAuth,
    PasswordAuth,
    TokenAuth,
)

from .constants import (
    LabelColor,
    Gradient,
    ListSorts,
    SortOption,
    Background,
    BackgroundImage,
    BoardRole,
    OFFSET,
)