from utils.handlers import JSONHandler, JSONResponse
from typing import Literal, TypeAlias

RequestType: TypeAlias = Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE']

class Route:
    """Wraps a JSONHandler method with a specific HTTP method and endpoint.
    On call, it delegates the request to the wrapped method.
    
    Usage:
    >>> route = Route('GET', '/api/projects', handler)
    >>> route()
    <JSONResponse>
    """
    def __init__(self, method: RequestType, endpoint: str, handler: JSONHandler):
        self.handler = handler
        self.method = method
        self.endpoint = endpoint

    @property
    def url(self):
        return self.handler.base_url + self.endpoint
    
    def __call__(self, **data) -> JSONResponse:
        match self.method:
            case 'GET':
                with self.handler.endpoint_as(self.endpoint):
                    return self.handler.get()
            case 'POST':
                with self.handler.endpoint_as(self.endpoint):
                    return self.handler.post(data)
            case 'PATCH':
                with self.handler.endpoint_as(self.endpoint):
                    return self.handler.patch(data)
            case 'PUT':
                with self.handler.endpoint_as(self.endpoint):
                    return self.handler.put(data)
            case 'DELETE':
                with self.handler.endpoint_as(self.endpoint):
                    return self.handler.delete()
            case _:
                raise ValueError(f'Invalid method: {self.method}, must be one of GET, POST, PATCH, PUT, DELETE')

    def __repr__(self):
        return f'<Route {self.method} {self.endpoint} for {self.handler}>'
    
    def __iter__(self):
        if not self.method == 'GET':
            raise ValueError('Only GET routes can be iterated')
        return iter(self()['items'])

