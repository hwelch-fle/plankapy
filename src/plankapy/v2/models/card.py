from __future__ import annotations

from httpx import HTTPStatusError

__all__ = ('Card', 'Stopwatch', )

from datetime import datetime, timedelta
from ._base import PlankaModel
from ._helpers import Position, dtfromiso, dttoiso, get_position, model_list
from ..api import schemas, paths, events

# Deferred Model imports at bottom of file

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any, Unpack
    #from models import *
    from ._literals import CardType, BoardRole


class Card(PlankaModel[schemas.Card]):
    """Python interface for Planka Cards"""
    
    __events__ = events.CardEvents

    @property
    def url(self) -> str:
        """The URL to the card"""
        return str(self.client.base_url.join(f'/cards/{self.id}'))
    
    @property
    def formal_name(self)-> str:
        """Get a formal name for the card `{Project}->{Board}->{List}->{Card}`"""
        return f'{self.project.name}->{self.board.name}->{self.list.name}->{self.name}'
        
    # Included objects
    @property
    def _included(self):
        return self.endpoints.getCard(self.id)['included']
    
    @property
    @model_list
    def attachments(self) -> list[Attachment]:
        """Get all Attachments associated with the Card"""
        return [Attachment(a, self.session) for a in self._included['attachments']]
    
    @property
    @model_list
    def card_memberships(self) -> list[CardMembership]:
        """Get all CardMemberships associated with the Card"""
        return [CardMembership(cm, self.session) for cm in self._included['cardMemberships']]
    
    @property
    @model_list
    def users(self) -> list[User]:
        """Get all Users associated with the Card (including Creator)"""
        return [User(u, self.session) for u in self._included['users']]
    
    @property
    @model_list
    def members(self) -> list[User]:
        """Get all Users Assigned to the card"""
        return [cm.user for cm in self.card_memberships]
    
    @property
    @model_list
    def card_labels(self) -> list[CardLabel]:
        """Get all CardLabel associations for the Card"""
        return [CardLabel(cl, self.session) for cl in self._included['cardLabels']]
    
    @property
    @model_list
    def labels(self) -> list[Label]:
        """Get all Labels associated with the Card"""
        return [cl.label for cl in self.card_labels]
    
    @property
    @model_list
    def tasks(self) -> list[Task]:
        """Get all Tasks associated with the card"""
        return [Task(t, self.session) for t in self._included['tasks']]
    
    @property
    @model_list
    def task_lists(self) -> list[TaskList]:
        """Get all TaskLists associated with the Card"""
        return [TaskList(tl, self.session) for tl in self._included['taskLists']]
    
    @property
    @model_list
    def custom_field_groups(self) -> list[CustomFieldGroup]:
        """Get all CustomFieldGroups associated with the Card"""
        return [CustomFieldGroup(cfg, self.session) for cfg in self._included['customFieldGroups']]
    
    @property
    @model_list
    def custom_fields(self) -> list[CustomField]:
         """Get all CustomFields associated with the Card"""
         return [CustomField(cf, self.session) for cf in self._included['customFields']]
    
    @property
    @model_list
    def custom_field_values(self) -> list[CustomFieldValue]:
        """Get all CustomFieldValues associated with the Card"""
        return [CustomFieldValue(cfv, self.session) for cfv in self._included['customFieldValues']]
    
    @property
    @model_list
    def comments(self) -> list[Comment]:
        """Get all Comments on the Card"""
        return [Comment(c, self.session) for c in self.endpoints.getComments(self.id)['items']]

    @property
    @model_list
    def actions(self) -> list[Action]:
        """Get all Actions associated with the Card"""
        return [Action(a, self.session) for a in self.endpoints.getCardActions(self.id)['items']]

    # Card props
    @property
    def subscribed(self) -> bool:
        """If the current user is subscribed to the Card"""
        return self.endpoints.getCard(self.id)['item']['isSubscribed']
    @subscribed.setter
    def subscribed(self, subscribed: bool) -> None:
        """Set subscription status on the Card for the current User"""
        self.update(isSubscribed=subscribed)
    
    @property
    def project(self) -> Project:
        """Get the Project that the card is in"""
        return self.board.project

    @property
    def board(self) -> Board:
        """The Board the Card belongs to"""
        return Board(self.endpoints.getBoard(self.schema['boardId'])['item'], self.session)
    
    @property
    def list(self)-> List:
        """The List the Card belongs to"""
        return List(self.endpoints.getList(self.schema['listId'])['item'], self.session)
    @list.setter
    def list(self, list: List) -> Card:
        """Set List the Card belongs to"""
        self.update(listId=list.id, boardId=list.board.id)
        return self

    @property
    def creator(self) -> User | None:
        """The User who Created the card
        
        Note: 
            If the creator is no longer on the Board, only Admins and Project Owners 
            can see them. Otherwise, None will be returned
            
            If the User has been deleted, Admins and Project Owners will get a Server error 
        """
        for u in self.board.users:
            if u.id == self.schema['creatorUserId']:
                return u
        
        if self.current_role in ('admin', 'projectOwner'):
            return User(self.endpoints.getUser(self.schema['creatorUserId'])['item'], self.session) 
        
    @property
    def prev_list(self) -> List | None:
        """The previous List the card was in (available when in archive or trash)"""
        if self.schema['prevListId']:
            return List(self.endpoints.getList(self.schema['prevListId'])['item'], self.session)
    
    @property
    def cover(self) -> Attachment | None:
        """The Attachment used as cover (None if no cover)"""
        for attachment in self.attachments:
            if attachment.id == self.schema['coverAttachmentId']:
                return attachment
            
    @cover.setter
    def cover(self, attachment: Attachment) -> None:
        """Set the Card cover"""
        self.update(coverAttachmentId=attachment.id)
    
    @property
    def type(self):
        """Type of the Card"""
        return self.schema['type']
    @type.setter
    def type(self, type: CardType) -> None:
        """Set the Card type"""
        self.update(type=type)
    
    @property
    def position(self) -> int:
        """Position of the Card within the List"""
        return self.schema['position']
    @position.setter
    def position(self, position: int) -> None:
        """Set the card position"""
        self.update(position=position)
    
    @property
    def name(self) -> str:
        """Name/title of the Card"""
        return self.schema['name']
    @name.setter
    def name(self, name: str) -> None:
        """Set the Card name"""
        self.update(name=name)
    
    @property
    def description(self) -> str:
        """Detailed description of the Card"""
        return self.schema['description']
    @description.setter
    def description(self, description: str) -> None:
        """Set the Card Description"""
        self.update(description=description)
    
    @property
    def due_date(self) -> datetime | None:
        """Due date for the card"""
        if self.schema['dueDate']:
            return dtfromiso(self.schema['dueDate'], self.session.timezone)
        return None
    @due_date.setter
    def due_date(self, due_date: datetime | str) -> None:
        """Set the due date (If using a string, a valid ISO 8601 string is required)"""
        self.update(dueDate=str(due_date))
    
    @property
    def due_date_completed(self) -> bool:
        """Whether the due date is completed"""
        return self.schema['isDueCompleted']
    @due_date_completed.setter
    def due_date_completed(self, is_completed: bool) -> None:
        """Set the due date completion status"""
        self.update(isDueCompleted=is_completed)
    
    @property
    def stopwatch(self) -> Stopwatch:
        """Stopwatch for time tracking"""
        return Stopwatch(self)
    
    @property
    def comments_count(self) -> int:
        """Total number of comments on the Card"""
        return self.schema['commentsTotal']
    @property
    def is_closed(self) -> bool:
        """Whether the Card is closed"""
        return self.schema['isClosed']
    
    @property
    def list_changed_at(self) -> datetime:
        """When the Card was last moved between Lists"""
        return dtfromiso(self.schema['listChangedAt'], self.session.timezone)
    
    @property
    def created_at(self) -> datetime:
        """When the Card was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the Card was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)

    # Special Methods
    def sync(self):
        """Sync the Card with the Planka server"""
        self.schema = self.endpoints.getCard(self.id)['item']
        
    def update(self, **kwargs: Unpack[paths.Request_updateCard]):
        """Update the Card

        Note:
            dueDate can be set using ISO 8601 string or datetime object
        """
        # Convert the dueDate to a iso string if a datetime is passed
        if 'dueDate' in kwargs:
            kwargs['dueDate'] = str(kwargs['dueDate'])
        self.schema = self.endpoints.updateCard(self.id, **kwargs)['item']
 
    def delete(self):
        """Delete the Card"""
        return self.endpoints.deleteCard(self.id)

    @model_list
    def read_notifications(self) -> list[Notification]:
        """Read all the current User's Notifications for the Card"""
        return [Notification(n, self.session) for n in self.endpoints.readCardNotifications(self.id)['included']['notifications']]

    def comment(self, comment: str, *, mentions: Sequence[User]|None=None) -> Comment:
        """Leave a comment as this user and mention any user included in the mentions list
        
        Args:
            text: The text body of the comment (`@[name|username|email]` will mention)
            mentions: A sequence of Users that will be mentioned after the body
        
        Note:
            If a user is explicitly mentioned in the comment, they will be removed from the 
            suffix mention. e.g. 
            ```python
            >>> card.comment(
            ...     'Fix this @user1, then send to @user2', 
            ...     mentions=[user1, user2, user3]
            ... )
            '''Fix this @user1, then send to @user2
            @user3'''
            ```
            
        Example:
            ```python
                >>> card.comment('Need Fix', mentions=card2.users)
                # Comment from current user On Card:
                Need Fix
                @user1
                @user2
            ```
        """
        # Store inline mentions to prevent additional mention in postfix
        _mentioned: list[User] = []
        if '@' in comment:
            for u in self.board.users:
                # Replace raw @ mentions with markdown formatted mentions
                # Allow mentioning by name, username, or email
                if f'@{u.email}' in comment:
                    comment = comment.replace(f'@{u.email}', f'@[{u.email}]({u.id})')
                    _mentioned.append(u)
                elif f'@{u.name}' in comment:
                    comment = comment.replace(f'@{u.name}', f'@[{u.name}]({u.id})')
                    _mentioned.append(u)
                elif f'@{u.username}' in comment:
                    comment = comment.replace(f'@{u.username}', f'@[{u.username}]({u.id})')
                    _mentioned.append(u)
        
        # Add additional postfix mentions
        if mentions:
            mentions = [m for m in mentions if m not in _mentioned]
            comment = '\n'.join([comment, *[f"@[{u.name}]({u.id})" for u in mentions or []]])
        return Comment(self.endpoints.createComment(self.id, text=comment)['item'], self.session)

    def move(self, list: List, position: Position = 'top') -> Card:
        """Move the card to a new list (default to top of new list)"""
        self.update(
            listId=list.id, 
            boardId=list.board.id, 
            position=get_position(list.cards, position),
        )
        return self

    def duplicate(self, position: Position = 'top', *, name: str|None=None) -> Card:
        """Duplicate the card in the current List
        
        Args:
            position (Position): The position to place the new Card in (default: `top`)
            name (str|None): An optional name to give the new Card (default `{name} (copy)`)
        """
        position = get_position(self.list.cards, position)
        return Card(
            self.endpoints.duplicateCard(
                self.id, 
                position=position, 
                name=name or f'{self.name} (copy)'
            )['item'], 
            self.session
        )

    def restore(self, position: Position='top') -> Card:
        """Restore the Card from arcive/trash to its previous list"""
        if self.prev_list is not None:
            self.move(self.prev_list, position)
        return self
    
    def add_attachment(self, attachment: str | bytes, 
                       *, 
                       cover: bool=False, 
                       download_url: bool=False,
                       name: str | None=None) -> Attachment:
        """Add an Attachment to the card
        
        Args:
            attachment (str | bytes): The URL or raw bytes of the attachment
            cover (bool): Set the new attachment as the cover of the card
            download_url (bool): If a link is used, download the file from the link and attach it (default: `False`)
            name (str | None): The optional name of the attachment (default is `hash() + mimetypes.guess_type(attachment)`)
            
        Returns:
            Attachment
            
        Raises:
            HTTPStatusError: If the url cannot be downloaded
            OSError: If a local file cannot be opened and read
        """
        # Force a PermissionError early if the user isn't a board editor
        if self.session.current_id not in [e.id for e in self.board.editors]:
            self.endpoints.createAttachment(self.id, type='link', url='nourl', name='NO_PERMISSION')
        
        # Deferred import of mimetypes that is only used here
        # This function takes so long anyways so the import delay 
        # isn't noticable
        import mimetypes
        
        # Handle filepath or URL
        mime_type = None
        extension = '.bin'
        if isinstance(attachment, str):
            
            # Guess URL file type
            if attachment.startswith('http'):
                mime_type, *_ = mimetypes.guess_type(attachment)
                mime_type = mime_type or 'application/octet-stream'
                extension = mimetypes.guess_extension(mime_type) or '.bin'
                
                # Download the file if requested
                if download_url:
                    try:
                        req = self.client.get(attachment)
                        attachment = req.raise_for_status().read()
                    except HTTPStatusError as status_error:
                        status_error.add_note(f'Unable to download attachment from {attachment}')
                        raise
                
                # Attach a link otherwise
                else:
                    return Attachment(
                        self.endpoints.createAttachment(
                            self.id, 
                            type='link', 
                            url=attachment, 
                            name=name or f'{name or hash(attachment)}{extension}')['item'], 
                        self.session
                    )
            
            # Guess local file type
            # And read Bytes
            else:
                mime_type, *_ = mimetypes.guess_file_type(attachment)
                mime_type = mime_type or 'application/octet-stream'
                attachment = open(attachment, 'rb').read()
            
        mime_type = mime_type or 'application/octet-stream'
        extension = mimetypes.guess_extension(mime_type) or '.bin'
        name = f'{name or hash(attachment)}'
        if not name.endswith(extension):
            name = f'{name}{extension}'        
        a = Attachment(
            self.endpoints.createAttachment(
                self.id, 
                name=name,
                type='file',
                file=bytes(attachment),
                requestId=str(abs(hash(datetime.now().isoformat()))),
                mime_type=mime_type,
            )['item'], 
            self.session
        )
        if cover:
            self.cover = a
        return a

    def get_field_values(self, *, with_groups: bool=False) -> dict[str, Any]:
        """Get a mapping of CustomFields to CustomFieldValues
        
        Args:
            with_groups (bool): If set to `True`, 
                return a nested dict with `{group: {field: value, ...}, ...}`, otherwise `{field: value ...}` (default: `False`)
        """
        if with_groups:
            return {
                cfg.name: {cfv.custom_field.name: cfv.content for cfv in cfg.custom_field_values}
                for cfg in self.custom_field_groups
            }
        else:
            return {
                cfv.custom_field.name: cfv.content
                for cfv in self.custom_field_values
            }

    def create_card_field_group(self, name: str, position: Position='top') -> CustomFieldGroup:
        """Create a CustomFieldGroup in the Card
        
        Args:
            name: The name of the group
            position: The position of the new group
        """
        return CustomFieldGroup(
                self.endpoints.createCardCustomFieldGroup(
                    self.id, 
                    name=name, 
                    position=get_position(self.custom_field_groups, position))['item'], 
                self.session
            )

    def add_card_fields(self, *fields: str,
                        group: str='Fields', 
                        position: Position='top') -> CustomFieldGroup:
        """Add fields directly to a Card
        
        Args:
            *fields: Varargs of the Fieldnames to add to the Card
            group: An optional FieldGroup name to add the fields to (default: `Fields`)
            position: The position to add the Card field group at (default: `top`)
        
        Returns:
            CustomFieldGroup
        """
        # Get an existing group if name matches
        cfg = (
            self.custom_field_groups[{'name': group}].dpop() 
            or self.create_card_field_group(group, position)
        )
        # Add any fields that don't already exist in the Group
        cfg.add_fields(*(set(fields) ^ set(cfg.custom_fields.extract('name'))))
        return cfg
        
    def add_member(self, user: User, 
                   *, 
                   add_to_board: bool=False, 
                   role: BoardRole='viewer', 
                   can_comment: bool=False) -> CardMembership:
        """Add a User to the Card
        
        Args:
            user (User): The User to add to the Card
            add_to_board (bool): Add the User to the Board if they are not already a member
            role (BoardRole): If User is added to board, set role (default: `viewer`)
            can_comment (bool): If User is added as a `viewer`, set commenting status (default: `False`)
        
        Note:
            Default options for adding to Board abide by least privilege so role and comment must be set 
        """
        # User is already a member
        for membership in self.card_memberships:
            if membership.user == user:
                return membership
        
        # Add the user to the board
        if user not in self.board.users and add_to_board:
            self.board.add_member(user, role=role, can_comment=can_comment if role == 'viewer' else True)
        
        return CardMembership(self.endpoints.createCardMembership(self.id, userId=user.id)['item'], self.session)

    @model_list
    def add_members(self, users: Sequence[User], 
                    *, 
                    add_to_board: bool=False, 
                    role: BoardRole='viewer', 
                    can_comment: bool=False) -> list[CardMembership]:
        """Add multiple members to a Card
        
        Args:
            users (Sequence[User]): The Users to add to the Card
            add_to_board (bool): Add the User to the Board if they are not already a member
            role (Literal['viewer', 'editor']): If User is added to board, set role (default: `viewer`)
            can_comment (bool): If User is added as a `viewer`, set commenting status (default: `False`)
        
        Note:
            Default options for adding to Board abide by least privilege so role and comment must be set

        """
        return [
            self.add_member(
                user, 
                add_to_board=add_to_board, 
                role=role, 
                can_comment=can_comment,
            )
            for user in users
        ]

    def remove_member(self, user: User) -> User | None:
        """Remove a User member from the Card
        
        Args:
            user (User): The User to remove
        
        Returns:
            (User | None): The removed User or None if tha User was not a member
        """
        for cm in self.card_memberships:
            if cm.user == user:
                cm.delete()
                return user

    @model_list
    def remove_members(self, users: Sequence[User]) -> list[User]:
        """Remove multiple members from a Card
        
        Args:
            users (Sequence[User]): The Users to remove from the Card
        
        Returns:
            list[User]: The Users that were removed from the card
            
        Note:
            If a User in the `users` sequence is not a member of the card, 
            They will be excluded from this list
        """
        return [
            user
            for user in users
            if self.remove_member(user) is not None
        ]

    def add_label(self, label: Label, 
                  *, 
                  add_to_board: bool=False) -> CardLabel:
        """Add a Label to the Card
        
        Args:
            label (Label): The Label to add to the card
            add_to_board (bool): If the Label is not in the board, add it (default: `False`)
        
        Returns:
            CardLabel: The CardLabel relationship
        
        Note:
            When using `add_to_board` The label position will default to the top of the label list
        """
        # Check if label is already on card
        for card_label in self.card_labels:
            if label.id == card_label.schema['labelId']:
                return card_label

        # Handle adding Label if it doesn't exist
        if label not in self.board.labels and add_to_board:
            label = label.add_to_board(self.board)
        
        # Create new CardLabel relationship
        return CardLabel(self.endpoints.createCardLabel(self.id, labelId=label.id)['item'], self.session)
    
    @model_list
    def add_labels(self, labels: Sequence[Label], 
                   *,
                   add_to_board: bool=False) -> list[CardLabel]:
        """Add multiple Labels to the Card
        
        Args:
            labels (Sequence[Label]): The Labels to add (must be associated with the card.board)
            add_to_board (bool): If a Label is not in the board, add it (default: `False`)
        
        Returns:
            list[CardLabel]: The added CardLabel relations
            
        Note:
            Any labels that are not on the Card's Board will be skipped
        """
        return [
            self.add_label(
                label, 
                add_to_board=add_to_board
            )
            for label in labels
        ]
    
    def remove_label(self, label: Label) -> Label | None:
        """Remove the Label from the Card
        
        Args:
            label (Label): The label to remove (must be associated with the Card)
        """
        for card_label in self.card_labels:
            if card_label.label == label:
                card_label.delete()
                return label

    @model_list
    def remove_labels(self, labels: Sequence[Label]) -> list[Label]:
        """Remove the Label from the Card
        
        Args:
            labels (Sequence[Label]): The labels to remove (must be associated with the Card)
        """
        return [removed for label in labels if (removed := self.remove_label(label))]

    def create_task_list(self, 
                      *, 
                      name: str,
                      position: Position | int='top',
                      show_on_card: bool=False,
                      hide_completed: bool=False) -> TaskList:
        """Create a NEW TaskList to the Card
        
        Args:
            name str: Name for the TaskList
            postion (Position | int): The position of the TaskList in the Card (default: `top`)
            show_on_card: bool: Show TaskList on the front of the card (default: `False`)
            hide_completed: bool: Hide completed tasks (default: `False`)

        Returns:
            The TaskList 
        """
        return TaskList(
            self.endpoints.createTaskList(
                self.id, 
                position=get_position(self.task_lists, position), 
                name=name, 
                showOnFrontOfCard=show_on_card, 
                hideCompletedTasks=hide_completed,
            )['item'], 
            self.session
        )

    def add_task_list(self, task_list: TaskList, 
                      *, 
                      name: str | None=None,
                      position: Position | int='top',
                      show_on_card: bool | None=None,
                      hide_completed: bool | None=None) -> TaskList:
        """Add a TaskList to the Card
        
        Args:
            task_list (TaskList): The TaskList to add
            name (str | None): Name override, None will use input name (default: `None`)
            postion (Position | int): The position of the TaskList in the Card (default: `top`)
            show_on_card: bool | None): Show On Card override, None will use input show (default: `None`)
            hide_completed: bool | None): Hide Completed override , None will use input hide (default: `None`)

        Returns:
            The TaskList 
        """
        return self.create_task_list(
            name=name or task_list.name,
            position=get_position(self.task_lists, position),
            show_on_card=show_on_card or task_list.show_on_front_of_card,
            hide_completed=hide_completed or task_list.hide_completed_tasks, 
        )
    
    def add_location(self, lat: float, lon: float, name: str, position: Position | int) -> CustomFieldGroup:
        """Add a point location to a card as a FieldGroup
        
        Args:
            lat (float): Latitude of the location
            lon (float): Longitude of the location
            name (str): Name of the location (FieldGroup name)
            position (Position | int): Position of the FieldGroup within the Card (default: `top`)
        """
        loc_group = self.add_card_fields('latitude', 'longitude', group=name, position=position)
        for field in loc_group.custom_field_values:
            if field.custom_field.name == 'latitude':
                field.content = str(lat)
            elif field.custom_field.name == 'longitude':
                field.content = str(lon)
        return loc_group


