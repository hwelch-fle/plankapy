from typing import Literal

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
BoardViews: tuple[BoardView, ...] = BoardView.__args__

# Single element literals throw warnings on __args__ access
BoardImportType = Literal['trello']
BoardImportTypes: tuple[BoardImportType, ...] = BoardImportType.__args__ # type: ignore

CardType = Literal['project', 'story']
CardTypes: tuple[CardType, ...] = CardType.__args__

BoardRole = Literal['editor', 'viewer']
BoardRoles: tuple[BoardRole, ...] = BoardRole.__args__

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
LabelColors: tuple[LabelColor, ...] = LabelColor.__args__

ListColor = Literal[
    'berry-red', 'pumpkin-orange', 'lagoon-blue', 'pink-tulip', 
    'light-mud', 'orange-peel', 'bright-moss', 'antique-blue', 
    'dark-granite', 'turquoise-sea',
]
ListColors: tuple[ListColor, ...] = ListColor.__args__

ListType = Literal['active', 'closed', 'archive', 'trash']
ListTypes: tuple[ListType, ...] = ListType.__args__

UserListType = Literal['active', 'closed']
UserListTypes: tuple[UserListType, ...] = UserListType.__args__

SystemListType = Literal['archive', 'trash']
SystemListTypes: tuple[SystemListType, ...] = SystemListType.__args__

NotificationType = Literal['moveCard', 'commentCard', 'addMemberToCard', 'mentionInComment']
NotificationTypes: tuple[NotificationType, ...] = NotificationType.__args__

NotificationServiceFormat = Literal['text', 'markdown', 'html']
NotificationServiceFormats: tuple[NotificationServiceFormat, ...] = NotificationServiceFormat.__args__

BackgroundType = Literal['gradient', 'image']
BackgroundTypes: tuple[BackgroundType, ...] = BackgroundType.__args__

BackgroundGradient = Literal[
    'old-lime', 'ocean-dive', 'tzepesch-style', 'jungle-mesh', 
    'strawberry-dust', 'purple-rose', 'sun-scream', 'warm-rust', 
    'sky-change', 'green-eyes', 'blue-xchange', 'blood-orange', 
    'sour-peel', 'green-ninja', 'algae-green', 'coral-reef', 
    'steel-grey', 'heat-waves', 'velvet-lounge', 'purple-rain', 
    'blue-steel', 'blueish-curve', 'prism-light', 'green-mist', 
    'red-curtain'
]
BackgroundGradients = BackgroundGradient.__args__

Language = Literal[
    'ar-YE', 'bg-BG', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US', 
    'es-ES', 'et-EE', 'fa-IR', 'fi-FI', 'fr-FR', 'hu-HU', 'id-ID', 'it-IT', 
    'ja-JP', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 
    'sk-SK', 'sr-Cyrl-RS', 'sr-Latn-RS', 'sv-SE', 'tr-TR', 'uk-UA', 'uz-UZ', 
    'zh-CN', 'zh-TW',
]
Languages: tuple[Language, ...] = Language.__args__

EditorMode = Literal['wysiwyg', 'markup']
EditorModes: tuple[EditorMode, ...] = EditorMode.__args__

HomeView = Literal['gridProjects', 'groupedProjects']
HomeViews: tuple[HomeView, ...] = HomeView.__args__

ProjectOrdering = Literal['byDefault', 'alphabetically', 'byCreationTime']
ProjectOrderings: tuple[ProjectOrdering, ...] = ProjectOrdering.__args__

ProjectType = Literal['shared', 'private']
ProjectTypes: tuple[ProjectType] = ProjectType.__args__

TermsType = Literal['general', 'extended']
TermsTypes: tuple[TermsType, ...] = TermsType.__args__

LockableField = Literal['email', 'password', 'name']
LockableFields: tuple[LockableField, ...] = LockableField.__args__

UserRole = Literal['admin', 'projectOwner', 'boardUser']
UserRoles: tuple[UserRole, ...] = UserRole.__args__
