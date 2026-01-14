from __future__ import annotations
from typing import TypedDict, NotRequired, Any, Literal

__all__ = (
	"Action",
	"Attachment",
	"BackgroundImage",
	"BaseCustomFieldGroup",
	"Board",
	"BoardMembership",
	"Card",
	"CardLabel",
	"CardMembership",
	"Comment",
	"Config",
	"CustomField",
	"CustomFieldGroup",
	"CustomFieldValue",
	"Label",
	"List",
	"Notification",
	"NotificationService",
	"Project",
	"ProjectManager",
	"Task",
	"TaskList",
	"User",
	"Webhook",
)

class Action(TypedDict):
    id: str
    """Unique identifier for the action"""
    boardId: str
    """ID of the board where the action occurred"""
    cardId: str
    """ID of the card where the action occurred"""
    userId: str
    """ID of the user who performed the action"""
    type: Literal['createCard', 'moveCard', 'addMemberToCard', 'removeMemberFromCard', 'completeTask', 'uncompleteTask']
    """Type of the action"""
    data: dict[str, Any]
    """Action specific data (varies by type)"""
    createdAt: str
    """When the action was created"""
    updatedAt: str
    """When the action was last updated"""

class Attachment(TypedDict):
    id: str
    """Unique identifier for the attachment"""
    cardId: str
    """ID of the card the attachment belongs to"""
    creatorUserId: str
    """ID of the user who created the attachment"""
    type: Literal['file', 'link']
    """Type of the attachment"""
    data: dict[str, Any]
    """Attachment specific data (varies by type)"""
    name: str
    """Name/title of the attachment"""
    createdAt: str
    """When the attachment was created"""
    updatedAt: str
    """When the attachment was last updated"""

class BackgroundImage(TypedDict):
    id: str
    """Unique identifier for the background image"""
    projectId: str
    """ID of the project the background image belongs to"""
    size: str
    """File size of the background image in bytes"""
    url: str
    """URL to access the full-size background image"""
    thumbnailUrls: dict[str, Any]
    """URLs for different thumbnail sizes of the background image"""
    createdAt: str
    """When the background image was created"""
    updatedAt: str
    """When the background image was last updated"""

class BaseCustomFieldGroup(TypedDict):
    id: str
    """Unique identifier for the base custom field group"""
    projectId: str
    """ID of the project the base custom field group belongs to"""
    name: str
    """Name/title of the base custom field group"""
    createdAt: str
    """When the base custom field group was created"""
    updatedAt: str
    """When the base custom field group was last updated"""

class Board(TypedDict):
    id: str
    """Unique identifier for the board"""
    projectId: str
    """ID of the project the board belongs to"""
    position: int
    """Position of the board within the project"""
    name: str
    """Name/title of the board"""
    defaultView: Literal['kanban', 'grid', 'list']
    """Default view for the board"""
    defaultCardType: Literal['project', 'story']
    """Default card type for new cards"""
    limitCardTypesToDefaultOne: bool
    """Whether to limit card types to default one"""
    alwaysDisplayCardCreator: bool
    """Whether to always display the card creator"""
    expandTaskListsByDefault: bool
    """Whether to expand task lists by default"""
    createdAt: str
    """When the board was created"""
    updatedAt: str
    """When the board was last updated"""

class BoardMembership(TypedDict):
    id: str
    """Unique identifier for the board membership"""
    projectId: str
    """ID of the project the board membership belongs to (denormalized)"""
    boardId: str
    """ID of the board the membership is associated with"""
    userId: str
    """ID of the user who is a member of the board"""
    role: Literal['editor', 'viewer']
    """Role of the user in the board"""
    canComment: bool
    """Whether the user can comment on cards (applies only to viewers)"""
    createdAt: str
    """When the board membership was created"""
    updatedAt: str
    """When the board membership was last updated"""

