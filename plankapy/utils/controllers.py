from dataclasses import dataclass
import json

import plankapy.utils.handlers as api
from constants import Gradient, LabelColor
from plankapy.utils.handlers import JSONResponse

# TODO: Add Image Background Support
class ProjectController(api.ProjectHandler):
    """
    [x] 'POST /api/projects': 'projects/create',
    [-] 'POST /api/projects/:id/background-image': 'projects/update-background-image',
    [x] 'POST /api/projects/:projectId/boards': 'boards/create',
    [x] 'POST /api/projects/:projectId/managers': 'project-managers/create',

    [x] 'PATCH /api/projects/:id': 'projects/update',

    [x] 'GET /api/projects': 'projects/index',
    [x] 'GET /api/projects/:id': 'projects/show',

    [x] 'DELETE /api/projects/:id': 'projects/delete',
    """
    
    def create_project(self, name: str, description: str, color: Gradient) -> dict:
        return self.post({
            'name': name,
            'description': description,
            'color': color
        })
    
    def update_background_image(self, project_id: int, image_path: str) -> dict:
        raise NotImplementedError
    
    def create_board(self, project_id: int, name: str, description: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{project_id}/boards'):
            return self.post({
                'name': name,
                'description': description
            })
    
    def create_project_manager(self, project_id: int, user_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{project_id}/managers'):
            return self.post({
                'user_id': user_id
            })
    
    def update_project(self, project_id: int, name: str, description: str, color: Gradient) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{project_id}'):
            return self.patch({
                'name': name,
                'description': description,
                'color': color
            })
        
    def get_projects(self) -> list[dict]:
        return self.get()
    
    def get_project(self, project_id: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{project_id}'):
            return self.get()
    
    def delete(self, project_id: str) -> dict[str, str]:
        with self.endpoint_as(f'{self.endpoint}/{project_id}'):
            return self.delete()
        
class BoardController(api.BoardHandler):
    """
    [x] 'DELETE /api/boards/:id': 'boards/delete',
    
    [x] 'GET /api/boards/:id': 'boards/show',
    
    [ ] 'PATCH /api/boards/:id': 'boards/update',
    
    [ ] 'POST /api/boards/:boardId/labels': 'labels/create',
    [ ] 'POST /api/boards/:boardId/lists': 'lists/create',
    [ ] 'POST /api/boards/:boardId/memberships': 'board-memberships/create',
    """
    
    def get_board(self, board_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{board_id}'):
            return self.get()
    
    def update_board(self, board_id: int, name: str, description: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{board_id}'):
            raise NotImplementedError
    
    def delete_board(self, board_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{board_id}'):
            return self.delete()
    
    def create_label(self, board_id: int, name: str, color: LabelColor) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{board_id}/labels'):
            raise NotImplementedError
    
    def create_list(self, board_id: int, name: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{board_id}/lists'):
            raise NotImplementedError
    
    def create_board_membership(self, board_id: int, user_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{board_id}/memberships'):
            raise NotImplementedError
            
class ListController(api.ListHandler):
    """
    [x] 'DELETE /api/lists/:id': 'lists/delete',
    
    [x] 'GET /api/lists/:id': 'lists/show',
    
    [ ] 'PATCH /api/lists/:id': 'lists/update',
    
    [ ] 'POST /api/lists/:listId/cards': 'cards/create',
    [ ] 'POST /api/lists/:id/sort': 'lists/sort'
    """
    
    def get_list(self, list_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{list_id}'):
            return self.get()
    
    def delete_list(self, list_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{list_id}'):
            return self.delete()
    
    def update_list(self, list_id: int, name: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{list_id}'):
            raise NotImplementedError
    
    def create_card(self, list_id: int, name: str, description: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{list_id}/cards'):
            raise NotImplementedError
    
    def sort_list(self, list_id: int, position: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{list_id}/sort'):
            raise NotImplementedError
        

class CardController(api.CardHandler):
    """
    [ ] 'DELETE /api/cards/:cardId/labels/:labelId': 'card-labels/delete',
    [ ] 'DELETE /api/cards/:cardId/memberships': 'card-memberships/delete',
    [x] 'DELETE /api/cards/:id': 'cards/delete',
    
    [x] 'GET /api/cards/:cardId/actions': 'actions/index',
    [x] 'GET /api/cards/:id': 'cards/show',
    
    [ ] 'PATCH /api/cards/:id': 'cards/update',
    
    [ ] 'POST /api/cards/:cardId/attachments': 'attachments/create',
    [ ] 'POST /api/cards/:cardId/comment-actions': 'comment-actions/create',
    [ ] 'POST /api/cards/:cardId/labels': 'card-labels/create',
    [ ] 'POST /api/cards/:cardId/memberships': 'card-memberships/create',
    [ ] 'POST /api/cards/:cardId/tasks': 'tasks/create',
    [ ] 'POST /api/cards/:id/duplicate': 'cards/duplicate',
    """
    
    def get_card(self, card_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{card_id}'):
            return self.get()
    
    def delete_card(self, card_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{card_id}'):
            return self.delete()
    
    def get_card_actions(self, card_id: int) -> list[dict]:
        with self.endpoint_as(f'{self.endpoint}/{card_id}/actions'):
            return self.get()
    
    def update_card(self, card_id: int, name: str, description: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{card_id}'):
            raise NotImplementedError
    
    def create_attachment(self, card_id: int, file_path: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{card_id}/attachments'):
            raise NotImplementedError
    
    def create_comment_action(self, card_id: int, comment: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{card_id}/comment-actions'):
            raise NotImplementedError
    
    def create_label(self, card_id: int, label_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{card_id}/labels'):
            raise NotImplementedError
    
    def create_card_membership(self, card_id: int, user_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{card_id}/memberships'):
            raise NotImplementedError
    
    def create_task(self, card_id: int, name: str, description: str) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{card_id}/tasks'):
            raise NotImplementedError
    
    def duplicate_card(self, card_id: int) -> dict:
        with self.endpoint_as(f'{self.endpoint}/{card_id}/duplicate'):
            raise NotImplementedError