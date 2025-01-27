from __future__ import annotations

from .interfaces import (
    Planka,
    Project,
    User,
    Board,
    Label,
    Action,
    BoardMembership,
    Card,
    CardLabel,
    CardMembership,
    List,
)

from .constants import (
    ActionType,
)

# Get by functions
# These all return a list of objects because Planka does not enforce unique names

def by_username(user_list: list[User], name: str) -> list[User]:
    """Get users by username
    
    Args:
        user_list (list[User]): List of users to search
        name (str): Username of the user
    
    Returns:
        list[User]: Users with the given username
    """
    return [user for user in user_list if user.username == name]

def by_project_name(project_list: list[Project], name: str) -> list[Project]:
    """Get projects by name
    
    Args:
        project_list (list[Project]): List of projects to search
        name (str): Name of the project
        
    Returns:
        list[Project]: Projects with the given name
    """
    return [project for project in project_list if project.name == name]

def by_board_name(board_list: list[Board], name: str) -> list[Board]:
    """Get boards by name
    
    Args:
        board_list (list[Board]): List of boards to search
        name (str): Name of the board
        
    Returns:
        list[Board]: Boards with the given name
    """
    return [board for board in board_list if board.name == name]

def by_list_name(list_list: list[List], name: str) -> list[List]:
    """Get lists by name
    
    Args:
        list_list (list[List]): List of lists to search
        name (str): Name of the list
        
    Returns:
        list[List]: Lists with the given name
    """
    return [list_ for list_ in list_list if list_.name == name]

def by_card_name(card_list: list[Card], name: str) -> list[Card]:
    """Get cards by name
    
    Args:
        card_list (list[Card]): List of cards to search
        name (str): Name of the card
        
    Returns:
        list[Card]: Cards with the given 
    """
    return [card for card in card_list if card.name == name]

def by_label_name(label_list: list[Label], name: str) -> list[Label]:
    """Get labels by name
    
    Args:
        label_list (list[Label]): List of labels to search
        name (str): Name of the label
        
    Returns:
        list[Label]: Labels with the given name
    """
    return [label for label in label_list if label.name == name]

def by_action_type(action_list: list[Action], type: ActionType) -> list[Action]:
    """Get actions by type
    
    Args:
        action_list (list[Action]): List of actions to search
        type (ActionType): Type of the action
        
    Returns:
        list[Action]: Actions with the given type
    """
    return [action for action in action_list if action.type == type]

# Batch Add functions

def add_editors_to_board(board: Board, users: list[User]) -> list[BoardMembership]:
    """Add users to a board with editing permissions
    
    Args:
        board (Board): Board to add users to
        users (list[User]): Users to add
        
    Returns:
        Board: Board with users added
    """
    return [board.add_user(users, canComment=True) for user in users]

def add_viewers_to_board(board: Board, users: list[User]) -> list[BoardMembership]:
    """Add users to a board with viewing permissions
    
    Args:
        board (Board): Board to add users to
        users (list[User]): Users to add
        
    Returns:
        list[BoardMembership]: BoardMemberships created
    """
    return [board.add_user(user, canComment=False) for user in users]

def create_board_labels(board: Board, labels: list[Label]) -> list[Label]:
    """Create labels on a board
    
    Args:
        board (Board): Board to create labels on
        labels (list[Label]): Labels to create
        
    Returns:
        list[Label]: The labels that were created
    """
    return [board.create_label(label) for label in labels]

def add_labels_to_card(card: Card, labels: list[Label]) -> list[CardLabel]:
    """Add labels to a card
    
    Args:
        card (Card): Card to add labels to
        labels (list[Label]): Labels to add
        
    Returns:
        list[CardLabel]: CardLabel relationships created
    """
    return [card.add_label(label) for label in labels]

def add_members_to_card(card: Card, members: list[User]) -> list[CardMembership]:
    """Add members to a card
    
    Args:
        card (Card): Card to add members to
        members (list[User]): Members to add
        
    Returns:
        list[CardMembership]: CardMemberships created
    """
    return [card.add_member(member) for member in members]


# Batch Delete functions

