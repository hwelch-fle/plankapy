"""All Object Models for Plankapy v2.5+ (Planka 2.0.0+)"""

__all__ = [
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
    "PlankaModel",
    "Project",
    "ProjectManager",
    "Stopwatch",
    "Task",
    "TaskList",
    "User",
    "Webhook",
]

__all__.extend(
    [
        "BackgroundGradients",
        "BoardRoles",
        "BoardViews",
        "CardTypes",
        "EditorModes",
        "HomeViews",
        "LabelColors",
        "Languages",
        "ListColors",
        "LockableFields",
        "NotificationTypes",
        "ProjectOrderings",
        "TermsTypes",
        "UserRoles",
    ]
)

from ._base import PlankaModel
from ._literals import *
from .action import Action
from .attachment import Attachment
from .background_image import BackgroundImage
from .base_custom_field_group import BaseCustomFieldGroup
from .board import Board
from .board_membership import BoardMembership
from .card import Card, Stopwatch
from .card_label import CardLabel
from .card_membership import CardMembership
from .comment import Comment
from .config import Config
from .custom_field import CustomField
from .custom_field_group import CustomFieldGroup
from .custom_field_value import CustomFieldValue
from .label import Label
from .list_ import List
from .notification import Notification
from .notification_service import NotificationService
from .project import Project
from .project_manager import ProjectManager
from .task import Task
from .task_list import TaskList
from .user import User
from .webhook import Webhook

# Model Format #####################################
# 1) add_*: For creating an association between a model and another model     #
#   - Card.add_label(label: Label): ...                                       #
#                                                                             #
# 2) create_*: For creating a NEW model associated with the current model     #
#   - Card.create_label(name='new label', color='berry-red', position='top')  #
#                                                                             #
# 3) get_*: For associations that require 2+ requests to find                 #
#   - label.get_cards()                                                       #
#                                                                             #
# 4) remove_*: Remove/Delete an associated object                             #
#   - card.remove_label(label)                                                #
#                                                                             #
# 5) delete_*: Delete an associated object                                    #
#   - board.delete_label(label)                                               #
#                                                                             #
# 6) sync, update, delete: If possible allow GET, PATCH, DELETE passthroughs  #
#   - If sync required more than 2 requests, don't implement it               #
#                                                                             #
# 7) @property: All attributes and includes that require 1 request            #
#   - board.labels (in board['included'])                                     #
#   - board.cards (has endpoint getCards(boardId))                            #
#                                                                             #
# 8) @field.setter: Allow setting properties available in Model patch request #
#   - These setters should implement the update() method of the model         #
#                                                                             #
# 9) datetimes: All ISO 8601 strings should be converted to datetime          #
#   - Use `timezone` property of session if no timezone in ISO string         #
#                                                                             #
# 10) Exceptions: Allow HTTPStatusError to be raised unless necessary         #
#   - PermissionError: Use session.current_role and current_id for checks     #
#   - LookupError: If the resource cannot be found (deleted on server)        #
#   - ValueError: Reserved for file operations (see Attachment)               #
#   - Any other Exception needs to be clearly documented                      #
#   - NOTE: If an endpoint will raise an error, allow it to do so. Do not     #
#       mask server exceptions with custom ones!                              #
#                                                                             #
# 11) property iteration: If a list property needs to be iterated, cache it   #
#   - _list_cards = list.cards                                                #
#   - This will prevent multiple requests to list._includes                   #
#   - If your operation is slow, do not cache to prevent de-syncing           #
#       - Slow is ~1-2s We want to capture accurate board states              #
###############################################################################
