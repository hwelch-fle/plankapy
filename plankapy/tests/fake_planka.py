"""
Dummy Planka API endpoints for testing purposes.
"""

import flask

APP = flask.app.Flask(__name__)

# Taken from https://github.com/plankanban/planka/blob/master/server/config/routes.js
ROUTES = {
    # Delete Endpoints
    'DELETE /api/access-tokens/me': 'access-tokens/delete',
    'DELETE /api/attachments/:id': 'attachments/delete',
    'DELETE /api/board-memberships/:id': 'board-memberships/delete',
    'DELETE /api/boards/:id': 'boards/delete',
    'DELETE /api/cards/:cardId/labels/:labelId': 'card-labels/delete',
    'DELETE /api/cards/:cardId/memberships': 'card-memberships/delete',
    'DELETE /api/cards/:id': 'cards/delete',
    'DELETE /api/comment-actions/:id': 'comment-actions/delete',
    'DELETE /api/labels/:id': 'labels/delete',
    'DELETE /api/lists/:id': 'lists/delete',
    'DELETE /api/project-managers/:id': 'project-managers/delete',
    'DELETE /api/projects/:id': 'projects/delete',
    'DELETE /api/tasks/:id': 'tasks/delete',
    'DELETE /api/users/:id': 'users/delete',
 
    # Get Endpoints
    'GET /*': 'index',
    'GET /api/boards/:id': 'boards/show',
    'GET /api/cards/:cardId/actions': 'actions/index',
    'GET /api/cards/:id': 'cards/show',
    'GET /api/config': 'show-config',
    'GET /api/notifications': 'notifications/index',
    'GET /api/notifications/:id': 'notifications/show',
    'GET /api/projects': 'projects/index',
    'GET /api/projects/:id': 'projects/show',
    'GET /api/users': 'users/index',
    'GET /api/users/:id': 'users/show',
    'GET /attachments/:id/download/:filename': 'attachments/download',
    'GET /attachments/:id/download/thumbnails/cover-256.:extension': 'attachments/download-thumbnail',
    'GET /project-background-images/*': '/project-background-images',
    'GET /user-avatars/*': '/user-avatars',
    
    # Patch Endpoints
    'PATCH /api/attachments/:id': 'attachments/update',
    'PATCH /api/board-memberships/:id': 'board-memberships/update',
    'PATCH /api/boards/:id': 'boards/update',
    'PATCH /api/cards/:id': 'cards/update',
    'PATCH /api/comment-actions/:id': 'comment-actions/update',
    'PATCH /api/labels/:id': 'labels/update',
    'PATCH /api/lists/:id': 'lists/update',
    'PATCH /api/notifications/:ids': 'notifications/update',
    'PATCH /api/projects/:id': 'projects/update',
    'PATCH /api/tasks/:id': 'tasks/update',
    'PATCH /api/users/:id': 'users/update',
    'PATCH /api/users/:id/email': 'users/update-email',
    'PATCH /api/users/:id/password': 'users/update-password',
    'PATCH /api/users/:id/username': 'users/update-username',

    # Post Endpoints
    'POST /api/access-tokens': 'access-tokens/create',
    'POST /api/access-tokens/exchange-using-oidc': 'access-tokens/exchange-using-oidc',
    'POST /api/boards/:boardId/labels': 'labels/create',
    'POST /api/boards/:boardId/lists': 'lists/create',
    'POST /api/boards/:boardId/memberships': 'board-memberships/create',
    'POST /api/cards/:cardId/attachments': 'attachments/create',
    'POST /api/cards/:cardId/comment-actions': 'comment-actions/create',
    'POST /api/cards/:cardId/labels': 'card-labels/create',
    'POST /api/cards/:cardId/memberships': 'card-memberships/create',
    'POST /api/cards/:cardId/tasks': 'tasks/create',
    'POST /api/cards/:id/duplicate': 'cards/duplicate',
    'POST /api/lists/:id/sort': 'lists/sort',
    'POST /api/lists/:listId/cards': 'cards/create',
    'POST /api/projects': 'projects/create',
    'POST /api/projects/:id/background-image': 'projects/update-background-image',
    'POST /api/projects/:projectId/boards': 'boards/create',
    'POST /api/projects/:projectId/managers': 'project-managers/create',
    'POST /api/users': 'users/create',
    'POST /api/users/:id/avatar': 'users/update-avatar'
}