class Card(TypedDict):
    id: str
    """Unique identifier for the card"""
    boardId: str
    """ID of the board the card belongs to (denormalized)"""
    listId: str
    """ID of the list the card belongs to"""
    creatorUserId: str
    """ID of the user who created the card"""
    prevListId: str
    """ID of the previous list the card was in (available when in archive or trash)"""
    coverAttachmentId: str
    """ID of the attachment used as cover"""
    type: Literal['project', 'story']
    """Type of the card"""
    position: int
    """Position of the card within the list"""
    name: str
    """Name/title of the card"""
    description: str
    """Detailed description of the card"""
    dueDate: str
    """Due date for the card"""
    isDueCompleted: bool
    """Whether the due date is completed"""
    stopwatch: dict[str, Any]
    """Stopwatch data for time tracking"""
    commentsTotal: int
    """Total number of comments on the card"""
    isClosed: bool
    """Whether the card is closed"""
    listChangedAt: str
    """When the card was last moved between lists"""
    createdAt: str
    """When the card was created"""
    updatedAt: str
    """When the card was last updated"""

class CardLabel(TypedDict):
    id: str
    """Unique identifier for the card-label association"""
    cardId: str
    """ID of the card the label is associated with"""
    labelId: str
    """ID of the label associated with the card"""
    createdAt: str
    """When the card-label association was created"""
    updatedAt: str
    """When the card-label association was last updated"""

class CardMembership(TypedDict):
    id: str
    """Unique identifier for the card membership"""
    cardId: str
    """ID of the card the user is a member of"""
    userId: str
    """ID of the user who is a member of the card"""
    createdAt: str
    """When the card membership was created"""
    updatedAt: str
    """When the card membership was last updated"""

class Comment(TypedDict):
    id: str
    """Unique identifier for the comment"""
    cardId: str
    """ID of the card the comment belongs to"""
    userId: str
    """ID of the user who created the comment"""
    text: str
    """Content of the comment"""
    createdAt: str
    """When the comment was created"""
    updatedAt: str
    """When the comment was last updated"""

class Config(TypedDict):
    version: str
    """Current version of the PLANKA application"""
    activeUsersLimit: NotRequired[int]
    """Maximum number of active users allowed (conditionally added for admins if configured)"""
    oidc: dict[str, Any]
    """OpenID Connect configuration (null if not configured)"""

class CustomField(TypedDict):
    id: str
    """Unique identifier for the custom field"""
    baseCustomFieldGroupId: str
    """ID of the base custom field group the custom field belongs to"""
    customFieldGroupId: str
    """ID of the custom field group the custom field belongs to"""
    position: int
    """Position of the custom field within the group"""
    name: str
    """Name/title of the custom field"""
    showOnFrontOfCard: bool
    """Whether to show the field on the front of cards"""
    createdAt: str
    """When the custom field was created"""
    updatedAt: str
    """When the custom field was last updated"""

class CustomFieldGroup(TypedDict):
    id: str
    """Unique identifier for the custom field group"""
    boardId: str
    """ID of the board the custom field group belongs to"""
    cardId: str
    """ID of the card the custom field group belongs to"""
    baseCustomFieldGroupId: str
    """ID of the base custom field group used as a template"""
    position: int
    """Position of the custom field group within the board/card"""
    name: str
    """Name/title of the custom field group"""
    createdAt: str
    """When the custom field group was created"""
    updatedAt: str
    """When the custom field group was last updated"""

class CustomFieldValue(TypedDict):
    id: str
    """Unique identifier for the custom field value"""
    cardId: str
    """ID of the card the value belongs to"""
    customFieldGroupId: str
    """ID of the custom field group the value belongs to"""
    customFieldId: str
    """ID of the custom field the value belongs to"""
    content: str
    """Content/value of the custom field"""
    createdAt: str
    """When the custom field value was created"""
    updatedAt: str
    """When the custom field value was last updated"""