ROUTES = {

    # GET
    'index': ('GET', '/*'),
    'boards_show': ('GET', '/api/boards/{id}'),
    'actions_index': ('GET', '/api/cards/{cardId}/actions'),
    'cards_show': ('GET', '/api/cards/{id}'),
    'show_config': ('GET', '/api/config'),
    'notifications_index': ('GET', '/api/notifications'),
    'notifications_show': ('GET', '/api/notifications/{id}'),
    'projects_index': ('GET', '/api/projects'),
    'projects_show': ('GET', '/api/projects/{id}'),
    'users_index': ('GET', '/api/users'),
    'users_show': ('GET', '/api/users/{id}'),
    'attachments_download': ('GET', '/attachments/{id}/download/{filename}'),
    'attachments_download_thumbnail': ('GET', '/attachments/{id}/download/thumbnails/cover-256.{extension}'),
    'project_background_images': ('GET', '/project-background-images/*'),
    'user_avatars': ('GET', '/user-avatars/*'),

    # POST
    'access_tokens_create': ('POST', '/api/access-tokens'),
    'exchange_using_oidc': ('POST', '/api/access-tokens/exchange-using-oidc'),
    'labels_create': ('POST', '/api/boards/{boardId}/labels'),
    'lists_create': ('POST', '/api/boards/{boardId}/lists'),
    'board_memberships_create': ('POST', '/api/boards/{boardId}/memberships'),
    'attachments_create': ('POST', '/api/cards/{cardId}/attachments'),
    'comment_actions_create': ('POST', '/api/cards/{cardId}/comment-actions'),
    'card_labels_create': ('POST', '/api/cards/{cardId}/labels'),
    'card_memberships_create': ('POST', '/api/cards/{cardId}/memberships'),
    'tasks_create': ('POST', '/api/cards/{cardId}/tasks'),
    'cards_duplicate': ('POST', '/api/cards/{id}/duplicate'),
    'lists_sort': ('POST', '/api/lists/{id}/sort'),
    'cards_create': ('POST', '/api/lists/{id}/cards'),
    'projects_create': ('POST', '/api/projects'),
    'projects_update_background_image': ('POST', '/api/projects/{id}/background-image'),
    'boards_create': ('POST', '/api/projects/{projectId}/boards'),
    'project_managers_create': ('POST', '/api/projects/{projectId}/managers'),
    'users_create': ('POST', '/api/users'),
    'users_update_avatar': ('POST', '/api/users/{id}/avatar'),

    # PUT
    'attachments_update': ('PUT', '/api/attachments/{id}'),
    'board_memberships_update': ('PUT', '/api/board-memberships/{id}'),
    'boards_update': ('PUT', '/api/boards/{id}'),
    'cards_update': ('PUT', '/api/cards/{id}'),
    'comment_actions_update': ('PUT', '/api/comment-actions/{id}'),
    'labels_update': ('PUT', '/api/labels/{id}'),
    'lists_update': ('PUT', '/api/lists/{id}'),
    'notifications_update': ('PUT', '/api/notifications/{ids}'),
    'projects_update': ('PUT', '/api/projects/{id}'),
    'tasks_update': ('PUT', '/api/tasks/{id}'),
    'users_update': ('PUT', '/api/users/{id}'),
    'users_update_email': ('PUT', '/api/users/{id}/email'),
    'users_update_password': ('PUT', '/api/users/{id}/password'),
    'users_update_username': ('PUT', '/api/users/{id}/username'),

    # PATCH
    'attachments_update': ('PATCH', '/api/attachments/{id}'),
    'board_memberships_update': ('PATCH', '/api/board-memberships/{id}'),
    'boards_update': ('PATCH', '/api/boards/{id}'),
    'cards_update': ('PATCH', '/api/cards/{id}'),
    'comment_actions_update': ('PATCH', '/api/comment-actions/{id}'),
    'labels_update': ('PATCH', '/api/labels/{id}'),
    'lists_update': ('PATCH', '/api/lists/{id}'),
    'notifications_update': ('PATCH', '/api/notifications/{ids}'),
    'projects_update': ('PATCH', '/api/projects/{id}'),
    'tasks_update': ('PATCH', '/api/tasks/{id}'),
    'users_update': ('PATCH', '/api/users/{id}'),
    'users_update_email': ('PATCH', '/api/users/{id}/email'),
    'users_update_password': ('PATCH', '/api/users/{id}/password'),
    'users_update_username': ('PATCH', '/api/users/{id}/username'),

    # DELETE
    'access_tokens_delete': ('DELETE', '/api/access-tokens/me'),
    'attachments_delete': ('DELETE', '/api/attachments/{id}'),
    'board_memberships_delete': ('DELETE', '/api/board-memberships/{id}'),
    'boards_delete': ('DELETE', '/api/boards/{id}'),
    'card_labels_delete': ('DELETE', '/api/cards/{cardId}/labels/{labelId}'),
    'card_memberships_delete': ('DELETE', '/api/cards/{cardId}/memberships'),
    'cards_delete': ('DELETE', '/api/cards/{id}'),
    'comment_actions_delete': ('DELETE', '/api/comment-actions/{id}'),
    'labels_delete': ('DELETE', '/api/labels/{id}'),
    'lists_delete': ('DELETE', '/api/lists/{id}'),
    'project_managers_delete': ('DELETE', '/api/project-managers/{id}'),
    'projects_delete': ('DELETE', '/api/projects/{id}'),
    'tasks_delete': ('DELETE', '/api/tasks/{id}'),
    'users_delete': ('DELETE', '/api/users/{id}'),
}

