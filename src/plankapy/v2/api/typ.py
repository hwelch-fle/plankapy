from __future__ import annotations
from datetime import datetime
from typing import (
    Any,
    Literal,
    TypedDict,
    NotRequired,
)
from .schemas import *


# Request Typing
class Request_acceptTerms(TypedDict):
    pendingToken: str
    """Pending token received from the authentication flow"""
    signature: str
    """Terms signature hash based on user role"""

class Request_createAccessToken(TypedDict):
    emailOrUsername: str
    """Email address or username of the user"""
    password: str
    """Password of the user"""
    withHttpOnlyToken: NotRequired[bool]
    """Whether to include an HTTP-only authentication cookie"""

class Request_exchangeForAccessTokenWithOidc(TypedDict):
    code: str
    """Authorization code from OIDC provider"""
    nonce: str
    """Nonce value for OIDC security"""
    withHttpOnlyToken: NotRequired[bool]
    """Whether to include HTTP-only authentication cookie"""

class Request_revokePendingToken(TypedDict):
    pendingToken: str
    """Pending token to revoke"""

class Request_getBoardActions(TypedDict):
    beforeId: NotRequired[str]
    """ID to get actions before (for pagination)"""

class Request_getCardActions(TypedDict):
    beforeId: NotRequired[str]
    """ID to get actions before (for pagination)"""

class Request_createAttachment(TypedDict):
    type: Literal['file', 'link']
    """Type of the attachment"""
    file: NotRequired[str]
    """File to upload"""
    url: NotRequired[str]
    """URL for the link attachment"""
    name: str
    """Name/title of the attachment"""
    requestId: NotRequired[str]
    """Request ID for tracking"""

class Request_updateAttachment(TypedDict):
    name: NotRequired[str]
    """Name/title of the attachment"""

class Request_createBackgroundImage(TypedDict):
    file: str
    """Background image file (must be an image format)"""
    requestId: NotRequired[str]
    """Request ID for tracking"""

class Request_createBaseCustomFieldGroup(TypedDict):
    name: str
    """Name/title of the base custom field group"""

class Request_updateBaseCustomFieldGroup(TypedDict):
    name: NotRequired[str]
    """Name/title of the base custom field group"""

class Request_createBoardMembership(TypedDict):
    userId: str
    """ID of the user who is a member of the board"""
    role: Literal['editor', 'viewer']
    """Role of the user in the board"""
    canComment: NotRequired[bool | None]
    """Whether the user can comment on cards (applies only to viewers)"""

class Request_updateBoardMembership(TypedDict):
    role: NotRequired[Literal['editor', 'viewer']]
    """Role of the user in the board"""
    canComment: NotRequired[bool | None]
    """Whether the user can comment on cards (applies only to viewers)"""

class Request_createBoard(TypedDict):
    position: int
    """Position of the board within the project"""
    name: str
    """Name/title of the board"""
    importType: NotRequired[Literal['trello']]
    """Type of import"""
    importFile: NotRequired[str]
    """Import file"""
    requestId: NotRequired[str]
    """Request ID for tracking"""

class Request_getBoard(TypedDict):
    subscribe: NotRequired[bool]
    """Whether to subscribe to real-time updates for this board (only for socket connections)"""

class Request_updateBoard(TypedDict):
    position: NotRequired[int]
    """Position of the board within the project"""
    name: NotRequired[str]
    """Name/title of the board"""
    defaultView: NotRequired[Literal['kanban', 'grid', 'list']]
    """Default view for the board"""
    defaultCardType: NotRequired[Literal['project', 'story']]
    """Default card type for new cards"""
    limitCardTypesToDefaultOne: NotRequired[bool]
    """Whether to limit card types to default one"""
    alwaysDisplayCardCreator: NotRequired[bool]
    """Whether to always display card creators"""
    expandTaskListsByDefault: NotRequired[bool]
    """Whether to expand task lists by default"""
    isSubscribed: NotRequired[bool]
    """Whether the current user is subscribed to the board"""

class Request_createCardLabel(TypedDict):
    labelId: str
    """ID of the label to add to the card"""

class Request_createCardMembership(TypedDict):
    userId: str
    """ID of the card to add the user to"""

