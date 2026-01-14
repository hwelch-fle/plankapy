from __future__ import annotations
from typing import Protocol
from typing import Any
from .schemas import *


class Response(Protocol):
    def json(self, *args: Any, **kwargs: Any) -> dict[str, Any]: ...


# Note: Clients require a base_url implementation that overrides the provided
# endpoint:
# e.g.
# >>> client = Client(base_url='http://<url>')
# >>> client.get('endpoint/id').request
# Request('http://<url>/endpoint/id')
# This functionality is provided by httpx.Client and httpx.AsyncClient
# But is missing from the requests.Session object
# This can be overcome by subclassing requests.Session:
# >>> class SessionURL(Session):
# ... 	def __init__(self, base_url: str|None=None):
# ...		super().__init__()
# ...		self.base_url = base_url
# ...
# ... 	@wraps(Session.request)
# ... 	def request(self, method, url, *args, **kwargs):
# ... 		if self.base_url is not None:
# ... 			url = self.base_url.rstrip('/') + '/' + url.lstrip('/')
# ... 		return super().request(method, url, *args, **kwargs)


class Client(Protocol):
    base_url: str

    def get(self, *args: Any, **kwargs: Any) -> Response: ...
    def post(self, *args: Any, **kwargs: Any) -> Response: ...
    def patch(self, *args: Any, **kwargs: Any) -> Response: ...
    def delete(self, *args: Any, **kwargs: Any) -> Response: ...