class Routes:
    """Container for all routes in the Planka API.
    Each method returns a Route object that can be called to make a request.
    
    Usage:
    >>> routes = Routes(handler)
    >>> route = routes.index()
    >>> route()
    <JSONResponse>

    >>> update_card = routes.cards_update(1)
    >>> update_card(name='Updated name')
    <JSONResponse>
    """
    def __init__(self, handler: JSONHandler) -> None:
        self.handler = handler
    
    def index(self) -> Route:
        route = Route(*ROUTES['index'], self.handler)
        return route


    def boards_show(self, id: int) -> Route:
        route = Route(*ROUTES['boards_show'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def actions_index(self, cardId: int) -> Route:
        route = Route(*ROUTES['actions_index'], self.handler)
        route.endpoint = route.endpoint.format(cardId=cardId)
        return route

    def cards_show(self, id: int) -> Route:
        route = Route(*ROUTES['cards_show'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def show_config(self) -> Route:
        route = Route(*ROUTES['show_config'], self.handler)
        return route

    def notifications_index(self) -> Route:
        route = Route(*ROUTES['notifications_index'], self.handler)
        return route

    def notifications_show(self, id: int) -> Route:
        route = Route(*ROUTES['notifications_show'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def projects_index(self) -> Route:
        route = Route(*ROUTES['projects_index'], self.handler)
        return route

    def projects_show(self, id: int) -> Route:
        route = Route(*ROUTES['projects_show'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_index(self) -> Route:
        route = Route(*ROUTES['users_index'], self.handler)
        return route

    def users_show(self, id: int) -> Route:
        route = Route(*ROUTES['users_show'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def attachments_download(self, id: int, filename: str) -> Route:
        route = Route(*ROUTES['attachments_download'], self.handler)
        route.endpoint = route.endpoint.format(id=id, filename=filename)
        return route

    def attachments_download_thumbnail(self, id: int, extension: str) -> Route:
        route = Route(*ROUTES['attachments_download_thumbnail'], self.handler)
        route.endpoint = route.endpoint.format(id=id, extension=extension)
        return route

    def project_background_images(self) -> Route:
        route = Route(*ROUTES['project_background_images'], self.handler)
        return route

    def user_avatars(self) -> Route:
        route = Route(*ROUTES['user_avatars'], self.handler)
        return route

    def access_tokens_create(self) -> Route:
        route = Route(*ROUTES['access_tokens_create'], self.handler)
        return route

    def exchange_using_oidc(self) -> Route:
        route = Route(*ROUTES['exchange_using_oidc'], self.handler)
        return route

    def labels_create(self, boardId: int) -> Route:
        route = Route(*ROUTES['labels_create'], self.handler)
        route.endpoint = route.endpoint.format(boardId=boardId)
        return route

    def lists_create(self, boardId: int) -> Route:
        route = Route(*ROUTES['lists_create'], self.handler)
        route.endpoint = route.endpoint.format(boardId=boardId)
        return route

    def board_memberships_create(self, boardId: int) -> Route:
        route = Route(*ROUTES['board_memberships_create'], self.handler)
        route.endpoint = route.endpoint.format(boardId=boardId)
        return route

    def attachments_create(self, cardId: int) -> Route:
        route = Route(*ROUTES['attachments_create'], self.handler)
        route.endpoint = route.endpoint.format(cardId=cardId)
        return route

    def comment_actions_create(self, cardId: int) -> Route:
        route = Route(*ROUTES['comment_actions_create'], self.handler)
        route.endpoint = route.endpoint.format(cardId=cardId)
        return route

    def card_labels_create(self, cardId: int) -> Route:
        route = Route(*ROUTES['card_labels_create'], self.handler)
        route.endpoint = route.endpoint.format(cardId=cardId)
        return route

    def card_memberships_create(self, cardId: int) -> Route:
        route = Route(*ROUTES['card_memberships_create'], self.handler)
        route.endpoint = route.endpoint.format(cardId=cardId)
        return route

    def tasks_create(self, cardId: int) -> Route:
        route = Route(*ROUTES['tasks_create'], self.handler)
        route.endpoint = route.endpoint.format(cardId=cardId)
        return route

    def cards_duplicate(self, id: int) -> Route:
        route = Route(*ROUTES['cards_duplicate'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def lists_sort(self, id: int) -> Route:
        route = Route(*ROUTES['lists_sort'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def cards_create(self, id: int) -> Route:
        route = Route(*ROUTES['cards_create'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def projects_create(self) -> Route:
        route = Route(*ROUTES['projects_create'], self.handler)
        return route

    def projects_update_background_image(self, id: int) -> Route:
        route = Route(*ROUTES['projects_update_background_image'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def boards_create(self, projectId: int) -> Route:
        route = Route(*ROUTES['boards_create'], self.handler)
        route.endpoint = route.endpoint.format(projectId=projectId)
        return route

    def project_managers_create(self, projectId: int) -> Route:
        route = Route(*ROUTES['project_managers_create'], self.handler)
        route.endpoint = route.endpoint.format(projectId=projectId)
        return route

    def users_create(self) -> Route:
        route = Route(*ROUTES['users_create'], self.handler)
        return route

    def users_update_avatar(self, id: int) -> Route:
        route = Route(*ROUTES['users_update_avatar'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def attachments_update(self, id: int) -> Route:
        route = Route(*ROUTES['attachments_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def board_memberships_update(self, id: int) -> Route:
        route = Route(*ROUTES['board_memberships_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def boards_update(self, id: int) -> Route:
        route = Route(*ROUTES['boards_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def cards_update(self, id: int) -> Route:
        route = Route(*ROUTES['cards_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def comment_actions_update(self, id: int) -> Route:
        route = Route(*ROUTES['comment_actions_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def labels_update(self, id: int) -> Route:
        route = Route(*ROUTES['labels_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def lists_update(self, id: int) -> Route:
        route = Route(*ROUTES['lists_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def notifications_update(self, ids: int) -> Route:
        route = Route(*ROUTES['notifications_update'], self.handler)
        route.endpoint = route.endpoint.format(ids=ids)
        return route

    def projects_update(self, id: int) -> Route:
        route = Route(*ROUTES['projects_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def tasks_update(self, id: int) -> Route:
        route = Route(*ROUTES['tasks_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_update(self, id: int) -> Route:
        route = Route(*ROUTES['users_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_update_email(self, id: int) -> Route:
        route = Route(*ROUTES['users_update_email'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_update_password(self, id: int) -> Route:
        route = Route(*ROUTES['users_update_password'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_update_username(self, id: int) -> Route:
        route = Route(*ROUTES['users_update_username'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def attachments_update(self, id: int) -> Route:
        route = Route(*ROUTES['attachments_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def board_memberships_update(self, id: int) -> Route:
        route = Route(*ROUTES['board_memberships_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def boards_update(self, id: int) -> Route:
        route = Route(*ROUTES['boards_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def cards_update(self, id: int) -> Route:
        route = Route(*ROUTES['cards_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def comment_actions_update(self, id: int) -> Route:
        route = Route(*ROUTES['comment_actions_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def labels_update(self, id: int) -> Route:
        route = Route(*ROUTES['labels_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def lists_update(self, id: int) -> Route:
        route = Route(*ROUTES['lists_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def notifications_update(self, ids: int) -> Route:
        route = Route(*ROUTES['notifications_update'], self.handler)
        route.endpoint = route.endpoint.format(ids=ids)
        return route

    def projects_update(self, id: int) -> Route:
        route = Route(*ROUTES['projects_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def tasks_update(self, id: int) -> Route:
        route = Route(*ROUTES['tasks_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_update(self, id: int) -> Route:
        route = Route(*ROUTES['users_update'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_update_email(self, id: int) -> Route:
        route = Route(*ROUTES['users_update_email'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_update_password(self, id: int) -> Route:
        route = Route(*ROUTES['users_update_password'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_update_username(self, id: int) -> Route:
        route = Route(*ROUTES['users_update_username'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def access_tokens_delete(self) -> Route:
        route = Route(*ROUTES['access_tokens_delete'], self.handler)
        return route

    def attachments_delete(self, id: int) -> Route:
        route = Route(*ROUTES['attachments_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def board_memberships_delete(self, id: int) -> Route:
        route = Route(*ROUTES['board_memberships_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def boards_delete(self, id: int) -> Route:
        route = Route(*ROUTES['boards_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def card_labels_delete(self, cardId: int, labelId: int) -> Route:
        route = Route(*ROUTES['card_labels_delete'], self.handler)
        route.endpoint = route.endpoint.format(cardId=cardId, labelId=labelId)
        return route

    def card_memberships_delete(self, cardId: int) -> Route:
        route = Route(*ROUTES['card_memberships_delete'], self.handler)
        route.endpoint = route.endpoint.format(cardId=cardId)
        return route

    def cards_delete(self, id: int) -> Route:
        route = Route(*ROUTES['cards_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def comment_actions_delete(self, id: int) -> Route:
        route = Route(*ROUTES['comment_actions_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def labels_delete(self, id: int) -> Route:
        route = Route(*ROUTES['labels_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def lists_delete(self, id: int) -> Route:
        route = Route(*ROUTES['lists_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def project_managers_delete(self, id: int) -> Route:
        route = Route(*ROUTES['project_managers_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def projects_delete(self, id: int) -> Route:
        route = Route(*ROUTES['projects_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def tasks_delete(self, id: int) -> Route:
        route = Route(*ROUTES['tasks_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route

    def users_delete(self, id: int) -> Route:
        route = Route(*ROUTES['users_delete'], self.handler)
        route.endpoint = route.endpoint.format(id=id)
        return route