class Request_createCard(TypedDict):
    type: Literal['project', 'story']
    """Type of the card"""
    position: NotRequired[int | None]
    """Position of the card within the list"""
    name: str
    """Name/title of the card"""
    description: NotRequired[str | None]
    """Detailed description of the card"""
    dueDate: NotRequired[str | datetime]
    """Due date for the card (`datetime` only allowed when using `Card.create_card`, otherwise use ISO string)"""
    isDueCompleted: NotRequired[bool]
    """Whether the due date is completed"""
    stopwatch: NotRequired[dict[str, Any] | None]
    """Stopwatch data for time tracking"""

class Request_getCards(TypedDict):
    before: NotRequired[str]
    """Pagination cursor (JSON object with id and listChangedAt)"""
    search: NotRequired[str]
    """Search term to filter cards"""
    filterUserIds: NotRequired[str]
    """Comma-separated user IDs to filter by members"""
    filterLabelIds: NotRequired[str]
    """Comma-separated label IDs to filter by labels"""

class Request_updateCard(TypedDict):
    boardId: NotRequired[str]
    """ID of the board to move the card to"""
    listId: NotRequired[str]
    """ID of the list to move the card to"""
    coverAttachmentId: NotRequired[str | None]
    """ID of the attachment used as cover"""
    type: NotRequired[Literal['project', 'story']]
    """Type of the card"""
    position: NotRequired[int | None]
    """Position of the card within the list"""
    name: NotRequired[str]
    """Name/title of the card"""
    description: NotRequired[str | None]
    """Detailed description of the card"""
    dueDate: NotRequired[str | None]
    """Due date for the card"""
    isDueCompleted: NotRequired[bool | None]
    """Whether the due date is completed"""
    stopwatch: NotRequired[Stopwatch | None]
    """Stopwatch data for time tracking"""
    isSubscribed: NotRequired[bool]
    """Whether the current user is subscribed to the card"""

class Request_duplicateCard(TypedDict):
    position: int
    """Position for the duplicated card within the list"""
    name: str
    """Name/title for the duplicated card"""

class Request_createComment(TypedDict):
    text: str
    """Content of the comment"""

class Request_getComments(TypedDict):
    beforeId: NotRequired[str]
    """ID to get comments before (for pagination)"""

class Request_updateComments(TypedDict):
    text: NotRequired[str]
    """Content of the comment"""

class Request_createBoardCustomFieldGroup(TypedDict):
    baseCustomFieldGroupId: NotRequired[str]
    """ID of the base custom field group used as a template"""
    position: int
    """Position of the custom field group within the board"""
    name: NotRequired[str | None]
    """Name/title of the custom field group (required if `baseCustomFieldGroupId` is not provided)"""

class Request_createCardCustomFieldGroup(TypedDict):
    baseCustomFieldGroupId: NotRequired[str]
    """ID of the base custom field group used as a template"""
    position: int
    """Position of the custom field group within the card"""
    name: NotRequired[str | None]
    """Name/title of the custom field group (required if `baseCustomFieldGroupId` is not provided)"""

class Request_updateCustomFieldGroup(TypedDict):
    position: NotRequired[int]
    """Position of the custom field group within the board/card"""
    name: NotRequired[str | None]
    """Name/title of the custom field group"""

class Request_updateCustomFieldValue(TypedDict):
    content: str
    """Content/value of the custom field"""

class Request_createCustomFieldInBaseGroup(TypedDict):
    position: int
    """Position of the custom field within the group"""
    name: str
    """Name/title of the custom field"""
    showOnFrontOfCard: NotRequired[bool]
    """Whether to show the field on the front of cards"""

class Request_createCustomFieldInGroup(TypedDict):
    position: int
    """Position of the custom field within the group"""
    name: str
    """Name/title of the custom field"""
    showOnFrontOfCard: NotRequired[bool]
    """Whether to show the field on the front of cards"""

class Request_updateCustomField(TypedDict):
    position: NotRequired[int]
    """Position of the custom field within the group"""
    name: NotRequired[str]
    """Name/title of the custom field"""
    showOnFrontOfCard: NotRequired[bool]
    """Whether to show the field on the front of cards"""

class Request_createLabel(TypedDict):
    position: int
    """Position of the label within the board"""
    name: NotRequired[str | None]
    """Name/title of the label"""
    color: Literal['muddy-grey', 'autumn-leafs', 'morning-sky', 'antique-blue', 'egg-yellow', 'desert-sand', 'dark-granite', 'fresh-salad', 'lagoon-blue', 'midnight-blue', 'light-orange', 'pumpkin-orange', 'light-concrete', 'sunny-grass', 'navy-blue', 'lilac-eyes', 'apricot-red', 'orange-peel', 'silver-glint', 'bright-moss', 'deep-ocean', 'summer-sky', 'berry-red', 'light-cocoa', 'grey-stone', 'tank-green', 'coral-green', 'sugar-plum', 'pink-tulip', 'shady-rust', 'wet-rock', 'wet-moss', 'turquoise-sea', 'lavender-fields', 'piggy-red', 'light-mud', 'gun-metal', 'modern-green', 'french-coast', 'sweet-lilac', 'red-burgundy', 'pirate-gold']
    """Color of the label"""