class Label(TypedDict):
    id: str
    """Unique identifier for the label"""
    boardId: str
    """ID of the board the label belongs to"""
    position: int
    """Position of the label within the board"""
    name: str
    """Name/title of the label"""
    color: Literal['muddy-grey', 'autumn-leafs', 'morning-sky', 'antique-blue', 'egg-yellow', 'desert-sand', 'dark-granite', 'fresh-salad', 'lagoon-blue', 'midnight-blue', 'light-orange', 'pumpkin-orange', 'light-concrete', 'sunny-grass', 'navy-blue', 'lilac-eyes', 'apricot-red', 'orange-peel', 'silver-glint', 'bright-moss', 'deep-ocean', 'summer-sky', 'berry-red', 'light-cocoa', 'grey-stone', 'tank-green', 'coral-green', 'sugar-plum', 'pink-tulip', 'shady-rust', 'wet-rock', 'wet-moss', 'turquoise-sea', 'lavender-fields', 'piggy-red', 'light-mud', 'gun-metal', 'modern-green', 'french-coast', 'sweet-lilac', 'red-burgundy', 'pirate-gold']
    """Color of the label"""
    createdAt: str
    """When the label was created"""
    updatedAt: str
    """When the label was last updated"""

class List(TypedDict):
    id: str
    """Unique identifier for the list"""
    boardId: str
    """ID of the board the list belongs to"""
    type: Literal['active', 'closed', 'archive', 'trash']
    """Type/status of the list"""
    position: int
    """Position of the list within the board"""
    name: str
    """Name/title of the list"""
    color: Literal['berry-red', 'pumpkin-orange', 'lagoon-blue', 'pink-tulip', 'light-mud', 'orange-peel', 'bright-moss', 'antique-blue', 'dark-granite', 'turquoise-sea']
    """Color for the list"""
    createdAt: str
    """When the list was created"""
    updatedAt: str
    """When the list was last updated"""

class Notification(TypedDict):
    id: str
    """Unique identifier for the notification"""
    userId: str
    """ID of the user who receives the notification"""
    creatorUserId: str
    """ID of the user who created the notification"""
    boardId: str
    """ID of the board associated with the notification (denormalized)"""
    cardId: str
    """ID of the card associated with the notification"""
    commentId: str
    """ID of the comment associated with the notification"""
    actionId: str
    """ID of the action associated with the notification"""
    type: Literal['moveCard', 'commentCard', 'addMemberToCard', 'mentionInComment']
    """Type of the notification"""
    data: dict[str, Any]
    """Notification specific data (varies by type)"""
    isRead: bool
    """Whether the notification has been read"""
    createdAt: str
    """When the notification was created"""
    updatedAt: str
    """When the notification was last updated"""

class NotificationService(TypedDict):
    id: str
    """Unique identifier for the notification service"""
    userId: str
    """ID of the user the service is associated with"""
    boardId: str
    """ID of the board the service is associated with"""
    url: str
    """URL endpoint for notifications"""
    format: Literal['text', 'markdown', 'html']
    """Format for notification messages"""
    createdAt: str
    """When the notification service was created"""
    updatedAt: str
    """When the notification service was last updated"""

class Project(TypedDict):
    id: str
    """Unique identifier for the project"""
    ownerProjectManagerId: str
    """ID of the project manager who owns the project"""
    backgroundImageId: str
    """ID of the background image used as background"""
    name: str
    """Name/title of the project"""
    description: str
    """Detailed description of the project"""
    backgroundType: Literal['gradient', 'image']
    """Type of background for the project"""
    backgroundGradient: Literal['old-lime', 'ocean-dive', 'tzepesch-style', 'jungle-mesh', 'strawberry-dust', 'purple-rose', 'sun-scream', 'warm-rust', 'sky-change', 'green-eyes', 'blue-xchange', 'blood-orange', 'sour-peel', 'green-ninja', 'algae-green', 'coral-reef', 'steel-grey', 'heat-waves', 'velvet-lounge', 'purple-rain', 'blue-steel', 'blueish-curve', 'prism-light', 'green-mist', 'red-curtain']
    """Gradient background for the project"""
    isHidden: bool
    """Whether the project is hidden"""
    createdAt: str
    """When the project was created"""
    updatedAt: str
    """When the project was last updated"""

class ProjectManager(TypedDict):
    id: str
    """Unique identifier for the project manager"""
    projectId: str
    """ID of the project the manager is associated with"""
    userId: str
    """ID of the user who is assigned as project manager"""
    createdAt: str
    """When the project manager was created"""
    updatedAt: str
    """When the project manager was last updated"""