class Stopwatch:
    """Python interface for Planka Stopwatches"""

    def __init__(self, card: Card) -> None:
        self.card = card
        self.tz = card.session.timezone
    
    @property
    def schema(self):
        return self.card.schema['stopwatch'] or {'startedAt': None, 'total': 0}
    
    @property
    def enabled(self):
        """If the stopwatch is enabled for the card (visible on front)"""
        self.sync()
        return self.card.schema['stopwatch'] is not None
    @enabled.setter
    def enabled(self, enabled: bool):
        """Enable/Disable the stopwatch"""
        self.sync()
        self.card.update(stopwatch=self.schema if enabled and not self.enabled else None)
        return self.schema
            
    @property
    def total(self) -> timedelta:
        self.card.sync()
        # Get the stored total seconds
        total = self.schema['total']
        
        # If the stopwatch is running, 
        # compute the time delta in seconds and add to total
        # The `total` attribute is only incremented when `startedAt` 
        # is set to None/null
        if self.is_running:
            now = datetime.now(tz=self.tz)
            total += (now - (self.last_started or now)).total_seconds()
            
        return timedelta(seconds=total)
    
    @total.setter
    def total(self, total: timedelta | int) -> None:
        """Set the total of the stopwatch using seconds or a timedelta"""
        self.update(total=total)
    
    @property
    def last_started(self) -> datetime | None:
        """The time a running stopwatch was started (None if the stopwatch is stopped)"""
        self.card.sync()
        if started := self.schema.get('startedAt'):
            return dtfromiso(started, default_timezone=self.tz)
    
    @property
    def is_running(self) -> bool:
        """If the stopwatch is currently running"""
        return self.last_started is not None
    
    def start(self) -> datetime | None:
        """Start the stopwatch and return the current datetime (None if the stopwatch is started)"""
        if self.is_running:
           return None
        return datetime.now(tz=self.card.session.timezone)
    
    def stop(self) -> datetime | None:
        """Stop a running stopwatch and return the time it was last started"""
        started = self.last_started
        self.update(started_at=None)
        return started
    
    def update(self, started_at: datetime | str | None=None, total: timedelta | int | None=None) -> None:
        """Update the stopwatch"""        
        current = self.schema
        if started_at:
            current['startedAt'] = str(
                dttoiso(started_at, default_timezone=self.tz) 
                if isinstance(started_at, datetime) 
                else started_at
            )
        if total:
            current['total'] = int(round( # Round seconds
                total.total_seconds() 
                if isinstance(total, timedelta) 
                else total
            ))
        self.card.update(stopwatch=current)
    
    def sync(self):
        self.card.sync()
        
    def __repr__(self) -> str:
        return f'Stopwatch(Card({self.card.name}), total={self.total}, running={self.is_running})'
    
    def json(self) -> str:
        import json
        return json.dumps(self.schema)
    

from .action import Action
from .attachment import Attachment
from .board import Board
from .card_label import CardLabel
from .card_membership import CardMembership
from .comment import Comment
from .custom_field import CustomField
from .custom_field_group import CustomFieldGroup
from .custom_field_value import CustomFieldValue
from .label import Label
from .list_ import List
from .notification import Notification
from .project import Project
from .task import Task
from .task_list import TaskList
from .user import User