class PlankaEndpoints:
    def __init__(self, client: Client) -> None:
        self.client = client

    def acceptTerms(self, **body: Any) -> Any:
        """Accept terms during the authentication flow. Converts the pending token to an access token.
        pendingToken (str): Pending token received from the authentication flow
        signature (str): Terms signature hash based on user role
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/access-tokens/accept-terms".format(**params), data=body
        )

    def createAccessToken(self, **body: Any) -> Any:
        """Authenticates a user using email/username and password. Returns an access token for API authentication.
        emailOrUsername (str): Email address or username of the user
        password (str): Password of the user
        withHttpOnlyToken (bool): Whether to include an HTTP-only authentication cookie
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post("api/access-tokens".format(**params), data=body)

    def deleteAccessToken(self) -> Any:
        """Logs out the current user by deleting the session and access token. Clears HTTP-only cookies if present."""
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/access-tokens/me".format(**params))

    def exchangeForAccessTokenWithOidc(self, **body: Any) -> Any:
        """Exchanges an OIDC authorization code for an access token. Creates a user if they do not exist.
        code (str): Authorization code from OIDC provider
        nonce (str): Nonce value for OIDC security
        withHttpOnlyToken (bool): Whether to include HTTP-only authentication cookie
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/access-tokens/exchange-with-oidc".format(**params), data=body
        )

    def revokePendingToken(self, **body: Any) -> Any:
        """Revokes a pending authentication token and cancels the authentication flow.
        pendingToken (str): Pending token to revoke
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/access-tokens/revoke-pending-token".format(**params), data=body
        )

    def getBoardActions(self, boardId: str, beforeId: str) -> Any:
        """Retrieves a list of actions (activity history) for a specific board, with pagination support.

        Args:
                boardId (str): ID of the board to get actions for)
                beforeId (str): ID to get actions before (for pagination))
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/boards/{boardId}/actions".format(**params))

    def getCardActions(self, cardId: str, beforeId: str) -> Any:
        """Retrieves a list of actions (activity history) for a specific card, with pagination support.

        Args:
                cardId (str): ID of the card to get actions for)
                beforeId (str): ID to get actions before (for pagination))
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/cards/{cardId}/actions".format(**params))

    def createAttachment(self, cardId: str, **body: Any) -> Any:
        """Creates an attachment on a card. Requires board editor permissions.

        Args:
                cardId (str): ID of the card to create the attachment on)
                type (str): Type of the attachment
                file (str): File to upload
                url (str): URL for the link attachment
                name (str): Name/title of the attachment
                requestId (str): Request ID for tracking
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/cards/{cardId}/attachments".format(**params), data=body
        )

    def deleteAttachment(self, id: str) -> Any:
        """Deletes an attachment. Requires board editor permissions.

        Args:
                id (str): ID of the attachment to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/attachments/{id}".format(**params))

    def updateAttachment(self, id: str, **body: Any) -> Any:
        """Updates an attachment. Requires board editor permissions.

        Args:
                id (str): ID of the attachment to update)
                name (str): Name/title of the attachment
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/attachments/{id}".format(**params), data=body)

    def createBackgroundImage(self, projectId: str, **body: Any) -> Any:
        """Uploads a background image for a project. Requires project manager permissions.

        Args:
                projectId (str): ID of the project to upload background image for)
                file (str): Background image file (must be an image format)
                requestId (str): Request ID for tracking
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/projects/{projectId}/background-images".format(**params), data=body
        )

    def deleteBackgroundImage(self, id: str) -> Any:
        """Deletes a background image. Requires project manager permissions.

        Args:
                id (str): ID of the background image to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/background-images/{id}".format(**params))

    def createBaseCustomFieldGroup(self, projectId: str, **body: Any) -> Any:
        """Creates a base custom field group within a project. Requires project manager permissions.

        Args:
                projectId (str): ID of the project to create the base custom field group in)
                name (str): Name/title of the base custom field group
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/projects/{projectId}/base-custom-field-groups".format(**params),
            data=body,
        )

    def deleteBaseCustomFieldGroup(self, id: str) -> Any:
        """Deletes a base custom field group. Requires project manager permissions.

        Args:
                id (str): ID of the base custom field group to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/base-custom-field-groups/{id}".format(**params))

    def updateBaseCustomFieldGroup(self, id: str, **body: Any) -> Any:
        """Updates a base custom field group. Requires project manager permissions.

        Args:
                id (str): ID of the base custom field group to update)
                name (str): Name/title of the base custom field group
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch(
            "api/base-custom-field-groups/{id}".format(**params), data=body
        )

    def createBoardMembership(self, boardId: str, **body: Any) -> Any:
        """Creates a board membership within a board. Requires project manager permissions.

        Args:
                boardId (str): ID of the board to create the board membership in)
                userId (str): ID of the user who is a member of the board
                role (str): Role of the user in the board
                canComment (bool): Whether the user can comment on cards (applies only to viewers)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/boards/{boardId}/board-memberships".format(**params), data=body
        )

    def deleteBoardMembership(self, id: str) -> Any:
        """Deletes a board membership. Users can remove their own membership, project managers can remove any membership.

        Args:
                id (str): ID of the board membership to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/board-memberships/{id}".format(**params))

    def updateBoardMembership(self, id: str, **body: Any) -> Any:
        """Updates a board membership. Requires project manager permissions.

        Args:
                id (str): ID of the board membership to update)
                role (str): Role of the user in the board
                canComment (bool): Whether the user can comment on cards (applies only to viewers)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch(
            "api/board-memberships/{id}".format(**params), data=body
        )

    def createBoard(self, projectId: str, **body: Any) -> Any:
        """Creates a board within a project. Supports importing from Trello. Requires project manager permissions.

        Args:
                projectId (str): ID of the project to create the board in)
                position (int): Position of the board within the project
                name (str): Name/title of the board
                importType (str): Type of import
                importFile (str): Import file
                requestId (str): Request ID for tracking
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/projects/{projectId}/boards".format(**params), data=body
        )

    def deleteBoard(self, id: str) -> Any:
        """Deletes a board and all its contents (lists, cards, etc.). Requires project manager permissions.

        Args:
                id (str): ID of the board to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/boards/{id}".format(**params))

    def getBoard(self, id: str, subscribe: bool) -> Any:
        """Retrieves comprehensive board information, including lists, cards, and other related data.

        Args:
                id (str): ID of the board to retrieve)
                subscribe (bool): Whether to subscribe to real-time updates for this board (only for socket connections))
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/boards/{id}".format(**params))

    def updateBoard(self, id: str, **body: Any) -> Any:
        """Updates a board. Project managers can update all fields, board members can only subscribe/unsubscribe.

        Args:
                id (str): ID of the board to update)
                position (int): Position of the board within the project
                name (str): Name/title of the board
                defaultView (str): Default view for the board
                defaultCardType (str): Default card type for new cards
                limitCardTypesToDefaultOne (bool): Whether to limit card types to default one
                alwaysDisplayCardCreator (bool): Whether to always display card creators
                expandTaskListsByDefault (bool): Whether to expand task lists by default
                isSubscribed (bool): Whether the current user is subscribed to the board
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/boards/{id}".format(**params), data=body)

    def createCardLabel(self, cardId: str, **body: Any) -> Any:
        """Adds a label to a card. Requires board editor permissions.

        Args:
                cardId (str): ID of the card to add the label to)
                labelId (str): ID of the label to add to the card
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/cards/{cardId}/card-labels".format(**params), data=body
        )

    def deleteCardLabel(self, cardId: str, labelId: str) -> Any:
        """Removes a label from a card. Requires board editor permissions.

        Args:
                cardId (str): ID of the card to remove the label from)
                labelId (str): ID of the label to remove from the card)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete(
            "api/cards/{cardId}/card-labels/labelId:{labelId}".format(**params)
        )

    def createCardMembership(self, cardId: str, **body: Any) -> Any:
        """Adds a user to a card. Requires board editor permissions.

        Args:
                cardId (str): ID of the card to add the user to)
                userId (str): ID of the card to add the user to
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/cards/{cardId}/card-memberships".format(**params), data=body
        )

    def deleteCardMembership(self, cardId: str, userId: str) -> Any:
        """Removes a user from a card. Requires board editor permissions.

        Args:
                cardId (str): ID of the card to remove the user from)
                userId (str): ID of the user to remove from the card)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete(
            "api/cards/{cardId}/card-memberships/userId:{userId}".format(**params)
        )

    def createCard(self, listId: str, **body: Any) -> Any:
        """Creates a card within a list. Requires board editor permissions.

        Args:
                listId (str): ID of the list to create the card in)
                type (str): Type of the card
                position (int): Position of the card within the list
                name (str): Name/title of the card
                description (str): Detailed description of the card
                dueDate (str): Due date for the card
                isDueCompleted (bool): Whether the due date is completed
                stopwatch (dict[str, Any]): Stopwatch data for time tracking
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post("api/lists/{listId}/cards".format(**params), data=body)

    def getCards(
        self,
        listId: str,
        before: str,
        search: str,
        filterUserIds: str,
        filterLabelIds: str,
    ) -> Any:
        """Retrieves cards from an endless list with filtering, search, and pagination support.

        Args:
                listId (str): ID of the list to get cards from (must be an endless list))
                before (str): Pagination cursor (JSON object with id and listChangedAt))
                search (str): Search term to filter cards)
                filterUserIds (str): Comma-separated user IDs to filter by members)
                filterLabelIds (str): Comma-separated label IDs to filter by labels)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/lists/{listId}/cards".format(**params))

    def deleteCard(self, id: str) -> Any:
        """Deletes a card and all its contents (tasks, attachments, etc.). Requires board editor permissions.

        Args:
                id (str): ID of the card to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/cards/{id}".format(**params))

    def getCard(self, id: str) -> Any:
        """Retrieves comprehensive card information, including tasks, attachments, and other related data.

        Args:
                id (str): ID of the card to retrieve)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/cards/{id}".format(**params))

    def updateCard(self, id: str, **body: Any) -> Any:
        """Updates a card. Board editors can update all fields, viewers can only subscribe/unsubscribe.

        Args:
                id (str): ID of the card to update)
                boardId (str): ID of the board to move the card to
                listId (str): ID of the list to move the card to
                coverAttachmentId (str): ID of the attachment used as cover
                type (str): Type of the card
                position (int): Position of the card within the list
                name (str): Name/title of the card
                description (str): Detailed description of the card
                dueDate (str): Due date for the card
                isDueCompleted (bool): Whether the due date is completed
                stopwatch (dict[str, Any]): Stopwatch data for time tracking
                isSubscribed (bool): Whether the current user is subscribed to the card
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/cards/{id}".format(**params), data=body)

    def duplicateCard(self, id: str, **body: Any) -> Any:
        """Creates a duplicate of a card with all its contents (tasks, attachments, etc.). Requires board editor permissions.

        Args:
                id (str): ID of the card to duplicate)
                position (int): Position for the duplicated card within the list
                name (str): Name/title for the duplicated card
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post("api/cards/{id}/duplicate".format(**params), data=body)

    def readCardNotifications(self, id: str) -> Any:
        """Marks all notifications for a specific card as read for the current user. Requires access to the card.

        Args:
                id (str): ID of the card to mark notifications as read for)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.post("api/cards/{id}/read-notifications".format(**params))

    def createComment(self, cardId: str, **body: Any) -> Any:
        """Creates a new comment on a card. Requires board editor permissions or comment permissions.

        Args:
                cardId (str): ID of the card to create the comment on)
                text (str): Content of the comment
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/cards/{cardId}/comments".format(**params), data=body
        )

    def getComments(self, cardId: str, beforeId: str) -> Any:
        """Retrieves comments for a card with pagination support. Requires access to the card.

        Args:
                cardId (str): ID of the card to retrieve comments for)
                beforeId (str): ID to get comments before (for pagination))
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/cards/{cardId}/comments".format(**params))

    def deleteComment(self, id: str) -> Any:
        """Deletes a comment. Can be deleted by the comment author (with comment permissions) or project manager.

        Args:
                id (str): ID of the comment to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/comments/{id}".format(**params))

    def updateComments(self, id: str, **body: Any) -> Any:
        """Updates a comment. Only the author of the comment can update it.

        Args:
                id (str): ID of the comment to update)
                text (str): Content of the comment
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/comments/{id}".format(**params), data=body)

    def getConfig(self) -> Any:
        """Retrieves the application configuration."""
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/config".format(**params))

    def createBoardCustomFieldGroup(self, boardId: str, **body: Any) -> Any:
        """Creates a custom field group within a board. Either `baseCustomFieldGroupId` or `name` must be provided. Requires board editor permissions.

        Args:
                boardId (str): ID of the board to create the custom field group in)
                baseCustomFieldGroupId (str): ID of the base custom field group used as a template
                position (int): Position of the custom field group within the board
                name (str): Name/title of the custom field group (required if `baseCustomFieldGroupId` is not provided)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/boards/{boardId}/custom-field-groups".format(**params), data=body
        )

    def createCardCustomFieldGroup(self, cardId: str, **body: Any) -> Any:
        """Creates a custom field group within a card. Either `baseCustomFieldGroupId` or `name` must be provided. Requires board editor permissions.

        Args:
                cardId (str): ID of the card to create the custom field group in)
                baseCustomFieldGroupId (str): ID of the base custom field group used as a template
                position (int): Position of the custom field group within the card
                name (str): Name/title of the custom field group (required if `baseCustomFieldGroupId` is not provided)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/cards/{cardId}/custom-field-groups".format(**params), data=body
        )

    def deleteCustomFieldGroup(self, id: str) -> Any:
        """Deletes a custom field group. Requires board editor permissions.

        Args:
                id (str): ID of the custom field group to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/custom-field-groups/{id}".format(**params))

    def getCustomFieldGroup(self, id: str) -> Any:
        """Retrieves comprehensive custom field group information, including fields and values. Requires access to the board/card.

        Args:
                id (str): ID of the custom field group to retrieve)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/custom-field-groups/{id}".format(**params))

    def updateCustomFieldGroup(self, id: str, **body: Any) -> Any:
        """Updates a custom field group. Supports both board-wide and card-specific groups. Requires board editor permissions.

        Args:
                id (str): ID of the custom field group to update)
                position (int): Position of the custom field group within the board/card
                name (str): Name/title of the custom field group
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch(
            "api/custom-field-groups/{id}".format(**params), data=body
        )

    def updateCustomFieldValue(
        self, cardId: str, customFieldGroupId: str, customFieldId: str, **body: Any
    ) -> Any:
        """Creates or updates a custom field value for a card. Requires board editor permissions.

        Args:
                cardId (str): ID of the card to set the custom field value for)
                customFieldGroupId (str): ID of the custom field group the value belongs to)
                customFieldId (str): ID of the custom field the value belongs to)
                content (str): Content/value of the custom field
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch(
            "api/cards/{cardId}/custom-field-values/customFieldGroupId:{customFieldGroupId}:customFieldId:${customFieldId}".format(
                **params
            ),
            data=body,
        )

    def deleteCustomFieldValue(
        self, cardId: str, customFieldGroupId: str, customFieldId: str
    ) -> Any:
        """Deletes a custom field value for a specific card. Requires board editor permissions.

        Args:
                cardId (str): ID of the card to delete the custom field value from)
                customFieldGroupId (str): ID of the custom field group the value belongs to)
                customFieldId (str): ID of the custom field the value belongs to)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete(
            "api/cards/{cardId}/custom-field-value/customFieldGroupId:{customFieldGroupId}:customFieldId:${customFieldId}".format(
                **params
            )
        )

    def createCustomFieldInBaseGroup(
        self, baseCustomFieldGroupId: str, **body: Any
    ) -> Any:
        """Creates a custom field within a base custom field group. Requires project manager permissions.

        Args:
                baseCustomFieldGroupId (str): ID of the base custom field group to create the custom field in)
                position (int): Position of the custom field within the group
                name (str): Name/title of the custom field
                showOnFrontOfCard (bool): Whether to show the field on the front of cards
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/base-custom-field-groups/{baseCustomFieldGroupId}/custom-fields".format(
                **params
            ),
            data=body,
        )

    def createCustomFieldInGroup(self, customFieldGroupId: str, **body: Any) -> Any:
        """Creates a custom field within a custom field group. Requires board editor permissions.

        Args:
                customFieldGroupId (str): ID of the custom field group to create the custom field in)
                position (int): Position of the custom field within the group
                name (str): Name/title of the custom field
                showOnFrontOfCard (bool): Whether to show the field on the front of cards
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/custom-field-groups/{customFieldGroupId}/custom-fields".format(
                **params
            ),
            data=body,
        )

    def deleteCustomField(self, id: str) -> Any:
        """Deletes a custom field. Can delete the in base custom field group (requires project manager permissions) or the custom field group (requires board editor permissions).

        Args:
                id (str): ID of the custom field to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/custom-fields/{id}".format(**params))

    def updateCustomField(self, id: str, **body: Any) -> Any:
        """Updates a custom field. Can update in the base custom field group (requires project manager permissions) or the custom field group (requires board editor permissions).

        Args:
                id (str): ID of the custom field to update)
                position (int): Position of the custom field within the group
                name (str): Name/title of the custom field
                showOnFrontOfCard (bool): Whether to show the field on the front of cards
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/custom-fields/{id}".format(**params), data=body)

    def createLabel(self, boardId: str, **body: Any) -> Any:
        """Creates a label within a board. Requires board editor permissions.

        Args:
                boardId (str): ID of the board to create the label in)
                position (int): Position of the label within the board
                name (str): Name/title of the label
                color (str): Color of the label
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/boards/{boardId}/labels".format(**params), data=body
        )

    def deleteLabel(self, id: str) -> Any:
        """Deletes a label. Requires board editor permissions.

        Args:
                id (str): ID of the label to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/labels/{id}".format(**params))

    def updateLabel(self, id: str, **body: Any) -> Any:
        """Updates a label. Requires board editor permissions.

        Args:
                id (str): ID of the label to update)
                position (int): Position of the label within the board
                name (str): Name/title of the label
                color (str): Color of the label
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/labels/{id}".format(**params), data=body)

    def clearList(self, id: str) -> Any:
        """Deletes all cards from a list. Only works with trash-type lists. Requires project manager or board editor permissions.

        Args:
                id (str): ID of the list to clear (must be a trash-type list))
        """
        params = locals().copy()
        params.pop("self")
        return self.client.post("api/lists/{id}/clear".format(**params))

    def createList(self, boardId: str, **body: Any) -> Any:
        """Creates a list within a board. Requires board editor permissions.

        Args:
                boardId (str): ID of the board to create the list in)
                type (str): Type/status of the list
                position (int): Position of the list within the board
                name (str): Name/title of the list
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/boards/{boardId}/lists".format(**params), data=body
        )

    def deleteList(self, id: str) -> Any:
        """Deletes a list and moves its cards to a trash list. Can only delete finite lists. Requires board editor permissions.

        Args:
                id (str): ID of the list to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/lists/{id}".format(**params))

    def getList(self, id: str) -> Any:
        """Retrieves comprehensive list information, including cards, attachments, and other related data. Requires access to the board.

        Args:
                id (str): ID of the list to retrieve)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/lists/{id}".format(**params))

    def updateList(self, id: str, **body: Any) -> Any:
        """Updates a list. Can move lists between boards. Requires board editor permissions.

        Args:
                id (str): ID of the list to update)
                boardId (str): ID of the board to move list to
                type (str): Type/status of the list
                position (int): Position of the list within the board
                name (str): Name/title of the list
                color (str): Color for the list
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/lists/{id}".format(**params), data=body)

    def moveListCards(self, id: str, **body: Any) -> Any:
        """Moves all cards from a closed list to an archive list. Requires board editor permissions.

        Args:
                id (str): ID of the source list (must be a closed-type list))
                listId (str): ID of the target list (must be an archive-type list)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post("api/lists/{id}/move-cards".format(**params), data=body)

    def sortList(self, id: str, **body: Any) -> Any:
        """Sorts all cards within a list. Requires board editor permissions.

        Args:
                id (str): ID of the list to sort)
                fieldName (str): Field to sort cards by
                order (str): Sorting order
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post("api/lists/{id}/sort".format(**params), data=body)

    def createBoardNotificationService(self, boardId: str, **body: Any) -> Any:
        """Creates a new notification service for a board. Requires project manager permissions.

        Args:
                boardId (str): ID of the board to create notification service for)
                url (str): URL endpoint for notifications
                format (str): Format for notification messages
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/boards/{boardId}/notification-services".format(**params), data=body
        )

    def createUserNotificationService(self, userId: str, **body: Any) -> Any:
        """Creates a new notification service for a user. Users can only create services for themselves.

        Args:
                userId (str): ID of the user to create notification service for (must be the current user))
                url (str): URL endpoint for notifications
                format (str): Format for notification messages
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/users/{userId}/notification-services".format(**params), data=body
        )

    def deleteNotificationService(self, id: str) -> Any:
        """Deletes a notification service. Users can delete their own services, project managers can delete board services.

        Args:
                id (str): ID of the notification service to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/notification-services/{id}".format(**params))

    def updateNotificationService(self, id: str, **body: Any) -> Any:
        """Updates a notification service. Users can update their own services, project managers can update board services.

        Args:
                id (str): ID of the notification service to update)
                url (str): URL endpoint for notifications
                format (str): Format for notification messages
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch(
            "api/notification-services/{id}".format(**params), data=body
        )

    def testNotificationService(self, id: str) -> Any:
        """Sends a test notification to verify the notification service is working. Users can test their own services, project managers can test board services.

        Args:
                id (str): ID of the notification service to test)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.post("api/notification-services/{id}/test".format(**params))

    def getNotifications(self) -> Any:
        """Retrieves all unread notifications for the current user, including creator users."""
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/notifications".format(**params))

    def readAllNotifications(self) -> Any:
        """Marks all notifications for the current user as read."""
        params = locals().copy()
        params.pop("self")
        return self.client.post("api/notifications/read-all".format(**params))

    def getNotification(self, id: str) -> Any:
        """Retrieves notification, including creator users. Users can only access their own notifications.

        Args:
                id (str): ID of the notification to retrieve)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/notifications/{id}".format(**params))

    def updateNotification(self, id: str, **body: Any) -> Any:
        """Updates a notification. Users can only update their own notifications.

        Args:
                id (str): ID of the notification to update)
                isRead (bool): Whether the notification has been read
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/notifications/{id}".format(**params), data=body)

    def createProjectManager(self, projectId: str, **body: Any) -> Any:
        """Creates a project manager within a project. Requires admin privileges for shared projects or existing project manager permissions. The user must be an admin or project owner.

        Args:
                projectId (str): ID of the project to create the project manager in)
                userId (str): ID of the user who is assigned as project manager
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/projects/{projectId}/project-managers".format(**params), data=body
        )

    def deleteProjectManager(self, id: str) -> Any:
        """Deletes a project manager. Requires admin privileges for shared projects or existing project manager permissions. Cannot remove the last project manager.

        Args:
                id (str): ID of the project manager to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/project-managers/{id}".format(**params))

    def createProject(self, **body: Any) -> Any:
        """Creates a project. The current user automatically becomes a project manager.
        type (str): Type of the project
        name (str): Name/title of the project
        description (str): Detailed description of the project
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post("api/projects".format(**params), data=body)

    def getProjects(self) -> Any:
        """Retrieves all projects the current user has access to, including managed projects, membership projects, and shared projects (for admins)."""
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/projects".format(**params))

    def deleteProject(self, id: str) -> Any:
        """Deletes a project. The project must not have any boards. Requires project manager permissions.

        Args:
                id (str): ID of the project to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/projects/{id}".format(**params))

    def getProject(self, id: str) -> Any:
        """Retrieves comprehensive project information, including boards, board memberships, and other related data.

        Args:
                id (str): ID of the project to retrieve)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/projects/{id}".format(**params))

    def updateProject(self, id: str, **body: Any) -> Any:
        """Updates a project. Accessible fields depend on user permissions.

        Args:
                id (str): ID of the project to update)
                ownerProjectManagerId (str): ID of the project manager who owns the project
                backgroundImageId (str): ID of the background image used as background
                name (str): Name/title of the project
                description (str): Detailed description of the project
                backgroundType (str): Type of background for the project
                backgroundGradient (str): Gradient background for the project
                isHidden (bool): Whether the project is hidden
                isFavorite (bool): Whether the project is marked as favorite by the current user
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/projects/{id}".format(**params), data=body)

    def createTaskList(self, cardId: str, **body: Any) -> Any:
        """Creates a task list within a card. Requires board editor permissions.

        Args:
                cardId (str): ID of the card to create task list in)
                position (int): Position of the task list within the card
                name (str): Name/title of the task list
                showOnFrontOfCard (bool): Whether to show the task list on the front of the card
                hideCompletedTasks (bool): Whether to hide completed tasks
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/cards/{cardId}/task-lists".format(**params), data=body
        )

    def deleteTaskList(self, id: str) -> Any:
        """Deletes a task list and all its tasks. Requires board editor permissions.

        Args:
                id (str): ID of the task list to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/task-lists/{id}".format(**params))

    def getTaskList(self, id: str) -> Any:
        """Retrieves task list information, including tasks. Requires access to the card.

        Args:
                id (str): ID of the task list to retrieve)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/task-lists/{id}".format(**params))

    def updateTaskList(self, id: str, **body: Any) -> Any:
        """Updates a task list. Requires board editor permissions.

        Args:
                id (str): ID of the task list to update)
                position (int): Position of the task list within the card
                name (str): Name/title of the task list
                showOnFrontOfCard (bool): Whether to show the task list on the front of the card
                hideCompletedTasks (bool): Whether to hide completed tasks
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/task-lists/{id}".format(**params), data=body)

    def createTask(self, taskListId: str, **body: Any) -> Any:
        """Creates a task within a task list. Either `linkedCardId` or `name` must be provided. Requires board editor permissions.

        Args:
                taskListId (str): ID of the task list to create task in)
                linkedCardId (str): ID of the card linked to the task
                position (int): Position of the task within the task list
                name (str): Name/title of the task (required if `linkedCardId` is not provided)
                isCompleted (bool): Whether the task is completed
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post(
            "api/task-lists/{taskListId}/tasks".format(**params), data=body
        )

    def deleteTask(self, id: str) -> Any:
        """Deletes a task. Requires board editor permissions.

        Args:
                id (str): ID of the task to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/tasks/{id}".format(**params))

    def updateTask(self, id: str, **body: Any) -> Any:
        """Updates a task. Linked card tasks have limited update options. Requires board editor permissions.

        Args:
                id (str): ID of the task to update)
                taskListId (str): ID of the task list to move the task to
                assigneeUserId (str): ID of the user assigned to the task (null to unassign)
                position (int): Position of the task within the task list
                name (str): Name/title of the task
                isCompleted (bool): Whether the task is completed
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/tasks/{id}".format(**params), data=body)

    def getTerms(self, type: str, language: str) -> Any:
        """Retrieves terms and conditions in the specified language.

        Args:
                type (str): Type of terms to retrieve)
                language (str): Language code for terms localization)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/terms/{type}".format(**params))

    def createUser(self, **body: Any) -> Any:
        """Creates a user account. Requires admin privileges.
        email (str): Email address for login and notifications
        password (str): Password for user authentication (must meet password requirements)
        role (str): User role defining access permissions
        name (str): Full display name of the user
        username (str): Unique username for user identification
        phone (str): Contact phone number
        organization (str): Organization or company name
        language (str): Preferred language for user interface and notifications
        subscribeToOwnCards (bool): Whether the user subscribes to their own cards
        subscribeToCardWhenCommenting (bool): Whether the user subscribes to cards when commenting
        turnOffRecentCardHighlighting (bool): Whether recent card highlighting is disabled
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post("api/users".format(**params), data=body)

    def getUsers(self) -> Any:
        """Retrieves a list of all users. Requires admin or project owner privileges."""
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/users".format(**params))

    def deleteUser(self, id: str) -> Any:
        """Deletes a user account. Cannot delete the default admin user. Requires admin privileges.

        Args:
                id (str): ID of the user to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/users/{id}".format(**params))

    def getUser(self, id: str, subscribe: bool) -> Any:
        """Retrieves a user. Use 'me' as ID to get the current user.

        Args:
                id (str): ID of the user or 'me' for current user)
                subscribe (bool): Whether to subscribe to real-time updates for this user (only for socket connections))
        """
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/users/{id}".format(**params))

    def updateUser(self, id: str, **body: Any) -> Any:
        """Updates a user. Users can update their own profile, admins can update any user.

        Args:
                id (str): ID of the user to update)
                role (str): User role defining access permissions
                name (str): Full display name of the user
                avatar (dict[str, Any]): Avatar of the user (only null value to remove avatar)
                phone (str): Contact phone number
                organization (str): Organization or company name
                language (str): Preferred language for user interface and notifications
                subscribeToOwnCards (bool): Whether the user subscribes to their own cards
                subscribeToCardWhenCommenting (bool): Whether the user subscribes to cards when commenting
                turnOffRecentCardHighlighting (bool): Whether recent card highlighting is disabled
                enableFavoritesByDefault (bool): Whether favorites are enabled by default
                defaultEditorMode (str): Default markdown editor mode
                defaultHomeView (str): Default view mode for the home page
                defaultProjectsOrder (str): Default sort order for projects display
                isDeactivated (bool): Whether the user account is deactivated and cannot log in (for admins)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/users/{id}".format(**params), data=body)

    def updateUserAvatar(self, id: str, **body: Any) -> Any:
        """Updates a user's avatar image. Users can update their own avatar, admins can update any user's avatar.

        Args:
                id (str): ID of the user whose avatar to update)
                file (str): Avatar image file (must be an image format)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post("api/users/{id}/avatar".format(**params), data=body)

    def updateUserEmail(self, id: str, **body: Any) -> Any:
        """Updates a user's email address. Users must provide current password when updating their own email. Admins can update any user's email without a password.

        Args:
                id (str): ID of the user whose email to update)
                email (str): Email address for login and notifications
                currentPassword (str): Current password (required when updating own email)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/users/{id}/email".format(**params), data=body)

    def updateUserPassword(self, id: str, **body: Any) -> Any:
        """Updates a user's password. Users must provide a current password when updating their own password. Admins can update any user's password without the current password. Returns a new access token when updating own password.

        Args:
                id (str): ID of the user whose password to update)
                password (str): Password (must meet password requirements)
                currentPassword (str): Current password (required when updating own password)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/users/{id}/password".format(**params), data=body)

    def updateUserUsername(self, id: str, **body: Any) -> Any:
        """Updates a user's username. Users must provide a current password when updating their own username (unless they are SSO users with `oidcIgnoreUsername` enabled). Admins can update any user's username without the current password.

        Args:
                id (str): ID of the user whose username to update)
                username (str): Unique username for user identification
                currentPassword (str): Current password (required when updating own username)
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/users/{id}/username".format(**params), data=body)

    def createWebhook(self, **body: Any) -> Any:
        """Creates a webhook. Requires admin privileges.
        name (str): Name/title of the webhook
        url (str): URL endpoint for the webhook
        accessToken (str): Access token for webhook authentication
        events (str): Comma-separated list of events that trigger the webhook
        excludedEvents (str): Comma-separated list of events excluded from the webhook
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.post("api/webhooks".format(**params), data=body)

    def getWebhooks(self) -> Any:
        """Retrieves a list of all configured webhooks. Requires admin privileges."""
        params = locals().copy()
        params.pop("self")
        return self.client.get("api/webhooks".format(**params))

    def deleteWebhook(self, id: str) -> Any:
        """Deletes a webhook. Requires admin privileges.

        Args:
                id (str): ID of the webhook to delete)
        """
        params = locals().copy()
        params.pop("self")
        return self.client.delete("api/webhooks/{id}".format(**params))

    def updateWebhook(self, id: str, **body: Any) -> Any:
        """Updates a webhook. Requires admin privileges.

        Args:
                id (str): ID of the webhook to update)
                name (str): Name/title of the webhook
                url (str): URL endpoint for the webhook
                accessToken (str): Access token for webhook authentication
                events (str): Comma-separated list of events that trigger the webhook
                excludedEvents (str): Comma-separated list of events excluded from the webhook
        """
        params = locals().copy()
        params.pop("self")
        body = params.pop("body")
        return self.client.patch("api/webhooks/{id}".format(**params), data=body)