def delete_projects(projects: list[Project]) -> list[Project]:
    """Delete a list of projects
    
    Args:
        projects (list[Project]): Projects to delete
        
    Returns:
        list[Project]: Projects that were deleted
    """
    return [project.delete() for project in projects]
        
def delete_boards(boards: list[Board]) -> list[Board]:
    """Delete a list of boards
    
    Args:
        boards (list[Board]): Boards to delete
    
    Returns:
        list[Board]: Boards that were deleted
    """
    return [board.delete() for board in boards]
        
def delete_lists(lists: list[List]) -> list[List]:
    """Delete a list of lists
    
    Args:
        lists (list[List]): Lists to delete
        
    Returns:
        list[List]: Lists that were deleted
    """
    return [list_.delete() for list_ in lists]
        
def delete_cards(cards: list[Card]) -> list[Card]:
    """Delete a list of cards
    
    Args:
        cards (list[Card]): Cards to delete
        
    Returns:
        list[Card]: Cards that were deleted
    """
    return [card.delete() for card in cards]

def delete_labels(labels: list[Label]) -> list[Label]:
    """Delete a list of labels
    
    Args:
        labels (list[Label]): Labels to delete
        
    Returns:
        list[Label]: Labels that were deleted
    """
    return [label.delete() for label in labels]

def delete_users(users: list[User]) -> list[User]:
    """Delete a list of users
    
    Args:
        users (list[User]): Users to delete
        
    Returns:
        list[User]: Users that were deleted
    """
    return [user.delete() for user in users]
        
def delete_actions(actions: list[Action]) -> list[Action]:
    """Delete a list of actions
    
    Args:
        actions (list[Action]): Actions to delete
        
    Returns:
        list[Action]: Actions that were deleted
    """
    return [action.delete() for action in actions]
        
# Batch remove functions

def remove_labels_from_card(card: Card, labels: list[Label]) -> list[Label]:
    """Remove labels from a card
    
    Args:
        card (Card): Card to remove labels from
        labels (list[Label]): Labels to remove
        
    Returns:
        list[Label]: Labels that were removed
    """
    return [card.remove_label(label) for label in labels]

# Get by name functions
def get_projects_by_name(planka: Planka, name: str) -> list[Project]:
    """Get all projects with the given name
    
    Args:
        planka (Planka): Planka instance
        name (str): Name of the project
    
    Returns:
        list[Project]: List of projects with the given name
    """
    return by_project_name(planka.projects, name)

def get_boards_by_name(project: Project, name: str) -> list[Board]:
    """Get all boards in a project by name
    
    Args:
        project (Project): Project to search
        name (str): Name of the board
    
    Returns:
        list[Board]: Boards in the project with the given name
    """
    return by_board_name(project.boards, name)

def get_lists_by_name(board: Board, name: str) -> list[List]:
    """Get all lists in a board by name

    Args:
        board (Board): Board to search
        name (str): Name of the list
    
    Returns:
        list[List]: Lists in the board with the given name
    """
    return by_list_name(board.lists, name)
        
def get_cards_by_name(org_unit: List | Board, name: str) -> list[Card]:
    """Get a card by name from a list or board
    
    Args:
        org_unit (List | Board): List or Board to search
        name (str): Name of the card
    
    Returns:
        list[Card]: Cards in the list or board with the given name
    """
    return by_card_name(org_unit.cards, name)
        
def get_labels_by_name(org_unit: Board | Card, name: str) -> list[Label]:
    """Get a label by name from a board or card
    
    Args:
        org_unit (Board | Card): Board or Card to search
        name (str): Name of the label
        
    Returns:
        list[Label]: Labels in the board or card with the given name
    """
    return by_label_name(org_unit.labels, name)
        
def get_users_by_username(org_unit: Planka | Project | Board, username: str) -> list[User]:
    """Get a user by username from a Planka Instance, Project, or Board
    
    Args:
        org_unit (Planka | Project | Board): Planka instance, Project, or Board to search
        username (str): Username of the user
    
    Returns:
        list[User]: Users in the org_unit with the given username
    """
    return by_username(org_unit.users, username)