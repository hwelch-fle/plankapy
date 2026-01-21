from __future__ import annotations
from typing import (
    Literal,
    Unpack,
)
from httpx import AsyncClient
from .schemas import *
from .typ import *

__all__ = ("AsyncPlankaEndpoints",)

class AsyncPlankaEndpoints:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def acceptTerms(self, **kwargs: Unpack[Request_acceptTerms]) -> Response_acceptTerms:
        """Accept terms during the authentication flow. Converts the pending token to an access token.

        Args:
            pendingToken (str): Pending token received from the authentication flow
            signature (str): Terms signature hash based on user role

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Error: 401 Invalid pending token
            Error: 403 Authentication restriction
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/access-tokens/accept-terms", data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createAccessToken(self, **kwargs: Unpack[Request_createAccessToken]) -> Response_createAccessToken:
        """Authenticates a user using email/username and password. Returns an access token for API authentication.

        Args:
            emailOrUsername (str): Email address or username of the user
            password (str): Password of the user
            withHttpOnlyToken (bool): Whether to include an HTTP-only authentication cookie

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Error: 401 Invalid credentials
            Error: 403 Authentication restriction
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/access-tokens", data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteAccessToken(self) -> Response_deleteAccessToken:
        """Logs out the current user by deleting the session and access token. Clears HTTP-only cookies if present.

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            Unauthorized: 401 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/access-tokens/me")
        resp.raise_for_status()
        return resp.json()

    async def exchangeForAccessTokenWithOidc(self, **kwargs: Unpack[Request_exchangeForAccessTokenWithOidc]) -> Response_exchangeForAccessTokenWithOidc:
        """Exchanges an OIDC authorization code for an access token. Creates a user if they do not exist.

        Args:
            code (str): Authorization code from OIDC provider
            nonce (str): Nonce value for OIDC security
            withHttpOnlyToken (bool): Whether to include HTTP-only authentication cookie

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Error: 401 OIDC authentication error
            Error: 403 Authentication restriction
            Error: 409 Conflict error
            Error: 422 Missing required values
            Error: 500 OIDC configuration error
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/access-tokens/exchange-with-oidc", data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def revokePendingToken(self, **kwargs: Unpack[Request_revokePendingToken]) -> Response_revokePendingToken:
        """Revokes a pending authentication token and cancels the authentication flow.

        Args:
            pendingToken (str): Pending token to revoke

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/access-tokens/revoke-pending-token", data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def getBoardActions(self, boardId: str, **kwargs: Unpack[Request_getBoardActions]) -> Response_getBoardActions:
        """Retrieves a list of actions (activity history) for a specific board, with pagination support.

        Args:
            boardId (str): ID of the board to get actions for)
            beforeId (str): ID to get actions before (for pagination)) (optional)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        valid_params = ('beforeId',)
        passed_params = {k: v for k, v in kwargs.items() if k in valid_params if isinstance(v, str | int | float)}
        resp = await self.client.get("api/boards/{boardId}/actions".format(**args), params=passed_params)
        resp.raise_for_status()
        return resp.json()

    async def getCardActions(self, cardId: str, **kwargs: Unpack[Request_getCardActions]) -> Response_getCardActions:
        """Retrieves a list of actions (activity history) for a specific card, with pagination support.

        Args:
            cardId (str): ID of the card to get actions for)
            beforeId (str): ID to get actions before (for pagination)) (optional)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        valid_params = ('beforeId',)
        passed_params = {k: v for k, v in kwargs.items() if k in valid_params if isinstance(v, str | int | float)}
        resp = await self.client.get("api/cards/{cardId}/actions".format(**args), params=passed_params)
        resp.raise_for_status()
        return resp.json()

    async def createAttachment(self, cardId: str, **kwargs: Unpack[Request_createAttachment]) -> Response_createAttachment:
        """Creates an attachment on a card. Requires board editor permissions.

        Args:
            cardId (str): ID of the card to create the attachment on)
            type (Literal['file', 'link']): Type of the attachment
            file (str): File to upload
            url (str): URL for the link attachment
            name (str): Name/title of the attachment
            requestId (str): Request ID for tracking

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Error: 422 Upload or validation error
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/cards/{cardId}/attachments".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteAttachment(self, id: str) -> Response_deleteAttachment:
        """Deletes an attachment. Requires board editor permissions.

        Args:
            id (str): ID of the attachment to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/attachments/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateAttachment(self, id: str, **kwargs: Unpack[Request_updateAttachment]) -> Response_updateAttachment:
        """Updates an attachment. Requires board editor permissions.

        Args:
            id (str): ID of the attachment to update)
            name (str): Name/title of the attachment

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/attachments/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createBackgroundImage(self, projectId: str, **kwargs: Unpack[Request_createBackgroundImage]) -> Response_createBackgroundImage:
        """Uploads a background image for a project. Requires project manager permissions.

        Args:
            projectId (str): ID of the project to upload background image for)
            file (str): Background image file (must be an image format)
            requestId (str): Request ID for tracking

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Error: 422 File upload error
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/projects/{projectId}/background-images".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteBackgroundImage(self, id: str) -> Response_deleteBackgroundImage:
        """Deletes a background image. Requires project manager permissions.

        Args:
            id (str): ID of the background image to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/background-images/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def createBaseCustomFieldGroup(self, projectId: str, **kwargs: Unpack[Request_createBaseCustomFieldGroup]) -> Response_createBaseCustomFieldGroup:
        """Creates a base custom field group within a project. Requires project manager permissions.

        Args:
            projectId (str): ID of the project to create the base custom field group in)
            name (str): Name/title of the base custom field group

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/projects/{projectId}/base-custom-field-groups".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteBaseCustomFieldGroup(self, id: str) -> Response_deleteBaseCustomFieldGroup:
        """Deletes a base custom field group. Requires project manager permissions.

        Args:
            id (str): ID of the base custom field group to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/base-custom-field-groups/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateBaseCustomFieldGroup(self, id: str, **kwargs: Unpack[Request_updateBaseCustomFieldGroup]) -> Response_updateBaseCustomFieldGroup:
        """Updates a base custom field group. Requires project manager permissions.

        Args:
            id (str): ID of the base custom field group to update)
            name (str): Name/title of the base custom field group

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/base-custom-field-groups/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createBoardMembership(self, boardId: str, **kwargs: Unpack[Request_createBoardMembership]) -> Response_createBoardMembership:
        """Creates a board membership within a board. Requires project manager permissions.

        Args:
            boardId (str): ID of the board to create the board membership in)
            userId (str): ID of the user who is a member of the board
            role (Literal['editor', 'viewer']): Role of the user in the board
            canComment (bool | None): Whether the user can comment on cards (applies only to viewers)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/boards/{boardId}/board-memberships".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteBoardMembership(self, id: str) -> Response_deleteBoardMembership:
        """Deletes a board membership. Users can remove their own membership, project managers can remove any membership.

        Args:
            id (str): ID of the board membership to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/board-memberships/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateBoardMembership(self, id: str, **kwargs: Unpack[Request_updateBoardMembership]) -> Response_updateBoardMembership:
        """Updates a board membership. Requires project manager permissions.

        Args:
            id (str): ID of the board membership to update)
            role (Literal['editor', 'viewer']): Role of the user in the board
            canComment (bool | None): Whether the user can comment on cards (applies only to viewers)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/board-memberships/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createBoard(self, projectId: str, **kwargs: Unpack[Request_createBoard]) -> Response_createBoard:
        """Creates a board within a project. Supports importing from Trello. Requires project manager permissions.

        Args:
            projectId (str): ID of the project to create the board in)
            position (int): Position of the board within the project
            name (str): Name/title of the board
            importType (Literal['trello']): Type of import
            importFile (str): Import file
            requestId (str): Request ID for tracking

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
            Error: 422 Import file upload error
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/projects/{projectId}/boards".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteBoard(self, id: str) -> Response_deleteBoard:
        """Deletes a board and all its contents (lists, cards, etc.). Requires project manager permissions.

        Args:
            id (str): ID of the board to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/boards/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def getBoard(self, id: str, **kwargs: Unpack[Request_getBoard]) -> Response_getBoard:
        """Retrieves comprehensive board information, including lists, cards, and other related data.

        Args:
            id (str): ID of the board to retrieve)
            subscribe (bool): Whether to subscribe to real-time updates for this board (only for socket connections)) (optional)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        valid_params = ('subscribe',)
        passed_params = {k: v for k, v in kwargs.items() if k in valid_params if isinstance(v, str | int | float)}
        resp = await self.client.get("api/boards/{id}".format(**args), params=passed_params)
        resp.raise_for_status()
        return resp.json()

    async def updateBoard(self, id: str, **kwargs: Unpack[Request_updateBoard]) -> Response_updateBoard:
        """Updates a board. Project managers can update all fields, board members can only subscribe/unsubscribe.

        Args:
            id (str): ID of the board to update)
            position (int): Position of the board within the project
            name (str): Name/title of the board
            defaultView (Literal['kanban', 'grid', 'list']): Default view for the board
            defaultCardType (Literal['project', 'story']): Default card type for new cards
            limitCardTypesToDefaultOne (bool): Whether to limit card types to default one
            alwaysDisplayCardCreator (bool): Whether to always display card creators
            expandTaskListsByDefault (bool): Whether to expand task lists by default
            isSubscribed (bool): Whether the current user is subscribed to the board

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/boards/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createCardLabel(self, cardId: str, **kwargs: Unpack[Request_createCardLabel]) -> Response_createCardLabel:
        """Adds a label to a card. Requires board editor permissions.

        Args:
            cardId (str): ID of the card to add the label to)
            labelId (str): ID of the label to add to the card

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/cards/{cardId}/card-labels".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteCardLabel(self, cardId: str, labelId: str) -> Response_deleteCardLabel:
        """Removes a label from a card. Requires board editor permissions.

        Args:
            cardId (str): ID of the card to remove the label from)
            labelId (str): ID of the label to remove from the card)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/cards/{cardId}/card-labels/labelId:{labelId}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def createCardMembership(self, cardId: str, **kwargs: Unpack[Request_createCardMembership]) -> Response_createCardMembership:
        """Adds a user to a card. Requires board editor permissions.

        Args:
            cardId (str): ID of the card to add the user to)
            userId (str): ID of the card to add the user to

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/cards/{cardId}/card-memberships".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteCardMembership(self, cardId: str, userId: str) -> Response_deleteCardMembership:
        """Removes a user from a card. Requires board editor permissions.

        Args:
            cardId (str): ID of the card to remove the user from)
            userId (str): ID of the user to remove from the card)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/cards/{cardId}/card-memberships/userId:{userId}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def createCard(self, listId: str, **kwargs: Unpack[Request_createCard]) -> Response_createCard:
        """Creates a card within a list. Requires board editor permissions.

        Args:
            listId (str): ID of the list to create the card in)
            type (Literal['project', 'story']): Type of the card
            position (int | None): Position of the card within the list
            name (str): Name/title of the card
            description (str | None): Detailed description of the card
            dueDate (str): Due date for the card
            isDueCompleted (bool | None): Whether the due date is completed
            stopwatch (dict[str, Any] | None): Stopwatch data for time tracking

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/lists/{listId}/cards".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def getCards(self, listId: str, **kwargs: Unpack[Request_getCards]) -> Response_getCards:
        """Retrieves cards from an endless list with filtering, search, and pagination support.

        Args:
            listId (str): ID of the list to get cards from (must be an endless list))
            before (str): Pagination cursor (JSON object with id and listChangedAt)) (optional)
            search (str): Search term to filter cards) (optional)
            filterUserIds (str): Comma-separated user IDs to filter by members) (optional)
            filterLabelIds (str): Comma-separated label IDs to filter by labels) (optional)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        valid_params = ('before', 'search', 'filterUserIds', 'filterLabelIds')
        passed_params = {k: v for k, v in kwargs.items() if k in valid_params if isinstance(v, str | int | float)}
        resp = await self.client.get("api/lists/{listId}/cards".format(**args), params=passed_params)
        resp.raise_for_status()
        return resp.json()

    async def deleteCard(self, id: str) -> Response_deleteCard:
        """Deletes a card and all its contents (tasks, attachments, etc.). Requires board editor permissions.

        Args:
            id (str): ID of the card to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/cards/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def getCard(self, id: str) -> Response_getCard:
        """Retrieves comprehensive card information, including tasks, attachments, and other related data.

        Args:
            id (str): ID of the card to retrieve)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/cards/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateCard(self, id: str, **kwargs: Unpack[Request_updateCard]) -> Response_updateCard:
        """Updates a card. Board editors can update all fields, viewers can only subscribe/unsubscribe.

        Args:
            id (str): ID of the card to update)
            boardId (str): ID of the board to move the card to
            listId (str): ID of the list to move the card to
            coverAttachmentId (str | None): ID of the attachment used as cover
            type (Literal['project', 'story']): Type of the card
            position (int | None): Position of the card within the list
            name (str): Name/title of the card
            description (str | None): Detailed description of the card
            dueDate (str | None): Due date for the card
            isDueCompleted (bool | None): Whether the due date is completed
            stopwatch (dict[str, Any] | None): Stopwatch data for time tracking
            isSubscribed (bool): Whether the current user is subscribed to the card

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/cards/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def duplicateCard(self, id: str, **kwargs: Unpack[Request_duplicateCard]) -> Response_duplicateCard:
        """Creates a duplicate of a card with all its contents (tasks, attachments, etc.). Requires board editor permissions.

        Args:
            id (str): ID of the card to duplicate)
            position (int): Position for the duplicated card within the list
            name (str): Name/title for the duplicated card

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/cards/{id}/duplicate".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def readCardNotifications(self, id: str) -> Response_readCardNotifications:
        """Marks all notifications for a specific card as read for the current user. Requires access to the card.

        Args:
            id (str): ID of the card to mark notifications as read for)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.post("api/cards/{id}/read-notifications".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def createComment(self, cardId: str, **kwargs: Unpack[Request_createComment]) -> Response_createComment:
        """Creates a new comment on a card. Requires board editor permissions or comment permissions.

        Args:
            cardId (str): ID of the card to create the comment on)
            text (str): Content of the comment

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/cards/{cardId}/comments".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def getComments(self, cardId: str, **kwargs: Unpack[Request_getComments]) -> Response_getComments:
        """Retrieves comments for a card with pagination support. Requires access to the card.

        Args:
            cardId (str): ID of the card to retrieve comments for)
            beforeId (str): ID to get comments before (for pagination)) (optional)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        valid_params = ('beforeId',)
        passed_params = {k: v for k, v in kwargs.items() if k in valid_params if isinstance(v, str | int | float)}
        resp = await self.client.get("api/cards/{cardId}/comments".format(**args), params=passed_params)
        resp.raise_for_status()
        return resp.json()

    async def deleteComment(self, id: str) -> Response_deleteComment:
        """Deletes a comment. Can be deleted by the comment author (with comment permissions) or project manager.

        Args:
            id (str): ID of the comment to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/comments/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateComments(self, id: str, **kwargs: Unpack[Request_updateComments]) -> Response_updateComments:
        """Updates a comment. Only the author of the comment can update it.

        Args:
            id (str): ID of the comment to update)
            text (str): Content of the comment

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/comments/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def getConfig(self) -> Response_getConfig:
        """Retrieves the application configuration.
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/config")
        resp.raise_for_status()
        return resp.json()

    async def createBoardCustomFieldGroup(self, boardId: str, **kwargs: Unpack[Request_createBoardCustomFieldGroup]) -> Response_createBoardCustomFieldGroup:
        """Creates a custom field group within a board. Either `baseCustomFieldGroupId` or `name` must be provided. Requires board editor permissions.

        Args:
            boardId (str): ID of the board to create the custom field group in)
            baseCustomFieldGroupId (str): ID of the base custom field group used as a template
            position (int): Position of the custom field group within the board
            name (str | None): Name/title of the custom field group (required if `baseCustomFieldGroupId` is not provided)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/boards/{boardId}/custom-field-groups".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createCardCustomFieldGroup(self, cardId: str, **kwargs: Unpack[Request_createCardCustomFieldGroup]) -> Response_createCardCustomFieldGroup:
        """Creates a custom field group within a card. Either `baseCustomFieldGroupId` or `name` must be provided. Requires board editor permissions.

        Args:
            cardId (str): ID of the card to create the custom field group in)
            baseCustomFieldGroupId (str): ID of the base custom field group used as a template
            position (int): Position of the custom field group within the card
            name (str | None): Name/title of the custom field group (required if `baseCustomFieldGroupId` is not provided)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/cards/{cardId}/custom-field-groups".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteCustomFieldGroup(self, id: str) -> Response_deleteCustomFieldGroup:
        """Deletes a custom field group. Requires board editor permissions.

        Args:
            id (str): ID of the custom field group to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/custom-field-groups/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def getCustomFieldGroup(self, id: str) -> Response_getCustomFieldGroup:
        """Retrieves comprehensive custom field group information, including fields and values. Requires access to the board/card.

        Args:
            id (str): ID of the custom field group to retrieve)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/custom-field-groups/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateCustomFieldGroup(self, id: str, **kwargs: Unpack[Request_updateCustomFieldGroup]) -> Response_updateCustomFieldGroup:
        """Updates a custom field group. Supports both board-wide and card-specific groups. Requires board editor permissions.

        Args:
            id (str): ID of the custom field group to update)
            position (int): Position of the custom field group within the board/card
            name (str | None): Name/title of the custom field group

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/custom-field-groups/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def updateCustomFieldValue(self, cardId: str, customFieldGroupId: str, customFieldId: str, **kwargs: Unpack[Request_updateCustomFieldValue]) -> Response_updateCustomFieldValue:
        """Creates or updates a custom field value for a card. Requires board editor permissions.

        Args:
            cardId (str): ID of the card to set the custom field value for)
            customFieldGroupId (str): ID of the custom field group the value belongs to)
            customFieldId (str): ID of the custom field the value belongs to)
            content (str): Content/value of the custom field

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/cards/{cardId}/custom-field-values/customFieldGroupId:{customFieldGroupId}:customFieldId:${customFieldId}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteCustomFieldValue(self, cardId: str, customFieldGroupId: str, customFieldId: str) -> Response_deleteCustomFieldValue:
        """Deletes a custom field value for a specific card. Requires board editor permissions.

        Args:
            cardId (str): ID of the card to delete the custom field value from)
            customFieldGroupId (str): ID of the custom field group the value belongs to)
            customFieldId (str): ID of the custom field the value belongs to)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/cards/{cardId}/custom-field-value/customFieldGroupId:{customFieldGroupId}:customFieldId:${customFieldId}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def createCustomFieldInBaseGroup(self, baseCustomFieldGroupId: str, **kwargs: Unpack[Request_createCustomFieldInBaseGroup]) -> Response_createCustomFieldInBaseGroup:
        """Creates a custom field within a base custom field group. Requires project manager permissions.

        Args:
            baseCustomFieldGroupId (str): ID of the base custom field group to create the custom field in)
            position (int): Position of the custom field within the group
            name (str): Name/title of the custom field
            showOnFrontOfCard (bool): Whether to show the field on the front of cards

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/base-custom-field-groups/{baseCustomFieldGroupId}/custom-fields".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createCustomFieldInGroup(self, customFieldGroupId: str, **kwargs: Unpack[Request_createCustomFieldInGroup]) -> Response_createCustomFieldInGroup:
        """Creates a custom field within a custom field group. Requires board editor permissions.

        Args:
            customFieldGroupId (str): ID of the custom field group to create the custom field in)
            position (int): Position of the custom field within the group
            name (str): Name/title of the custom field
            showOnFrontOfCard (bool): Whether to show the field on the front of cards

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/custom-field-groups/{customFieldGroupId}/custom-fields".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteCustomField(self, id: str) -> Response_deleteCustomField:
        """Deletes a custom field. Can delete the in base custom field group (requires project manager permissions) or the custom field group (requires board editor permissions).

        Args:
            id (str): ID of the custom field to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/custom-fields/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateCustomField(self, id: str, **kwargs: Unpack[Request_updateCustomField]) -> Response_updateCustomField:
        """Updates a custom field. Can update in the base custom field group (requires project manager permissions) or the custom field group (requires board editor permissions).

        Args:
            id (str): ID of the custom field to update)
            position (int): Position of the custom field within the group
            name (str): Name/title of the custom field
            showOnFrontOfCard (bool): Whether to show the field on the front of cards

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/custom-fields/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createLabel(self, boardId: str, **kwargs: Unpack[Request_createLabel]) -> Response_createLabel:
        """Creates a label within a board. Requires board editor permissions.

        Args:
            boardId (str): ID of the board to create the label in)
            position (int): Position of the label within the board
            name (str | None): Name/title of the label
            color (Literal['muddy-grey', 'autumn-leafs', 'morning-sky', 'antique-blue', 'egg-yellow', 'desert-sand', 'dark-granite', 'fresh-salad', 'lagoon-blue', 'midnight-blue', 'light-orange', 'pumpkin-orange', 'light-concrete', 'sunny-grass', 'navy-blue', 'lilac-eyes', 'apricot-red', 'orange-peel', 'silver-glint', 'bright-moss', 'deep-ocean', 'summer-sky', 'berry-red', 'light-cocoa', 'grey-stone', 'tank-green', 'coral-green', 'sugar-plum', 'pink-tulip', 'shady-rust', 'wet-rock', 'wet-moss', 'turquoise-sea', 'lavender-fields', 'piggy-red', 'light-mud', 'gun-metal', 'modern-green', 'french-coast', 'sweet-lilac', 'red-burgundy', 'pirate-gold']): Color of the label

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/boards/{boardId}/labels".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteLabel(self, id: str) -> Response_deleteLabel:
        """Deletes a label. Requires board editor permissions.

        Args:
            id (str): ID of the label to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/labels/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateLabel(self, id: str, **kwargs: Unpack[Request_updateLabel]) -> Response_updateLabel:
        """Updates a label. Requires board editor permissions.

        Args:
            id (str): ID of the label to update)
            position (int): Position of the label within the board
            name (str | None): Name/title of the label
            color (Literal['muddy-grey', 'autumn-leafs', 'morning-sky', 'antique-blue', 'egg-yellow', 'desert-sand', 'dark-granite', 'fresh-salad', 'lagoon-blue', 'midnight-blue', 'light-orange', 'pumpkin-orange', 'light-concrete', 'sunny-grass', 'navy-blue', 'lilac-eyes', 'apricot-red', 'orange-peel', 'silver-glint', 'bright-moss', 'deep-ocean', 'summer-sky', 'berry-red', 'light-cocoa', 'grey-stone', 'tank-green', 'coral-green', 'sugar-plum', 'pink-tulip', 'shady-rust', 'wet-rock', 'wet-moss', 'turquoise-sea', 'lavender-fields', 'piggy-red', 'light-mud', 'gun-metal', 'modern-green', 'french-coast', 'sweet-lilac', 'red-burgundy', 'pirate-gold']): Color of the label

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/labels/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def clearList(self, id: str) -> Response_clearList:
        """Deletes all cards from a list. Only works with trash-type lists. Requires project manager or board editor permissions.

        Args:
            id (str): ID of the list to clear (must be a trash-type list))

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.post("api/lists/{id}/clear".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def createList(self, boardId: str, **kwargs: Unpack[Request_createList]) -> Response_createList:
        """Creates a list within a board. Requires board editor permissions.

        Args:
            boardId (str): ID of the board to create the list in)
            type (Literal['active', 'closed']): Type/status of the list
            position (int): Position of the list within the board
            name (str): Name/title of the list

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/boards/{boardId}/lists".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteList(self, id: str) -> Response_deleteList:
        """Deletes a list and moves its cards to a trash list. Can only delete finite lists. Requires board editor permissions.

        Args:
            id (str): ID of the list to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/lists/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def getList(self, id: str) -> Response_getList:
        """Retrieves comprehensive list information, including cards, attachments, and other related data. Requires access to the board.

        Args:
            id (str): ID of the list to retrieve)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/lists/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateList(self, id: str, **kwargs: Unpack[Request_updateList]) -> Response_updateList:
        """Updates a list. Can move lists between boards. Requires board editor permissions.

        Args:
            id (str): ID of the list to update)
            boardId (str): ID of the board to move list to
            type (Literal['active', 'closed']): Type/status of the list
            position (int): Position of the list within the board
            name (str): Name/title of the list
            color (Literal['berry-red', 'pumpkin-orange', 'lagoon-blue', 'pink-tulip', 'light-mud', 'orange-peel', 'bright-moss', 'antique-blue', 'dark-granite', 'turquoise-sea'] | None): Color for the list

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/lists/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def moveListCards(self, id: str, **kwargs: Unpack[Request_moveListCards]) -> Response_moveListCards:
        """Moves all cards from a closed list to an archive list. Requires board editor permissions.

        Args:
            id (str): ID of the source list (must be a closed-type list))
            listId (str): ID of the target list (must be an archive-type list)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/lists/{id}/move-cards".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def sortList(self, id: str, **kwargs: Unpack[Request_sortList]) -> Response_sortList:
        """Sorts all cards within a list. Requires board editor permissions.

        Args:
            id (str): ID of the list to sort)
            fieldName (Literal['name', 'dueDate', 'createdAt']): Field to sort cards by
            order (Literal['asc', 'desc']): Sorting order

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/lists/{id}/sort".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createBoardNotificationService(self, boardId: str, **kwargs: Unpack[Request_createBoardNotificationService]) -> Response_createBoardNotificationService:
        """Creates a new notification service for a board. Requires project manager permissions.

        Args:
            boardId (str): ID of the board to create notification service for)
            url (str): URL endpoint for notifications
            format (Literal['text', 'markdown', 'html']): Format for notification messages

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/boards/{boardId}/notification-services".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createUserNotificationService(self, userId: str, **kwargs: Unpack[Request_createUserNotificationService]) -> Response_createUserNotificationService:
        """Creates a new notification service for a user. Users can only create services for themselves.

        Args:
            userId (str): ID of the user to create notification service for (must be the current user))
            url (str): URL endpoint for notifications
            format (Literal['text', 'markdown', 'html']): Format for notification messages

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/users/{userId}/notification-services".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteNotificationService(self, id: str) -> Response_deleteNotificationService:
        """Deletes a notification service. Users can delete their own services, project managers can delete board services.

        Args:
            id (str): ID of the notification service to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/notification-services/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateNotificationService(self, id: str, **kwargs: Unpack[Request_updateNotificationService]) -> Response_updateNotificationService:
        """Updates a notification service. Users can update their own services, project managers can update board services.

        Args:
            id (str): ID of the notification service to update)
            url (str): URL endpoint for notifications
            format (Literal['text', 'markdown', 'html']): Format for notification messages

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/notification-services/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def testNotificationService(self, id: str) -> Response_testNotificationService:
        """Sends a test notification to verify the notification service is working. Users can test their own services, project managers can test board services.

        Args:
            id (str): ID of the notification service to test)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.post("api/notification-services/{id}/test".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def getNotifications(self) -> Response_getNotifications:
        """Retrieves all unread notifications for the current user, including creator users.

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/notifications")
        resp.raise_for_status()
        return resp.json()

    async def readAllNotifications(self) -> Response_readAllNotifications:
        """Marks all notifications for the current user as read.

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.post("api/notifications/read-all")
        resp.raise_for_status()
        return resp.json()

    async def getNotification(self, id: str) -> Response_getNotification:
        """Retrieves notification, including creator users. Users can only access their own notifications.

        Args:
            id (str): ID of the notification to retrieve)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/notifications/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateNotification(self, id: str, **kwargs: Unpack[Request_updateNotification]) -> Response_updateNotification:
        """Updates a notification. Users can only update their own notifications.

        Args:
            id (str): ID of the notification to update)
            isRead (bool): Whether the notification has been read

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/notifications/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createProjectManager(self, projectId: str, **kwargs: Unpack[Request_createProjectManager]) -> Response_createProjectManager:
        """Creates a project manager within a project. Requires admin privileges for shared projects or existing project manager permissions. The user must be an admin or project owner.

        Args:
            projectId (str): ID of the project to create the project manager in)
            userId (str): ID of the user who is assigned as project manager

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Conflict: 409 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/projects/{projectId}/project-managers".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteProjectManager(self, id: str) -> Response_deleteProjectManager:
        """Deletes a project manager. Requires admin privileges for shared projects or existing project manager permissions. Cannot remove the last project manager.

        Args:
            id (str): ID of the project manager to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/project-managers/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def createProject(self, **kwargs: Unpack[Request_createProject]) -> Response_createProject:
        """Creates a project. The current user automatically becomes a project manager.

        Args:
            type (Literal['public', 'private']): Type of the project
            name (str): Name/title of the project
            description (str | None): Detailed description of the project

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/projects", data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def getProjects(self) -> Response_getProjects:
        """Retrieves all projects the current user has access to, including managed projects, membership projects, and shared projects (for admins).

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/projects")
        resp.raise_for_status()
        return resp.json()

    async def deleteProject(self, id: str) -> Response_deleteProject:
        """Deletes a project. The project must not have any boards. Requires project manager permissions.

        Args:
            id (str): ID of the project to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/projects/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def getProject(self, id: str) -> Response_getProject:
        """Retrieves comprehensive project information, including boards, board memberships, and other related data.

        Args:
            id (str): ID of the project to retrieve)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/projects/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateProject(self, id: str, **kwargs: Unpack[Request_updateProject]) -> Response_updateProject:
        """Updates a project. Accessible fields depend on user permissions.

        Args:
            id (str): ID of the project to update)
            ownerProjectManagerId (str | None): ID of the project manager who owns the project
            backgroundImageId (str | None): ID of the background image used as background
            name (str): Name/title of the project
            description (str | None): Detailed description of the project
            backgroundType (Literal['gradient', 'image'] | None): Type of background for the project
            backgroundGradient (Literal['old-lime', 'ocean-dive', 'tzepesch-style', 'jungle-mesh', 'strawberry-dust', 'purple-rose', 'sun-scream', 'warm-rust', 'sky-change', 'green-eyes', 'blue-xchange', 'blood-orange', 'sour-peel', 'green-ninja', 'algae-green', 'coral-reef', 'steel-grey', 'heat-waves', 'velvet-lounge', 'purple-rain', 'blue-steel', 'blueish-curve', 'prism-light', 'green-mist', 'red-curtain'] | None): Gradient background for the project
            isHidden (bool): Whether the project is hidden
            isFavorite (bool): Whether the project is marked as favorite by the current user

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Conflict: 409 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/projects/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createTaskList(self, cardId: str, **kwargs: Unpack[Request_createTaskList]) -> Response_createTaskList:
        """Creates a task list within a card. Requires board editor permissions.

        Args:
            cardId (str): ID of the card to create task list in)
            position (int): Position of the task list within the card
            name (str): Name/title of the task list
            showOnFrontOfCard (bool): Whether to show the task list on the front of the card
            hideCompletedTasks (bool): Whether to hide completed tasks

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/cards/{cardId}/task-lists".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteTaskList(self, id: str) -> Response_deleteTaskList:
        """Deletes a task list and all its tasks. Requires board editor permissions.

        Args:
            id (str): ID of the task list to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/task-lists/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def getTaskList(self, id: str) -> Response_getTaskList:
        """Retrieves task list information, including tasks. Requires access to the card.

        Args:
            id (str): ID of the task list to retrieve)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/task-lists/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateTaskList(self, id: str, **kwargs: Unpack[Request_updateTaskList]) -> Response_updateTaskList:
        """Updates a task list. Requires board editor permissions.

        Args:
            id (str): ID of the task list to update)
            position (int): Position of the task list within the card
            name (str): Name/title of the task list
            showOnFrontOfCard (bool): Whether to show the task list on the front of the card
            hideCompletedTasks (bool): Whether to hide completed tasks

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/task-lists/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createTask(self, taskListId: str, **kwargs: Unpack[Request_createTask]) -> Response_createTask:
        """Creates a task within a task list. Either `linkedCardId` or `name` must be provided. Requires board editor permissions.

        Args:
            taskListId (str): ID of the task list to create task in)
            linkedCardId (str): ID of the card linked to the task
            position (int): Position of the task within the task list
            name (str | None): Name/title of the task (required if `linkedCardId` is not provided)
            isCompleted (bool): Whether the task is completed

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/task-lists/{taskListId}/tasks".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def deleteTask(self, id: str) -> Response_deleteTask:
        """Deletes a task. Requires board editor permissions.

        Args:
            id (str): ID of the task to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/tasks/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateTask(self, id: str, **kwargs: Unpack[Request_updateTask]) -> Response_updateTask:
        """Updates a task. Linked card tasks have limited update options. Requires board editor permissions.

        Args:
            id (str): ID of the task to update)
            taskListId (str): ID of the task list to move the task to
            assigneeUserId (str | None): ID of the user assigned to the task (null to unassign)
            position (int): Position of the task within the task list
            name (str): Name/title of the task
            isCompleted (bool): Whether the task is completed

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/tasks/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def getTerms(self, type: Literal['general', 'extended'], **kwargs: Unpack[Request_getTerms]) -> Response_getTerms:
        """Retrieves terms and conditions in the specified language.

        Args:
            type (Literal['general', 'extended']): Type of terms to retrieve)
            language (Literal['de-DE', 'en-US']): Language code for terms localization) (optional)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        valid_params = ('language',)
        passed_params = {k: v for k, v in kwargs.items() if k in valid_params if isinstance(v, str | int | float)}
        resp = await self.client.get("api/terms/{type}".format(**args), params=passed_params)
        resp.raise_for_status()
        return resp.json()

    async def createUser(self, **kwargs: Unpack[Request_createUser]) -> Response_createUser:
        """Creates a user account. Requires admin privileges.

        Args:
            email (str): Email address for login and notifications
            password (str): Password for user authentication (must meet password requirements)
            role (Literal['admin', 'projectOwner', 'boardUser']): User role defining access permissions
            name (str): Full display name of the user
            username (str | None): Unique username for user identification
            phone (str | None): Contact phone number
            organization (str | None): Organization or company name
            language (Literal['ar-YE', 'bg-BG', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US', 'es-ES', 'et-EE', 'fa-IR', 'fi-FI', 'fr-FR', 'hu-HU', 'id-ID', 'it-IT', 'ja-JP', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'sk-SK', 'sr-Cyrl-RS', 'sr-Latn-RS', 'sv-SE', 'tr-TR', 'uk-UA', 'uz-UZ', 'zh-CN', 'zh-TW'] | None): Preferred language for user interface and notifications
            subscribeToOwnCards (bool): Whether the user subscribes to their own cards
            subscribeToCardWhenCommenting (bool): Whether the user subscribes to cards when commenting
            turnOffRecentCardHighlighting (bool): Whether recent card highlighting is disabled

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/users", data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def getUsers(self) -> Response_getUsers:
        """Retrieves a list of all users. Requires admin or project owner privileges.

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/users")
        resp.raise_for_status()
        return resp.json()

    async def deleteUser(self, id: str) -> Response_deleteUser:
        """Deletes a user account. Cannot delete the default admin user. Requires admin privileges.

        Args:
            id (str): ID of the user to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/users/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def getUser(self, id: str, **kwargs: Unpack[Request_getUser]) -> Response_getUser:
        """Retrieves a user. Use 'me' as ID to get the current user.

        Args:
            id (str): ID of the user or 'me' for current user)
            subscribe (bool): Whether to subscribe to real-time updates for this user (only for socket connections)) (optional)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        valid_params = ('subscribe',)
        passed_params = {k: v for k, v in kwargs.items() if k in valid_params if isinstance(v, str | int | float)}
        resp = await self.client.get("api/users/{id}".format(**args), params=passed_params)
        resp.raise_for_status()
        return resp.json()

    async def updateUser(self, id: str, **kwargs: Unpack[Request_updateUser]) -> Response_updateUser:
        """Updates a user. Users can update their own profile, admins can update any user.

        Args:
            id (str): ID of the user to update)
            role (Literal['admin', 'projectOwner', 'boardUser']): User role defining access permissions
            name (str): Full display name of the user
            avatar (dict[str, Any] | None): Avatar of the user (only null value to remove avatar)
            phone (str | None): Contact phone number
            organization (str | None): Organization or company name
            language (Literal['ar-YE', 'bg-BG', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US', 'es-ES', 'et-EE', 'fa-IR', 'fi-FI', 'fr-FR', 'hu-HU', 'id-ID', 'it-IT', 'ja-JP', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'sk-SK', 'sr-Cyrl-RS', 'sr-Latn-RS', 'sv-SE', 'tr-TR', 'uk-UA', 'uz-UZ', 'zh-CN', 'zh-TW'] | None): Preferred language for user interface and notifications
            subscribeToOwnCards (bool): Whether the user subscribes to their own cards
            subscribeToCardWhenCommenting (bool): Whether the user subscribes to cards when commenting
            turnOffRecentCardHighlighting (bool): Whether recent card highlighting is disabled
            enableFavoritesByDefault (bool): Whether favorites are enabled by default
            defaultEditorMode (Literal['wysiwyg', 'markup']): Default markdown editor mode
            defaultHomeView (Literal['gridProjects', 'groupedProjects']): Default view mode for the home page
            defaultProjectsOrder (Literal['byDefault', 'alphabetically', 'byCreationTime']): Default sort order for projects display
            isDeactivated (bool): Whether the user account is deactivated and cannot log in (for admins)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/users/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def updateUserAvatar(self, id: str, **kwargs: Unpack[Request_updateUserAvatar]) -> Response_updateUserAvatar:
        """Updates a user's avatar image. Users can update their own avatar, admins can update any user's avatar.

        Args:
            id (str): ID of the user whose avatar to update)
            file (str): Avatar image file (must be an image format)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
            UnprocessableEntity: 422 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/users/{id}/avatar".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def updateUserEmail(self, id: str, **kwargs: Unpack[Request_updateUserEmail]) -> Response_updateUserEmail:
        """Updates a user's email address. Users must provide current password when updating their own email. Admins can update any user's email without a password.

        Args:
            id (str): ID of the user whose email to update)
            email (str): Email address for login and notifications
            currentPassword (str): Current password (required when updating own email)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/users/{id}/email".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def updateUserPassword(self, id: str, **kwargs: Unpack[Request_updateUserPassword]) -> Response_updateUserPassword:
        """Updates a user's password. Users must provide a current password when updating their own password. Admins can update any user's password without the current password. Returns a new access token when updating own password.

        Args:
            id (str): ID of the user whose password to update)
            password (str): Password (must meet password requirements)
            currentPassword (str): Current password (required when updating own password)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/users/{id}/password".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def updateUserUsername(self, id: str, **kwargs: Unpack[Request_updateUserUsername]) -> Response_updateUserUsername:
        """Updates a user's username. Users must provide a current password when updating their own username (unless they are SSO users with `oidcIgnoreUsername` enabled). Admins can update any user's username without the current password.

        Args:
            id (str): ID of the user whose username to update)
            username (str | None): Unique username for user identification
            currentPassword (str): Current password (required when updating own username)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Forbidden: 403 
            NotFound: 404 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/users/{id}/username".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def createWebhook(self, **kwargs: Unpack[Request_createWebhook]) -> Response_createWebhook:
        """Creates a webhook. Requires admin privileges.

        Args:
            name (str): Name/title of the webhook
            url (str): URL endpoint for the webhook
            accessToken (str | None): Access token for webhook authentication
            events (str | None): Comma-separated list of events that trigger the webhook
            excludedEvents (str | None): Comma-separated list of events excluded from the webhook

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            Conflict: 409 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.post("api/webhooks", data=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def getWebhooks(self) -> Response_getWebhooks:
        """Retrieves a list of all configured webhooks. Requires admin privileges.

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.get("api/webhooks")
        resp.raise_for_status()
        return resp.json()

    async def deleteWebhook(self, id: str) -> Response_deleteWebhook:
        """Deletes a webhook. Requires admin privileges.

        Args:
            id (str): ID of the webhook to delete)

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        resp = await self.client.delete("api/webhooks/{id}".format(**args))
        resp.raise_for_status()
        return resp.json()

    async def updateWebhook(self, id: str, **kwargs: Unpack[Request_updateWebhook]) -> Response_updateWebhook:
        """Updates a webhook. Requires admin privileges.

        Args:
            id (str): ID of the webhook to update)
            name (str): Name/title of the webhook
            url (str): URL endpoint for the webhook
            accessToken (str | None): Access token for webhook authentication
            events (str | None): Comma-separated list of events that trigger the webhook
            excludedEvents (str | None): Comma-separated list of events excluded from the webhook

        Note:
            All status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). 
            Planka internal status errors are included here for disambiguation

        Raises:
            ValidationError: 400 
            Unauthorized: 401 
            NotFound: 404 
        """
        args = locals().copy()
        args.pop('self')
        kwargs = args.pop('kwargs')
        resp = await self.client.patch("api/webhooks/{id}".format(**args), data=kwargs)
        resp.raise_for_status()
        return resp.json()
