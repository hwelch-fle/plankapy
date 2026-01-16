from typing import Literal, TypeAlias
from functools import wraps

from .handlers import JSONHandler



class Route:
    """Wraps a JSONHandler method with a specific HTTP method and endpoint.
    On call, it delegates the request to the wrapped method.
    
    Usage:
    >>> route = Route('GET', '/api/projects', handler)
    >>> route()
    <JSONResponse>
    """
    
    RequestType: TypeAlias = Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE']
    
    def __init__(self, method: RequestType, endpoint: str, handler: JSONHandler):
        self.handler = handler
        self.method = method
        self.endpoint = endpoint

    @property
    def url(self):
        return self.handler.base_url + self.endpoint
    
    def __call__(self, **data) -> JSONHandler.JSONResponse:
        with self.handler.endpoint_as(self.endpoint):
            if self.method == 'GET':
                return self.handler.get()
            
            elif self.method == 'POST':
                return self.handler.post(data)
            
            elif self.method == 'PATCH':
                return self.handler.patch(data)
            
            elif self.method == 'PUT':
                return self.handler.put(data)
            
            elif self.method == 'DELETE':
                return self.handler.delete()
                
        return None

    def __repr__(self):
        return f'<Route {self.method} {self.endpoint} for {self.handler}>'
    
    def __iter__(self):
        if not self.method == 'GET':
            raise ValueError('Only GET routes can be iterated')
        return iter(self()['items'])