# Delete Endpoints
@APP.route('/api/access-tokens/me', methods=['DELETE'])
def access_tokens_delete():
    return 'access-tokens/delete'

@APP.route('/api/attachments/<int:id>', methods=['DELETE'])
def attachments_delete(id):
    return 'attachments/delete'

@APP.route('/api/board-memberships/<int:id>', methods=['DELETE'])
def board_memberships_delete(id):
    return 'board-memberships/delete'

@APP.route('/api/boards/<int:id>', methods=['DELETE'])
def boards_delete(id):
    return 'boards/delete'

@APP.route('/api/cards/<int:cardId>/labels/<int:labelId>', methods=['DELETE'])
def card_labels_delete(cardId, labelId):
    return 'card-labels/delete'

@APP.route('/api/cards/<int:cardId>/memberships', methods=['DELETE'])
def card_memberships_delete(cardId):
    return 'card-memberships/delete'

@APP.route('/api/cards/<int:id>', methods=['DELETE'])
def cards_delete(id):
    return 'cards/delete'

@APP.route('/api/comment-actions/<int:id>', methods=['DELETE'])
def comment_actions_delete(id):
    return 'comment-actions/delete'

@APP.route('/api/labels/<int:id>', methods=['DELETE'])
def labels_delete(id):
    return 'labels/delete'

@APP.route('/api/lists/<int:id>', methods=['DELETE'])
def lists_delete(id):
    return 'lists/delete'

@APP.route('/api/project-managers/<int:id>', methods=['DELETE'])
def project_managers_delete(id):
    return 'project-managers/delete'

@APP.route('/api/projects/<int:id>', methods=['DELETE'])
def projects_delete(id):
    return 'projects/delete'

@APP.route('/api/tasks/<int:id>', methods=['DELETE'])
def tasks_delete(id):
    return 'tasks/delete'

@APP.route('/api/users/<int:id>', methods=['DELETE'])
def users_delete(id):
    return 'users/delete'

# Get Endpoints
@APP.route('/*', methods=['GET'])
def index():
    return 'index'

@APP.route('/api/boards/<int:id>', methods=['GET'])
def boards_show(id):
    return 'boards/show'

@APP.route('/api/cards/<int:cardId>/actions', methods=['GET'])
def actions_index(cardId):
    return 'actions/index'

@APP.route('/api/cards/<int:id>', methods=['GET'])
def cards_show(id):
    return 'cards/show'

@APP.route('/api/config', methods=['GET'])
def show_config():
    return 'show-config'

@APP.route('/api/notifications', methods=['GET'])
def notifications_index():
    return 'notifications/index'

@APP.route('/api/notifications/<int:id>', methods=['GET'])
def notifications_show(id):
    return 'notifications/show'

@APP.route('/api/projects', methods=['GET'])
def projects_index():
    return 'projects/index'

@APP.route('/api/projects/<int:id>', methods=['GET'])
def projects_show(id):
    return 'projects/show'

@APP.route('/api/users', methods=['GET'])
def users_index():
    return 'users/index'

@APP.route('/api/users/<int:id>', methods=['GET'])
def users_show(id):
    return 'users/show'

@APP.route('/attachments/<int:id>/download/<string:filename>', methods=['GET'])
def attachments_download(id, filename):
    return 'attachments/download'

@APP.route('/attachments/<int:id>/download/thumbnails/cover-256.<string:extension>', methods=['GET'])
def attachments_download_thumbnail(id, extension):
    return 'attachments/download-thumbnail'

@APP.route('/project-background-images/*', methods=['GET'])
def project_background_images():
    return '/project-background-images'

@APP.route('/user-avatars/*', methods=['GET'])
def user_avatars():
    return '/user-avatars'

# Patch Endpoints
@APP.route('/api/attachments/<int:id>', methods=['PATCH'])
def attachments_update(id):
    return 'attachments/update'

@APP.route('/api/board-memberships/<int:id>', methods=['PATCH'])
def board_memberships_update(id):
    return 'board-memberships/update'