class Request_updateLabel(TypedDict):
    position: NotRequired[int]
    """Position of the label within the board"""
    name: NotRequired[str | None]
    """Name/title of the label"""
    color: NotRequired[Literal['muddy-grey', 'autumn-leafs', 'morning-sky', 'antique-blue', 'egg-yellow', 'desert-sand', 'dark-granite', 'fresh-salad', 'lagoon-blue', 'midnight-blue', 'light-orange', 'pumpkin-orange', 'light-concrete', 'sunny-grass', 'navy-blue', 'lilac-eyes', 'apricot-red', 'orange-peel', 'silver-glint', 'bright-moss', 'deep-ocean', 'summer-sky', 'berry-red', 'light-cocoa', 'grey-stone', 'tank-green', 'coral-green', 'sugar-plum', 'pink-tulip', 'shady-rust', 'wet-rock', 'wet-moss', 'turquoise-sea', 'lavender-fields', 'piggy-red', 'light-mud', 'gun-metal', 'modern-green', 'french-coast', 'sweet-lilac', 'red-burgundy', 'pirate-gold']]
    """Color of the label"""

class Request_createList(TypedDict):
    type: Literal['active', 'closed']
    """Type/status of the list"""
    position: int
    """Position of the list within the board"""
    name: str
    """Name/title of the list"""

class Request_updateList(TypedDict):
    boardId: NotRequired[str]
    """ID of the board to move list to"""
    type: NotRequired[Literal['active', 'closed']]
    """Type/status of the list"""
    position: NotRequired[int]
    """Position of the list within the board"""
    name: NotRequired[str]
    """Name/title of the list"""
    color: NotRequired[Literal['berry-red', 'pumpkin-orange', 'lagoon-blue', 'pink-tulip', 'light-mud', 'orange-peel', 'bright-moss', 'antique-blue', 'dark-granite', 'turquoise-sea'] | None]
    """Color for the list"""

class Request_moveListCards(TypedDict):
    listId: str
    """ID of the target list (must be an archive-type list)"""

class Request_sortList(TypedDict):
    fieldName: Literal['name', 'dueDate', 'createdAt']
    """Field to sort cards by"""
    order: NotRequired[Literal['asc', 'desc']]
    """Sorting order"""

class Request_createBoardNotificationService(TypedDict):
    url: str
    """URL endpoint for notifications"""
    format: Literal['text', 'markdown', 'html']
    """Format for notification messages"""

class Request_createUserNotificationService(TypedDict):
    url: str
    """URL endpoint for notifications"""
    format: Literal['text', 'markdown', 'html']
    """Format for notification messages"""

class Request_updateNotificationService(TypedDict):
    url: NotRequired[str]
    """URL endpoint for notifications"""
    format: NotRequired[Literal['text', 'markdown', 'html']]
    """Format for notification messages"""

class Request_updateNotification(TypedDict):
    isRead: NotRequired[bool]
    """Whether the notification has been read"""

class Request_createProjectManager(TypedDict):
    userId: str
    """ID of the user who is assigned as project manager"""

class Request_createProject(TypedDict):
    type: Literal['shared', 'private']
    """Type of the project"""
    name: str
    """Name/title of the project"""
    description: NotRequired[str | None]
    """Detailed description of the project"""

class Request_updateProject(TypedDict):
    ownerProjectManagerId: NotRequired[str | None]
    """ID of the project manager who owns the project"""
    backgroundImageId: NotRequired[str | None]
    """ID of the background image used as background"""
    name: NotRequired[str]
    """Name/title of the project"""
    description: NotRequired[str | None]
    """Detailed description of the project"""
    backgroundType: NotRequired[Literal['gradient', 'image'] | None]
    """Type of background for the project"""
    backgroundGradient: NotRequired[Literal['old-lime', 'ocean-dive', 'tzepesch-style', 'jungle-mesh', 'strawberry-dust', 'purple-rose', 'sun-scream', 'warm-rust', 'sky-change', 'green-eyes', 'blue-xchange', 'blood-orange', 'sour-peel', 'green-ninja', 'algae-green', 'coral-reef', 'steel-grey', 'heat-waves', 'velvet-lounge', 'purple-rain', 'blue-steel', 'blueish-curve', 'prism-light', 'green-mist', 'red-curtain'] | None]
    """Gradient background for the project"""
    isHidden: NotRequired[bool]
    """Whether the project is hidden"""
    isFavorite: NotRequired[bool]
    """Whether the project is marked as favorite by the current user"""