class Routes:
    """Container for all routes in the Planka API.
    Each method returns a Route object that can be called to make a request.
    
    Usage:
    >>> routes = Routes(handler)
    >>> route = routes.index()
    >>> route()
    <JSONHandler.JSONResponse>

    >>> update_card = routes.cards_update(1)
    >>> update_card(name='Updated name')
    <JSONHandler.JSONResponse>
    """
    def __init__(self, handler: JSONHandler) -> None:
        self.handler = handler
    
    def register_route(method: Route.RequestType, endpoint: str):
        def _wrapper(route):
            @wraps(route)
            def _wrapped(self, *args, **kwargs):
                if args:
                    arg_map = dict(zip(route.__annotations__.keys(), args))
                    kwargs.update(arg_map)
                return Route(method, endpoint.format(**kwargs), self.handler)
            return _wrapped
        return _wrapper

    @register_route('GET', '/*')
    def get_index(self) -> Route: ...

    @register_route('GET', '/api/users/me')
    def get_me(self) -> Route: ...

    @register_route('GET', '/api/config')
    def get_config(self) -> Route: ...

    @register_route('GET', '/api/boards/{id}')
    def get_board(self, id: int) -> Route: ...

    @register_route('GET', '/api/cards/{cardId}/actions')
    def get_action_index(self, cardId: int) -> Route: ...

    @register_route('GET', '/api/cards/{id}')
    def get_card(self, id: int) -> Route: ...

    @register_route('GET', '/api/notifications')
    def get_notification_index(self) -> Route: ...

    @register_route('GET', '/api/notifications/{id}')
    def get_notification(self, id: int) -> Route: ...

    @register_route('GET', '/api/projects')
    def get_project_index(self) -> Route: ...

    @register_route('GET', '/api/projects/{id}')
    def get_project(self, id: int) -> Route: ...

    @register_route('GET', '/api/users')
    def get_user_index(self) -> Route: ...

    @register_route('GET', '/api/users/{id}')
    def get_user(self, id: int) -> Route: ...

    @register_route('GET', '/attachments/{id}/download/{filename}')
    def get_attachment_download(self, id: int, filename: str) -> Route: ...

    @register_route('GET', '/attachments/{id}/download/thumbnails/cover-256.{extension}')
    def get_attachment_download_thumbnail(self, id: int, extension: str) -> Route: ...

    @register_route('GET', '/project-background-images/*')
    def get_project_background_images(self) -> Route: ...

    @register_route('GET', '/user-avatars/*')
    def get_user_avatars(self) -> Route: ...

    @register_route('POST', '/api/access-tokens')
    def post_access_tokens(self) -> Route: ...

    @register_route('POST', '/api/access-tokens/exchange-using-oidc')
    def post_exchange_using_oidc(self) -> Route: ...

    @register_route('POST', '/api/boards/{boardId}/labels')
    def post_label(self, boardId: int) -> Route: ...

    @register_route('POST', '/api/boards/{boardId}/lists')
    def post_list(self, boardId: int) -> Route: ...

    @register_route('POST', '/api/boards/{boardId}/memberships')
    def post_board_membership(self, boardId: int) -> Route: ...

    @register_route('POST', '/api/cards/{cardId}/attachments')
    def post_attachment(self, cardId: int) -> Route: ...

    @register_route('POST', '/api/cards/{cardId}/comment-actions')
    def post_comment_action(self, cardId: int) -> Route: ...

    @register_route('POST', '/api/cards/{cardId}/labels')
    def post_card_label(self, cardId: int) -> Route: ...

    @register_route('POST', '/api/cards/{cardId}/memberships')
    def post_card_membership(self, cardId: int) -> Route: ...

    @register_route('POST', '/api/cards/{cardId}/tasks')
    def post_task(self, cardId: int) -> Route: ...

    @register_route('POST', '/api/cards/{id}/duplicate')
    def post_duplicate_card(self, id: int) -> Route: ...

    @register_route('POST', '/api/lists/{id}/sort')
    def post_sort_list(self, id: int) -> Route: ...

    @register_route('POST', '/api/lists/{id}/cards')
    def post_card(self, id: int) -> Route: ...

    @register_route('POST', '/api/projects')
    def post_project(self) -> Route: ...

    @register_route('POST', '/api/projects/{id}/background-image')
    def post_project_background_image(self, id: int) -> Route: ...

    @register_route('POST', '/api/projects/{projectId}/boards')
    def post_board(self, projectId: int) -> Route: ...

    @register_route('POST', '/api/projects/{projectId}/managers')
    def post_project_manager(self, projectId: int) -> Route: ...

    @register_route('POST', '/api/users')
    def post_user(self) -> Route: ...

    @register_route('POST', '/api/users/{id}/avatar')
    def post_user_avatar(self, id: int) -> Route: ...

    @register_route('PUT', '/api/attachments/{id}')
    def put_attachment(self, id: int) -> Route: ...

    @register_route('PUT', '/api/board-memberships/{id}')
    def put_board_membership(self, id: int) -> Route: ...

    @register_route('PUT', '/api/boards/{id}')
    def put_board(self, id: int) -> Route: ...

    @register_route('PUT', '/api/cards/{id}')
    def put_card(self, id: int) -> Route: ...

    @register_route('PUT', '/api/comment-actions/{id}')
    def put_comment_action(self, id: int) -> Route: ...

    @register_route('PUT', '/api/labels/{id}')
    def put_label(self, id: int) -> Route: ...

    @register_route('PUT', '/api/lists/{id}')
    def put_list(self, id: int) -> Route: ...

    @register_route('PUT', '/api/notifications/{ids}')
    def put_notification(self, ids: str) -> Route: ...

    @register_route('PUT', '/api/projects/{id}')
    def put_project(self, id: int) -> Route: ...

    @register_route('PUT', '/api/tasks/{id}')
    def put_task(self, id: int) -> Route: ...

    @register_route('PUT', '/api/users/{id}')
    def put_user(self, id: int) -> Route: ...

    @register_route('PUT', '/api/users/{id}/email')
    def put_user_email(self, id: int) -> Route: ...

    @register_route('PUT', '/api/users/{id}/password')
    def put_user_password(self, id: int) -> Route: ...

    @register_route('PUT', '/api/users/{id}/username')
    def put_user_username(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/attachments/{id}')
    def patch_attachment(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/board-memberships/{id}')
    def patch_board_membership(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/boards/{id}')
    def patch_board(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/cards/{id}')
    def patch_card(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/comment-actions/{id}')
    def patch_comment_action(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/labels/{id}')
    def patch_label(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/lists/{id}')
    def patch_list(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/notifications/{ids}')
    def patch_notification(self, ids: str) -> Route: ...

    @register_route('PATCH', '/api/projects/{id}')
    def patch_project(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/tasks/{id}')
    def patch_task(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/users/{id}')
    def patch_user(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/users/{id}/email')
    def patch_user_email(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/users/{id}/password')
    def patch_user_password(self, id: int) -> Route: ...

    @register_route('PATCH', '/api/users/{id}/username')
    def patch_user_username(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/access-tokens/me')
    def delete_access_tokens(self) -> Route: ...

    @register_route('DELETE', '/api/attachments/{id}')
    def delete_attachment(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/board-memberships/{id}')
    def delete_board_membership(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/boards/{id}')
    def delete_board(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/cards/{cardId}/labels/{labelId}')
    def delete_card_label(self, cardId: int, labelId: int) -> Route: ...

    @register_route('DELETE', '/api/cards/{cardId}/memberships')
    def delete_card_membership(self, cardId: int) -> Route: ...

    @register_route('DELETE', '/api/cards/{id}')
    def delete_card(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/comment-actions/{id}')
    def delete_comment_action(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/labels/{id}')
    def delete_label(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/lists/{id}')
    def delete_list(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/project-managers/{id}')
    def delete_project_manager(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/projects/{id}')
    def delete_project(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/tasks/{id}')
    def delete_task(self, id: int) -> Route: ...

    @register_route('DELETE', '/api/users/{id}')
    def delete_user(self, id: int) -> Route: ...