@APP.route('/api/boards/<int:id>', methods=['PATCH'])
def boards_update(id):
    return 'boards/update'

@APP.route('/api/cards/<int:id>', methods=['PATCH'])
def cards_update(id):
    return 'cards/update'

@APP.route('/api/comment-actions/<int:id>', methods=['PATCH'])
def comment_actions_update(id):
    return 'comment-actions/update'

@APP.route('/api/labels/<int:id>', methods=['PATCH'])
def labels_update(id):
    return 'labels/update'

@APP.route('/api/lists/<int:id>', methods=['PATCH'])
def lists_update(id):
    return 'lists/update'

@APP.route('/api/notifications/<int:ids>', methods=['PATCH'])
def notifications_update(ids):
    return 'notifications/update'

@APP.route('/api/projects/<int:id>', methods=['PATCH'])
def projects_update(id):
    return 'projects/update'

@APP.route('/api/tasks/<int:id>', methods=['PATCH'])
def tasks_update(id):
    return 'tasks/update'

@APP.route('/api/users/<int:id>', methods=['PATCH'])
def users_update(id):
    return 'users/update'

@APP.route('/api/users/<int:id>/email', methods=['PATCH'])
def users_update_email(id):
    return 'users/update-email'

@APP.route('/api/users/<int:id>/password', methods=['PATCH'])
def users_update_password(id):
    return 'users/update-password'

@APP.route('/api/users/<int:id>/username', methods=['PATCH'])
def users_update_username(id):
    return 'users/update-username'

# Post Endpoints
@APP.route('/api/access-tokens', methods=['POST'])
def access_tokens_create():
    return 'access-tokens/create'

@APP.route('/api/access-tokens/exchange-using-oidc', methods=['POST'])
def access_tokens_exchange_using_oidc():
    return 'access-tokens/exchange-using-oidc'

@APP.route('/api/boards/<int:boardId>/labels', methods=['POST'])
def labels_create(boardId):
    return 'labels/create'

@APP.route('/api/boards/<int:boardId>/lists', methods=['POST'])
def lists_create(boardId):
    return 'lists/create'

@APP.route('/api/boards/<int:boardId>/memberships', methods=['POST'])
def board_memberships_create(boardId):
    return 'board-memberships/create'

@APP.route('/api/cards/<int:cardId>/attachments', methods=['POST'])
def attachments_create(cardId):
    return 'attachments/create'

@APP.route('/api/cards/<int:cardId>/comment-actions', methods=['POST'])
def comment_actions_create(cardId):
    return 'comment-actions/create'

@APP.route('/api/cards/<int:cardId>/labels', methods=['POST'])
def card_labels_create(cardId):
    return 'card-labels/create'

@APP.route('/api/cards/<int:cardId>/memberships', methods=['POST'])
def card_memberships_create(cardId):
    return 'card-memberships/create'

@APP.route('/api/cards/<int:cardId>/tasks', methods=['POST'])
def tasks_create(cardId):
    return 'tasks/create'

@APP.route('/api/cards/<int:id>/duplicate', methods=['POST'])
def cards_duplicate(id):
    return 'cards/duplicate'

@APP.route('/api/lists/<int:id>/sort', methods=['POST'])
def lists_sort(id):
    return 'lists/sort'

@APP.route('/api/lists/<int:listId>/cards', methods=['POST'])
def cards_create(listId):
    return 'cards/create'

@APP.route('/api/projects', methods=['POST'])
def projects_create():
    return 'projects/create'

@APP.route('/api/projects/<int:id>/background-image', methods=['POST'])
def projects_update_background_image(id):
    return 'projects/update-background-image'

@APP.route('/api/projects/<int:projectId>/boards', methods=['POST'])
def boards_create(projectId):
    return 'boards/create'

@APP.route('/api/projects/<int:projectId>/managers', methods=['POST'])
def project_managers_create(projectId):
    return 'project-managers/create'

@APP.route('/api/users', methods=['POST'])
def users_create():
    return 'users/create'

@APP.route('/api/users/<int:id>/avatar', methods=['POST'])
def users_update_avatar(id):
    return 'users/update-avatar'

if __name__ == '__main__':
    APP.run(debug=True, port=1338)