class Task(TypedDict):
    id: str
    """Unique identifier for the task"""
    taskListId: str
    """ID of the task list the task belongs to"""
    linkedCardId: str
    """ID of the card linked to the task"""
    assigneeUserId: str
    """ID of the user assigned to the task"""
    position: int
    """Position of the task within the task list"""
    name: str
    """Name/title of the task"""
    isCompleted: bool
    """Whether the task is completed"""
    createdAt: str
    """When the task was created"""
    updatedAt: str
    """When the task was last updated"""

class TaskList(TypedDict):
    id: str
    """Unique identifier for the task list"""
    cardId: str
    """ID of the card the task list belongs to"""
    position: int
    """Position of the task list within the card"""
    name: str
    """Name/title of the task list"""
    showOnFrontOfCard: bool
    """Whether to show the task list on the front of the card"""
    hideCompletedTasks: bool
    """Whether to hide completed tasks"""
    createdAt: str
    """When the task list was created"""
    updatedAt: str
    """When the task list was last updated"""

class User(TypedDict):
    id: str
    """Unique identifier for the user"""
    email: NotRequired[str]
    """Email address for login and notifications (private field)"""
    role: Literal['admin', 'projectOwner', 'boardUser']
    """User role defining access permissions"""
    name: str
    """Full display name of the user"""
    username: str
    """Unique username for user identification"""
    avatar: dict[str, Any]
    """Avatar information for the user with generated URLs"""
    gravatarUrl: NotRequired[str]
    """Gravatar URL for the user (conditionally added if configured)"""
    phone: str
    """Contact phone number"""
    organization: str
    """Organization or company name"""
    language: NotRequired[Literal['ar-YE', 'bg-BG', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US', 'es-ES', 'et-EE', 'fa-IR', 'fi-FI', 'fr-FR', 'hu-HU', 'id-ID', 'it-IT', 'ja-JP', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'sk-SK', 'sr-Cyrl-RS', 'sr-Latn-RS', 'sv-SE', 'tr-TR', 'uk-UA', 'uz-UZ', 'zh-CN', 'zh-TW']]
    """Preferred language for user interface and notifications (personal field)"""
    subscribeToOwnCards: NotRequired[bool]
    """Whether the user subscribes to their own cards (personal field)"""
    subscribeToCardWhenCommenting: NotRequired[bool]
    """Whether the user subscribes to cards when commenting (personal field)"""
    turnOffRecentCardHighlighting: NotRequired[bool]
    """Whether recent card highlighting is disabled (personal field)"""
    enableFavoritesByDefault: NotRequired[bool]
    """Whether favorites are enabled by default (personal field)"""
    defaultEditorMode: NotRequired[Literal['wysiwyg', 'markup']]
    """Default markdown editor mode (personal field)"""
    defaultHomeView: NotRequired[Literal['gridProjects', 'groupedProjects']]
    """Default view mode for the home page (personal field)"""
    defaultProjectsOrder: NotRequired[Literal['byDefault', 'alphabetically', 'byCreationTime']]
    """Default sort order for projects display (personal field)"""
    termsType: str
    """Type of terms applicable to the user based on role"""
    isSsoUser: NotRequired[bool]
    """Whether the user is SSO user (private field)"""
    isDeactivated: bool
    """Whether the user account is deactivated and cannot log in"""
    isDefaultAdmin: NotRequired[bool]
    """Whether the user is the default admin (visible only to current user or admin)"""
    lockedFieldNames: NotRequired[list[Literal['email', 'password', 'name']]]
    """List of fields locked from editing (visible only to current user or admin)"""
    createdAt: str
    """When the user was created"""
    updatedAt: str
    """When the user was last updated"""

class Webhook(TypedDict):
    id: str
    """Unique identifier for the webhook"""
    name: str
    """Name/title of the webhook"""
    url: str
    """URL endpoint for the webhook"""
    accessToken: str
    """Access token for webhook authentication"""
    events: list[Literal['cardCreate', 'cardUpdate', 'cardDelete']]
    """List of events that trigger the webhook"""
    excludedEvents: list[Literal['userCreate', 'userUpdate', 'userDelete']]
    """List of events excluded from the webhook"""
    createdAt: str
    """When the webhook was created"""
    updatedAt: str
    """When the webhook was last updated"""