class Request_createTaskList(TypedDict):
    position: int
    """Position of the task list within the card"""
    name: str
    """Name/title of the task list"""
    showOnFrontOfCard: NotRequired[bool]
    """Whether to show the task list on the front of the card"""
    hideCompletedTasks: NotRequired[bool]
    """Whether to hide completed tasks"""

class Request_updateTaskList(TypedDict):
    position: NotRequired[int]
    """Position of the task list within the card"""
    name: NotRequired[str]
    """Name/title of the task list"""
    showOnFrontOfCard: NotRequired[bool]
    """Whether to show the task list on the front of the card"""
    hideCompletedTasks: NotRequired[bool]
    """Whether to hide completed tasks"""

class Request_createTask(TypedDict):
    linkedCardId: NotRequired[str]
    """ID of the card linked to the task"""
    position: int
    """Position of the task within the task list"""
    name: NotRequired[str | None]
    """Name/title of the task (required if `linkedCardId` is not provided)"""
    isCompleted: NotRequired[bool]
    """Whether the task is completed"""

class Request_updateTask(TypedDict):
    taskListId: NotRequired[str]
    """ID of the task list to move the task to"""
    assigneeUserId: NotRequired[str | None]
    """ID of the user assigned to the task (null to unassign)"""
    position: NotRequired[int]
    """Position of the task within the task list"""
    name: NotRequired[str]
    """Name/title of the task"""
    isCompleted: NotRequired[bool]
    """Whether the task is completed"""

class Request_getTerms(TypedDict):
    language: NotRequired[str]
    """Language code for terms localization"""

