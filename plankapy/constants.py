from dataclasses import dataclass
from typing import Literal, TypeAlias

# All positions in Planka are multples of this number
OFFSET = 65535

# Sometimes elements get set to a half offset value
HALF_OFFSET = 32767.5

def get_position(value: int, zero_index: bool=False) -> int:
    """Converts a Planka position to an indexed position
    e.g. 65535 -> 1, 131070 -> 2, 196605 -> 3
    Args:
        value (int): The Planka position
        zero_index (bool, optional): Whether to use 0-indexed positions. Defaults to False.
    """
    if value % OFFSET == HALF_OFFSET:
        return 1
    return int(value / OFFSET) - zero_index

def set_position(value: int, zero_index: bool=False) -> int:
    """Converts an indexed position to a Planka position
    e.g. 1 -> 65535, 2 -> 131070, 3 -> 196605
    Args:
        value (int): The indexed position
        zero_index (bool, optional): Whether to use 0-indexed positions. Defaults to False.
    """
    return int(value * OFFSET) - zero_index

# From https://github.com/plankanban/planka/blob/master/server/api/models/Action.js
ActionType = Literal[
    'createCard',
    'moveCard',
    'commentCard',
]

# From https://github.com/plankanban/planka/blob/master/server/api/models/BoardMembership.js
BoardRole = Literal[
    'editor',
    'viewer',
]

# From https://github.com/plankanban/planka/blob/master/server/api/models/Project.js
Gradient = Literal[
  'old-lime',
  'ocean-dive',
  'tzepesch-style',
  'jungle-mesh',
  'strawberry-dust',
  'purple-rose',
  'sun-scream',
  'warm-rust',
  'sky-change',
  'green-eyes',
  'blue-xchange',
  'blood-orange',
  'sour-peel',
  'green-ninja',
  'algae-green',
  'coral-reef',
  'steel-grey',
  'heat-waves',
  'velvet-lounge',
  'purple-rain',
  'blue-steel',
  'blueish-curve',
  'prism-light',
  'green-mist',
  'red-curtain',
]

@dataclass
class Background:
    name: Gradient
    type: str = 'gradient'

@dataclass
class BackgroundImage:
    url: str
    coverUrl: str

# From https://github.com/plankanban/planka/blob/master/server/api/models/Label.js
LabelColor = Literal[
  'berry-red',
  'pumpkin-orange',
  'lagoon-blue',
  'pink-tulip',
  'light-mud',
  'orange-peel',
  'bright-moss',
  'antique-blue',
  'dark-granite',
  'lagune-blue',
  'sunny-grass',
  'morning-sky',
  'light-orange',
  'midnight-blue',
  'tank-green',
  'gun-metal',
  'wet-moss',
  'red-burgundy',
  'light-concrete',
  'apricot-red',
  'desert-sand',
  'navy-blue',
  'egg-yellow',
  'coral-green',
  'light-cocoa',
]

ListSorts = {
    'Name': 'name_asc',
    'Due date': 'dueDate_asc',
    'Oldest First': 'createdAt_asc',
    'Newest First': 'createdAt_desc',
}

SortOption = Literal[
    'Name',
    'Due date',
    'Oldest First',
    'Newest First',
]