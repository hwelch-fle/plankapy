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
    ActionType,
)

# Get by functions
# These all return a list of objects because Planka does not enforce unique names

def by_username(user_list: list[User], name: str) -> list[User]:
    return [user for user in user_list if user.username == name]

def by_project_name(project_list: list[Project], name: str) -> list[Project]:
    return [project for project in project_list if project.name == name]

def by_board_name(board_list: list[Board], name: str) -> list[Board]:
    return [board for board in board_list if board.name == name]

def by_list_name(list_list: list[List], name: str) -> list[List]:
    return [list_ for list_ in list_list if list_.name == name]

def by_card_name(card_list: list[Card], name: str) -> list[Card]:
    return [card for card in card_list if card.name == name]

def by_label_name(label_list: list[Label], name: str) -> list[Label]:
    return [label for label in label_list if label.name == name]

def by_action_type(action_list: list[Action], type: ActionType) -> list[Action]:
    return [action for action in action_list if action.type == type]

# Batch Add functions

def add_editors_to_board(board: Board, users: list[User]) -> Board:
    for user in users:
        board.add_user(user, canComment=True)
    return board

def add_viewers_to_board(board: Board, users: list[User]) -> Board:
    for user in users:
        board.add_user(user, canComment=False)
    return board

def create_board_labels(board: Board, labels: list[Label]) -> Board:
    for label in labels:
        board.create_label(label)
    return board

def add_labels_to_card(card: Card, labels: list[Label]) -> Card:
    for label in labels:
        card.add_label(label)
    return card

def add_members_to_card(card: Card, members: list[User]) -> Card:
    for member in members:
        card.add_member(member)
    return card


# Batch Delete functions

def delete_projects(projects: list[Project]) -> list[Project]:
    for project in projects:
        project.delete()
        
def delete_boards(boards: list[Board]) -> list[Board]:
    for board in boards:
        board.delete()
        
def delete_lists(lists: list[List]) -> list[List]:
    for list_ in lists:
        list_.delete()
        
def delete_cards(cards: list[Card]) -> list[Card]:
    for card in cards:
        card.delete()

def delete_labels(labels: list[Label]) -> list[Label]:
    for label in labels:
        label.delete()

def delete_users(users: list[User]) -> list[User]:
    for user in users:
        user.delete()
        
def delete_actions(actions: list[Action]) -> list[Action]:
    for action in actions:
        action.delete()
        
# Batch remove functions

def remove_labels_from_card(card: Card, labels: list[Label]) -> Card:
    card_labels = card.board.cardLabels
    
    for card_label in card_labels:
        label = card_label.label
        if label in labels:
            card.remove_label(label)
    
    return card