class Request_createUser(TypedDict):
    email: str
    """Email address for login and notifications"""
    password: str
    """Password for user authentication (must meet password requirements)"""
    role: Literal['admin', 'projectOwner', 'boardUser']
    """User role defining access permissions"""
    name: str
    """Full display name of the user"""
    username: NotRequired[str | None]
    """Unique username for user identification"""
    phone: NotRequired[str | None]
    """Contact phone number"""
    organization: NotRequired[str | None]
    """Organization or company name"""
    language: NotRequired[Literal['ar-YE', 'bg-BG', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US', 'es-ES', 'et-EE', 'fa-IR', 'fi-FI', 'fr-FR', 'hu-HU', 'id-ID', 'it-IT', 'ja-JP', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'sk-SK', 'sr-Cyrl-RS', 'sr-Latn-RS', 'sv-SE', 'tr-TR', 'uk-UA', 'uz-UZ', 'zh-CN', 'zh-TW'] | None]
    """Preferred language for user interface and notifications"""
    subscribeToOwnCards: NotRequired[bool]
    """Whether the user subscribes to their own cards"""
    subscribeToCardWhenCommenting: NotRequired[bool]
    """Whether the user subscribes to cards when commenting"""
    turnOffRecentCardHighlighting: NotRequired[bool]
    """Whether recent card highlighting is disabled"""

class Request_getUser(TypedDict):
    subscribe: NotRequired[bool]
    """Whether to subscribe to real-time updates for this user (only for socket connections)"""

class Request_updateUser(TypedDict):
    role: NotRequired[Literal['admin', 'projectOwner', 'boardUser']]
    """User role defining access permissions"""
    name: NotRequired[str]
    """Full display name of the user"""
    avatar: NotRequired[dict[str, Any] | None]
    """Avatar of the user (only null value to remove avatar)"""
    phone: NotRequired[str | None]
    """Contact phone number"""
    organization: NotRequired[str | None]
    """Organization or company name"""
    language: NotRequired[Literal['ar-YE', 'bg-BG', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US', 'es-ES', 'et-EE', 'fa-IR', 'fi-FI', 'fr-FR', 'hu-HU', 'id-ID', 'it-IT', 'ja-JP', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'sk-SK', 'sr-Cyrl-RS', 'sr-Latn-RS', 'sv-SE', 'tr-TR', 'uk-UA', 'uz-UZ', 'zh-CN', 'zh-TW'] | None]
    """Preferred language for user interface and notifications"""
    subscribeToOwnCards: NotRequired[bool]
    """Whether the user subscribes to their own cards"""
    subscribeToCardWhenCommenting: NotRequired[bool]
    """Whether the user subscribes to cards when commenting"""
    turnOffRecentCardHighlighting: NotRequired[bool]
    """Whether recent card highlighting is disabled"""
    enableFavoritesByDefault: NotRequired[bool]
    """Whether favorites are enabled by default"""
    defaultEditorMode: NotRequired[Literal['wysiwyg', 'markup']]
    """Default markdown editor mode"""
    defaultHomeView: NotRequired[Literal['gridProjects', 'groupedProjects']]
    """Default view mode for the home page"""
    defaultProjectsOrder: NotRequired[Literal['byDefault', 'alphabetically', 'byCreationTime']]
    """Default sort order for projects display"""
    isDeactivated: NotRequired[bool]
    """Whether the user account is deactivated and cannot log in (for admins)"""

class Request_updateUserAvatar(TypedDict):
    file: str
    """Avatar image file (must be an image format)"""

class Request_updateUserEmail(TypedDict):
    email: str
    """Email address for login and notifications"""
    currentPassword: NotRequired[str]
    """Current password (required when updating own email)"""

class Request_updateUserPassword(TypedDict):
    password: str
    """Password (must meet password requirements)"""
    currentPassword: NotRequired[str]
    """Current password (required when updating own password)"""

class Request_updateUserUsername(TypedDict):
    username: NotRequired[str | None]
    """Unique username for user identification"""
    currentPassword: NotRequired[str]
    """Current password (required when updating own username)"""

class Request_createWebhook(TypedDict):
    name: str
    """Name/title of the webhook"""
    url: str
    """URL endpoint for the webhook"""
    accessToken: NotRequired[str | None]
    """Access token for webhook authentication"""
    events: NotRequired[str | None]
    """Comma-separated list of events that trigger the webhook"""
    excludedEvents: NotRequired[str | None]
    """Comma-separated list of events excluded from the webhook"""

class Request_updateWebhook(TypedDict):
    name: NotRequired[str]
    """Name/title of the webhook"""
    url: NotRequired[str]
    """URL endpoint for the webhook"""
    accessToken: NotRequired[str | None]
    """Access token for webhook authentication"""
    events: NotRequired[str | None]
    """Comma-separated list of events that trigger the webhook"""
    excludedEvents: NotRequired[str | None]
    """Comma-separated list of events excluded from the webhook"""



# Response Typing
class Response_acceptTerms(TypedDict):
    """Terms accepted successfully"""
    item: str
    """Access token for API authentication"""

class Response_createAccessToken(TypedDict):
    """Login successful"""
    item: str
    """Access token for API authentication"""

class Response_deleteAccessToken(TypedDict):
    """Logout successful"""
    item: str
    """Revoked access token"""

class Response_exchangeForAccessTokenWithOidc(TypedDict):
    """OIDC exchange successful"""
    item: str
    """Access token for API authentication"""

class Response_revokePendingToken(TypedDict):
    """Pending token revoked successfully"""
    item: dict[str, Any] | None
    """No data returned"""

class Response_getBoardActions(TypedDict):
    """Board actions retrieved successfully"""
    items: list[Action]
    included: Included_getBoardActions

class Included_getBoardActions(TypedDict):
    users: list[User]

class Response_getCardActions(TypedDict):
    """Card actions retrieved successfully"""
    items: list[Action]
    included: Included_getCardActions

class Included_getCardActions(TypedDict):
    users: list[User]

class Response_createAttachment(TypedDict):
    """Attachment created successfully"""
    item: Attachment

class Response_deleteAttachment(TypedDict):
    """Attachment deleted successfully"""
    item: Attachment

class Response_updateAttachment(TypedDict):
    """Attachment updated successfully"""
    item: Attachment

class Response_createBackgroundImage(TypedDict):
    """Background image uploaded successfully"""
    item: BackgroundImage

class Response_deleteBackgroundImage(TypedDict):
    """Background image deleted successfully"""
    item: BackgroundImage

class Response_createBaseCustomFieldGroup(TypedDict):
    """Base custom field group created successfully"""
    item: BaseCustomFieldGroup

class Response_deleteBaseCustomFieldGroup(TypedDict):
    """Base custom field group deleted successfully"""
    item: BaseCustomFieldGroup

class Response_updateBaseCustomFieldGroup(TypedDict):
    """Base custom field group updated successfully"""
    item: BaseCustomFieldGroup

class Response_createBoardMembership(TypedDict):
    """Board membership created successfully"""
    item: BoardMembership

class Response_deleteBoardMembership(TypedDict):
    """Board membership deleted successfully"""
    item: BoardMembership

class Response_updateBoardMembership(TypedDict):
    """Board membership updated successfully"""
    item: BoardMembership

class Response_createBoard(TypedDict):
    """Board created successfully"""
    item: Board
    included: Included_createBoard

class Included_createBoard(TypedDict):
    boardMemberships: list[BoardMembership]

class Response_deleteBoard(TypedDict):
    """Board deleted successfully"""
    item: Board

class Response_getBoard(TypedDict):
    """Board details retrieved successfully"""
    item: Item_getBoard
    included: Included_getBoard

class Included_getBoard(TypedDict):
    users: list[User]
    projects: list[Project]
    boardMemberships: list[BoardMembership]
    labels: list[Label]
    lists: list[List]
    cards: list[Included_getBoard_all]
    """Related cards"""
    cardMemberships: list[CardMembership]
    cardLabels: list[CardLabel]
    taskLists: list[TaskList]
    tasks: list[Task]
    attachments: list[Attachment]
    customFieldGroups: list[CustomFieldGroup]
    customFields: list[CustomField]
    customFieldValues: list[CustomFieldValue]

class Included_getBoard_all(Card):
    isSubscribed: bool
    """Whether the current user is subscribed to the card"""

class Item_getBoard(Board):
    isSubscribed: bool
    """Whether the current user is subscribed to the board"""

class Response_updateBoard(TypedDict):
    """Board updated successfully"""
    item: Board

class Response_createCardLabel(TypedDict):
    """Label added to card successfully"""
    item: CardLabel

class Response_deleteCardLabel(TypedDict):
    """Label removed from card successfully"""
    item: CardLabel

class Response_createCardMembership(TypedDict):
    """User added to card successfully"""
    item: CardMembership

class Response_deleteCardMembership(TypedDict):
    """User removed from card successfully"""
    item: CardMembership

class Response_createCard(TypedDict):
    """Card created successfully"""
    item: Card

class Response_getCards(TypedDict):
    """Cards retrieved successfully"""
    items: list[Items_getCards]
    included: Included_getCards

class Included_getCards(TypedDict):
    users: list[User]
    cardMemberships: list[CardMembership]
    cardLabels: list[CardLabel]
    taskLists: list[TaskList]
    tasks: list[Task]
    attachments: list[Attachment]
    customFieldGroups: list[CustomFieldGroup]
    customFields: list[CustomField]
    customFieldValues: list[CustomFieldValue]

class Items_getCards(Card):
    isSubscribed: bool
    """Whether the current user is subscribed to the card"""

class Response_deleteCard(TypedDict):
    """Card deleted successfully"""
    item: Card

class Response_getCard(TypedDict):
    """Card details retrieved successfully"""
    item: Item_getCard
    included: Included_getCard

class Included_getCard(TypedDict):
    users: list[User]
    cardMemberships: list[CardMembership]
    cardLabels: list[CardLabel]
    taskLists: list[TaskList]
    tasks: list[Task]
    attachments: list[Attachment]
    customFieldGroups: list[CustomFieldGroup]
    customFields: list[CustomField]
    customFieldValues: list[CustomFieldValue]

class Item_getCard(Card):
    isSubscribed: bool
    """Whether the current user is subscribed to the card"""

class Response_updateCard(TypedDict):
    """Card updated successfully"""
    item: Card

class Response_duplicateCard(TypedDict):
    """Card duplicated successfully"""
    item: Card
    included: Included_duplicateCard

class Included_duplicateCard(TypedDict):
    cardMemberships: list[CardMembership]
    cardLabels: list[CardLabel]
    taskLists: list[TaskList]
    tasks: list[Task]
    attachments: list[Attachment]
    customFieldGroups: list[CustomFieldGroup]
    customFields: list[CustomField]
    customFieldValues: list[CustomFieldValue]

class Response_readCardNotifications(TypedDict):
    """Notifications marked as read successfully"""
    item: Card
    included: Included_readCardNotifications

class Included_readCardNotifications(TypedDict):
    notifications: list[Notification]

class Response_createComment(TypedDict):
    """Comment created successfully"""
    item: Comment

class Response_getComments(TypedDict):
    """Comments retrieved successfully"""
    items: list[Comment]
    included: Included_getComments

class Included_getComments(TypedDict):
    users: list[User]

class Response_deleteComment(TypedDict):
    """Comment deleted successfully"""
    item: Comment

class Response_updateComments(TypedDict):
    """Comment updated successfully"""
    item: Comment

class Response_getConfig(TypedDict):
    """Configuration retrieved successfully"""
    item: Config

class Response_createBoardCustomFieldGroup(TypedDict):
    """Custom field group created successfully"""
    item: CustomFieldGroup

class Response_createCardCustomFieldGroup(TypedDict):
    """Custom field group created successfully"""
    item: CustomFieldGroup

class Response_deleteCustomFieldGroup(TypedDict):
    """Custom field group deleted successfully"""
    item: CustomFieldGroup

class Response_getCustomFieldGroup(TypedDict):
    """Custom field group details retrieved successfully"""
    item: CustomFieldGroup
    included: Included_getCustomFieldGroup

class Included_getCustomFieldGroup(TypedDict):
    customFields: list[CustomField]
    customFieldValues: list[CustomFieldValue]

class Response_updateCustomFieldGroup(TypedDict):
    """Custom field group updated successfully"""
    item: CustomFieldGroup

class Response_updateCustomFieldValue(TypedDict):
    """Custom field value created or updated successfully"""
    item: CustomFieldValue

class Response_deleteCustomFieldValue(TypedDict):
    """Custom field value deleted successfully"""
    item: CustomFieldValue

class Response_createCustomFieldInBaseGroup(TypedDict):
    """Custom field created successfully"""
    item: CustomField

class Response_createCustomFieldInGroup(TypedDict):
    """Custom field created successfully"""
    item: CustomField

class Response_deleteCustomField(TypedDict):
    """Custom field deleted successfully"""
    item: CustomField

class Response_updateCustomField(TypedDict):
    """Custom field updated successfully"""
    item: CustomField

class Response_createLabel(TypedDict):
    """Label created successfully"""
    item: Label

class Response_deleteLabel(TypedDict):
    """Label deleted successfully"""
    item: Label

class Response_updateLabel(TypedDict):
    """Label updated successfully"""
    item: Label

class Response_clearList(TypedDict):
    """List cleared successfully"""
    item: List

class Response_createList(TypedDict):
    """List created successfully"""
    item: List

class Response_deleteList(TypedDict):
    """List deleted successfully"""
    item: List
    included: Included_deleteList

class Included_deleteList(TypedDict):
    cards: list[Card]

class Response_getList(TypedDict):
    """List details retrieved successfully"""
    item: List
    included: Included_getList

class Included_getList(TypedDict):
    users: list[User]
    cards: list[Included_getList_all]
    """Related cards"""
    cardMemberships: list[CardMembership]
    cardLabels: list[CardLabel]
    taskLists: list[TaskList]
    tasks: list[Task]
    attachments: list[Attachment]
    customFieldGroups: list[CustomFieldGroup]
    customFields: list[CustomField]
    customFieldValues: list[CustomFieldValue]

class Included_getList_all(Card):
    isSubscribed: bool
    """Whether the current user is subscribed to the card"""

class Response_updateList(TypedDict):
    """List updated successfully"""
    item: List

class Response_moveListCards(TypedDict):
    """Cards moved successfully"""
    item: List
    included: Included_moveListCards

class Included_moveListCards(TypedDict):
    cards: list[Card]
    actions: list[Action]

class Response_sortList(TypedDict):
    """List sorted successfully"""
    item: List
    included: Included_sortList

class Included_sortList(TypedDict):
    cards: list[Card]

class Response_createBoardNotificationService(TypedDict):
    """Notification service created successfully"""
    item: NotificationService

class Response_createUserNotificationService(TypedDict):
    """Notification service created successfully"""
    item: NotificationService

class Response_deleteNotificationService(TypedDict):
    """Notification service deleted successfully"""
    item: NotificationService

class Response_updateNotificationService(TypedDict):
    """Notification service updated successfully"""
    item: NotificationService

class Response_testNotificationService(TypedDict):
    """Test notification sent successfully"""
    item: NotificationService

class Response_getNotifications(TypedDict):
    """Notifications retrieved successfully"""
    items: list[Notification]
    included: Included_getNotifications

class Included_getNotifications(TypedDict):
    users: list[User]

class Response_readAllNotifications(TypedDict):
    """Notifications marked as read successfully"""
    items: list[Notification]

class Response_getNotification(TypedDict):
    """Notification details retrieved successfully"""
    item: Notification
    included: Included_getNotification

class Included_getNotification(TypedDict):
    users: list[User]

class Response_updateNotification(TypedDict):
    """Notification updated successfully"""
    item: Notification

class Response_createProjectManager(TypedDict):
    """Project manager created successfully"""
    item: ProjectManager

class Response_deleteProjectManager(TypedDict):
    """Project manager deleted successfully"""
    item: ProjectManager

class Response_createProject(TypedDict):
    """Project created successfully"""
    item: Project
    included: Included_createProject

class Included_createProject(TypedDict):
    projectManagers: list[ProjectManager]

class Response_getProjects(TypedDict):
    """Projects retrieved successfully"""
    items: list[Items_getProjects]
    included: Included_getProjects

class Included_getProjects(TypedDict):
    users: list[User]
    projectManagers: list[ProjectManager]
    backgroundImages: list[BackgroundImage]
    baseCustomFieldGroups: list[BaseCustomFieldGroup]
    boards: list[Board]
    boardMemberships: list[BoardMembership]
    customFields: list[CustomField]
    notificationServices: list[NotificationService]

class Items_getProjects(Project):
    isFavorite: bool
    """Whether the project is marked as favorite by the current user"""

class Response_deleteProject(TypedDict):
    """Project deleted successfully"""
    item: Project

class Response_getProject(TypedDict):
    """Project details retrieved successfully"""
    item: Item_getProject
    included: Included_getProject

class Included_getProject(TypedDict):
    users: list[User]
    projectManagers: list[ProjectManager]
    backgroundImages: list[BackgroundImage]
    baseCustomFieldGroups: list[BaseCustomFieldGroup]
    boards: list[Board]
    boardMemberships: list[BoardMembership]
    customFields: list[CustomField]
    notificationServices: list[NotificationService]

class Item_getProject(Project):
    isFavorite: bool
    """Whether the project is marked as favorite by the current user"""

class Response_updateProject(TypedDict):
    """Project updated successfully"""
    item: Project

class Response_createTaskList(TypedDict):
    """Task list created successfully"""
    item: TaskList

class Response_deleteTaskList(TypedDict):
    """Task list deleted successfully"""
    item: TaskList

class Response_getTaskList(TypedDict):
    """Task list details retrieved successfully"""
    item: TaskList
    included: Included_getTaskList

class Included_getTaskList(TypedDict):
    tasks: list[Task]

class Response_updateTaskList(TypedDict):
    """Task list updated successfully"""
    item: TaskList

class Response_createTask(TypedDict):
    """Task created successfully"""
    item: Task

class Response_deleteTask(TypedDict):
    """Task deleted successfully"""
    item: Task

class Response_updateTask(TypedDict):
    """Task updated successfully"""
    item: Task

class Response_getTerms(TypedDict):
    """Terms content retrieved successfully"""
    item: Item_getTerms

class Item_getTerms(TypedDict):
    type: Literal['general', 'extended']
    language: Literal['de-DE', 'en-US']
    content: str
    signature: str

class Response_createUser(TypedDict):
    """User created successfully"""
    item: User

class Response_getUsers(TypedDict):
    """List of users retrieved successfully"""
    items: list[User]

class Response_deleteUser(TypedDict):
    """User deleted successfully"""
    item: User

class Response_getUser(TypedDict):
    """User details retrieved successfully"""
    item: User
    included: Included_getUser

class Included_getUser(TypedDict):
    notificationServices: list[NotificationService]

class Response_updateUser(TypedDict):
    """User updated successfully"""
    item: User

class Response_updateUserAvatar(TypedDict):
    """Avatar updated successfully"""
    item: User

class Response_updateUserEmail(TypedDict):
    """Email updated successfully"""
    item: User

class Response_updateUserPassword(TypedDict):
    """Password updated successfully"""
    item: User
    included: Included_updateUserPassword

class Included_updateUserPassword(TypedDict):
    accessTokens: list[str]
    """New acces tokens (when updating own password)"""

class Response_updateUserUsername(TypedDict):
    """Username updated successfully"""
    item: User

class Response_createWebhook(TypedDict):
    """Webhook created successfully"""
    item: Webhook

class Response_getWebhooks(TypedDict):
    """List of webhooks retrieved successfully"""
    items: list[Webhook]

class Response_deleteWebhook(TypedDict):
    """Webhook deleted successfully"""
    item: Webhook

class Response_updateWebhook(TypedDict):
    """Webhook updated successfully"""
    item: Webhook

