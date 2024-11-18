from handlers import JSONHandler, JSONResponse
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

    def __call__(self, **data):
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

def index(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['index'], handler)
    return route


def boards_show(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['boards_show'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def actions_index(handler: JSONHandler, cardId: int) -> Route:
    route = Route(*ROUTES['actions_index'], handler)
    route.endpoint = route.endpoint.format(cardId=cardId)
    return route

def cards_show(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['cards_show'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def show_config(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['show_config'], handler)
    return route

def notifications_index(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['notifications_index'], handler)
    return route

def notifications_show(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['notifications_show'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def projects_index(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['projects_index'], handler)
    return route

def projects_show(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['projects_show'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_index(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['users_index'], handler)
    return route

def users_show(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_show'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def attachments_download(handler: JSONHandler, id: int, filename: str) -> Route:
    route = Route(*ROUTES['attachments_download'], handler)
    route.endpoint = route.endpoint.format(id=id, filename=filename)
    return route

def attachments_download_thumbnail(handler: JSONHandler, id: int, extension: str) -> Route:
    route = Route(*ROUTES['attachments_download_thumbnail'], handler)
    route.endpoint = route.endpoint.format(id=id, extension=extension)
    return route

def project_background_images(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['project_background_images'], handler)
    return route

def user_avatars(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['user_avatars'], handler)
    return route

def access_tokens_create(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['access_tokens_create'], handler)
    return route

def exchange_using_oidc(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['exchange_using_oidc'], handler)
    return route

def labels_create(handler: JSONHandler, boardId: int) -> Route:
    route = Route(*ROUTES['labels_create'], handler)
    route.endpoint = route.endpoint.format(boardId=boardId)
    return route

def lists_create(handler: JSONHandler, boardId: int) -> Route:
    route = Route(*ROUTES['lists_create'], handler)
    route.endpoint = route.endpoint.format(boardId=boardId)
    return route

def board_memberships_create(handler: JSONHandler, boardId: int) -> Route:
    route = Route(*ROUTES['board_memberships_create'], handler)
    route.endpoint = route.endpoint.format(boardId=boardId)
    return route

def attachments_create(handler: JSONHandler, cardId: int) -> Route:
    route = Route(*ROUTES['attachments_create'], handler)
    route.endpoint = route.endpoint.format(cardId=cardId)
    return route

def comment_actions_create(handler: JSONHandler, cardId: int) -> Route:
    route = Route(*ROUTES['comment_actions_create'], handler)
    route.endpoint = route.endpoint.format(cardId=cardId)
    return route

def card_labels_create(handler: JSONHandler, cardId: int) -> Route:
    route = Route(*ROUTES['card_labels_create'], handler)
    route.endpoint = route.endpoint.format(cardId=cardId)
    return route

def card_memberships_create(handler: JSONHandler, cardId: int) -> Route:
    route = Route(*ROUTES['card_memberships_create'], handler)
    route.endpoint = route.endpoint.format(cardId=cardId)
    return route

def tasks_create(handler: JSONHandler, cardId: int) -> Route:
    route = Route(*ROUTES['tasks_create'], handler)
    route.endpoint = route.endpoint.format(cardId=cardId)
    return route

def cards_duplicate(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['cards_duplicate'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def lists_sort(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['lists_sort'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def cards_create(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['cards_create'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def projects_create(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['projects_create'], handler)
    return route

def projects_update_background_image(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['projects_update_background_image'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def boards_create(handler: JSONHandler, projectId: int) -> Route:
    route = Route(*ROUTES['boards_create'], handler)
    route.endpoint = route.endpoint.format(projectId=projectId)
    return route

def project_managers_create(handler: JSONHandler, projectId: int) -> Route:
    route = Route(*ROUTES['project_managers_create'], handler)
    route.endpoint = route.endpoint.format(projectId=projectId)
    return route

def users_create(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['users_create'], handler)
    return route

def users_update_avatar(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_update_avatar'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def attachments_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['attachments_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def board_memberships_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['board_memberships_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def boards_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['boards_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def cards_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['cards_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def comment_actions_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['comment_actions_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def labels_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['labels_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def lists_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['lists_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def notifications_update(handler: JSONHandler, ids: int) -> Route:
    route = Route(*ROUTES['notifications_update'], handler)
    route.endpoint = route.endpoint.format(ids=ids)
    return route

def projects_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['projects_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def tasks_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['tasks_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_update_email(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_update_email'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_update_password(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_update_password'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_update_username(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_update_username'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route
    
def attachments_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['attachments_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def board_memberships_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['board_memberships_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def boards_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['boards_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def cards_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['cards_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def comment_actions_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['comment_actions_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def labels_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['labels_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def lists_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['lists_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def notifications_update(handler: JSONHandler, ids: int) -> Route:
    route = Route(*ROUTES['notifications_update'], handler)
    route.endpoint = route.endpoint.format(ids=ids)
    return route

def projects_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['projects_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def tasks_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['tasks_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_update(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_update'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_update_email(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_update_email'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_update_password(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_update_password'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_update_username(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_update_username'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def access_tokens_delete(handler: JSONHandler) -> Route:
    route = Route(*ROUTES['access_tokens_delete'], handler)
    return route

def attachments_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['attachments_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def board_memberships_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['board_memberships_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def boards_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['boards_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def card_labels_delete(handler: JSONHandler, cardId: int, labelId: int) -> Route:
    route = Route(*ROUTES['card_labels_delete'], handler)
    route.endpoint = route.endpoint.format(cardId=cardId, labelId=labelId)
    return route

def card_memberships_delete(handler: JSONHandler, cardId: int) -> Route:
    route = Route(*ROUTES['card_memberships_delete'], handler)
    route.endpoint = route.endpoint.format(cardId=cardId)
    return route

def cards_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['cards_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def comment_actions_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['comment_actions_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def labels_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['labels_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def lists_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['lists_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def project_managers_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['project_managers_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def projects_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['projects_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def tasks_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['tasks_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route

def users_delete(handler: JSONHandler, id: int) -> Route:
    route = Route(*ROUTES['users_delete'], handler)
    route.endpoint = route.endpoint.format(id=id)
    return route