from typing import Literal, get_args

__all__ =   (
    
    # Literal Types for hinting
    "BoardView",
    "CardType",
    "BoardRole",
    "LabelColor",
    "ListColor",
    "BackgroundGradient",
    "Language",
    "EditorMode",
    "HomeView",
    "ProjectOrdering",
    "ProjectType",
    "TermsType",
    "LockableField",
    "NotificationType",
    "UserRole",
    
    # String Tuples (for in/choice operations)
    "BoardViews",
    "CardTypes",
    "BoardRoles",
    "LabelColors",
    "ListColors",
    "BackgroundGradients",
    "Languages",
    "EditorModes",
    "HomeViews",
    "ProjectOrderings",
    "ProjectTypes",
    "TermsTypes",
    "LockableFields",
    "NotificationTypes",
    "UserRoles",
)

BoardView = Literal['kanban', 'grid', 'list']
BoardViews: tuple[BoardView, ...] = get_args(BoardView)

# Single element literals throw warnings on __args__ access
BoardImportType = Literal['trello']
BoardImportTypes: tuple[BoardImportType, ...] = BoardImportType # type: ignore

CardType = Literal['project', 'story']
CardTypes: tuple[CardType, ...] = get_args(CardType)

BoardRole = Literal['editor', 'viewer']
BoardRoles: tuple[BoardRole, ...] = get_args(BoardRole)

LabelColor = Literal[
    'muddy-grey', 'autumn-leafs', 'morning-sky', 'antique-blue', 
    'egg-yellow', 'desert-sand', 'dark-granite', 'fresh-salad', 
    'lagoon-blue', 'midnight-blue', 'light-orange', 'pumpkin-orange', 
    'light-concrete', 'sunny-grass', 'navy-blue', 'lilac-eyes', 
    'apricot-red', 'orange-peel', 'silver-glint', 'bright-moss', 
    'deep-ocean', 'summer-sky', 'berry-red', 'light-cocoa', 'grey-stone', 
    'tank-green', 'coral-green', 'sugar-plum', 'pink-tulip', 'shady-rust', 
    'wet-rock', 'wet-moss', 'turquoise-sea', 'lavender-fields', 'piggy-red', 
    'light-mud', 'gun-metal', 'modern-green', 'french-coast', 'sweet-lilac', 
    'red-burgundy', 'pirate-gold',
]
LabelColors: tuple[LabelColor, ...] = get_args(LabelColor)

ListColor = Literal[
    'berry-red', 'pumpkin-orange', 'lagoon-blue', 'pink-tulip', 
    'light-mud', 'orange-peel', 'bright-moss', 'antique-blue', 
    'dark-granite', 'turquoise-sea',
]
ListColors: tuple[ListColor, ...] = get_args(ListColor)

ListType = Literal['active', 'closed', 'archive', 'trash']
ListTypes: tuple[ListType, ...] = get_args(ListType)

UserListType = Literal['active', 'closed']
UserListTypes: tuple[UserListType, ...] = get_args(UserListType)

SystemListType = Literal['archive', 'trash']
SystemListTypes: tuple[SystemListType, ...] = get_args(SystemListType)

NotificationType = Literal['moveCard', 'commentCard', 'addMemberToCard', 'mentionInComment']
NotificationTypes: tuple[NotificationType, ...] = get_args(NotificationType)

NotificationServiceFormat = Literal['text', 'markdown', 'html']
NotificationServiceFormats: tuple[NotificationServiceFormat, ...] = get_args(NotificationServiceFormat)

BackgroundType = Literal['gradient', 'image']
BackgroundTypes: tuple[BackgroundType, ...] = get_args(BackgroundType)

BackgroundGradient = Literal[
    'old-lime', 'ocean-dive', 'tzepesch-style', 'jungle-mesh', 
    'strawberry-dust', 'purple-rose', 'sun-scream', 'warm-rust', 
    'sky-change', 'green-eyes', 'blue-xchange', 'blood-orange', 
    'sour-peel', 'green-ninja', 'algae-green', 'coral-reef', 
    'steel-grey', 'heat-waves', 'velvet-lounge', 'purple-rain', 
    'blue-steel', 'blueish-curve', 'prism-light', 'green-mist', 
    'red-curtain'
]
BackgroundGradients = get_args(BackgroundGradient)

Language = Literal[
    'ar-YE', 'bg-BG', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US', 
    'es-ES', 'et-EE', 'fa-IR', 'fi-FI', 'fr-FR', 'hu-HU', 'id-ID', 'it-IT', 
    'ja-JP', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 
    'sk-SK', 'sr-Cyrl-RS', 'sr-Latn-RS', 'sv-SE', 'tr-TR', 'uk-UA', 'uz-UZ', 
    'zh-CN', 'zh-TW',
]
Languages: tuple[Language, ...] = get_args(Language)

EditorMode = Literal['wysiwyg', 'markup']
EditorModes: tuple[EditorMode, ...] = get_args(EditorMode)

HomeView = Literal['gridProjects', 'groupedProjects']
HomeViews: tuple[HomeView, ...] = get_args(HomeView)

ProjectOrdering = Literal['byDefault', 'alphabetically', 'byCreationTime']
ProjectOrderings: tuple[ProjectOrdering, ...] = get_args(ProjectOrdering)

ProjectType = Literal['shared', 'private']
ProjectTypes: tuple[ProjectType] = get_args(ProjectType)

TermsType = Literal['general', 'extended']
TermsTypes: tuple[TermsType, ...] = get_args(TermsType)

LockableField = Literal['email', 'password', 'name']
LockableFields: tuple[LockableField, ...] = get_args(LockableField)

UserRole = Literal['admin', 'projectOwner', 'boardUser']
UserRoles: tuple[UserRole, ...] = get_args(UserRole)
