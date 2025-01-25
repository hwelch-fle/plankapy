# FILE: /home/asimov/Desktop/plankapy/tests/test_models.py

import pytest
import plankapy.models as models
from dataclasses import dataclass
from datetime import datetime

@dataclass(eq=False)
class TestModel(models.Model):
    id: int = models.Unset
    name: str = models.Unset
    _private: str = models.Unset

def test_base_model():
    instance = TestModel(id=1, name='test', _private='private')
    assert 'private' not in instance, "Private attributes should not be included in __iter__"

    instance.name = models.Unset
    assert 'name' in instance, "Unset value should be skipped by __iter__"

    instance2 = TestModel(**instance)

    assert 'private' not in instance2, "Private attributes should not be unpacked"
    assert hash(instance) == instance.id, "Hash should be equal to id"
    assert instance == instance2, "instances with same `id` should be equal"

@pytest.mark.parametrize("model_class, kwargs", [
    (models.Action_, {'id': 1, 'type': models.ActionType.CREATE, 'data': {}, 'cardId': 1, 'userId': 1}),
    (models.Archive_, {'fromModel': 'Card', 'originalRecordId': 1, 'originalRecord': {}}),
    (models.Attachment_, {'id': 1, 'name': 'Attachment', 'dirname': 'dir', 'filename': 'file'}),
    (models.Board_, {'id': 1, 'name': 'Board', 'position': 1, 'projectId': 1}),
    (models.BoardMembership_, {'id': 1, 'role': models.BoardRole.MEMBER, 'boardId': 1, 'userId': 1}),
    (models.Card_, {'id': 1, 'name': 'Card', 'position': 1, 'boardId': 1, 'listId': 1}),
    (models.CardLabel_, {'id': 1, 'cardId': 1, 'labelId': 1}),
    (models.CardMembership_, {'id': 1, 'cardId': 1, 'userId': 1}),
    (models.CardSubscription_, {'id': 1, 'cardId': 1, 'userId': 1}),
    (models.IdentityProviderUser_, {'id': 1, 'userId': 1}),
    (models.Label_, {'id': 1, 'name': 'Label', 'position': 1, 'color': 'red', 'boardId': 1}),
    (models.List_, {'id': 1, 'name': 'List', 'position': 1, 'boardId': 1}),
    (models.Notification_, {'id': 1, 'isRead': True, 'userId': 1, 'actionId': 1, 'cardId': 1}),
    (models.Project_, {'id': 1, 'name': 'Project'}),
    (models.ProjectManager_, {'id': 1, 'projectId': 1, 'userId': 1}),
    (models.Task_, {'id': 1, 'name': 'Task', 'position': 1}),
    (models.User_, {'id': 1, 'name': 'User', 'email': 'user@example.com'}),
])
def test_model_creation(model_class, kwargs):
    instance = model_class(**kwargs)
    for key, value in kwargs.items():
        assert getattr(instance, key) == value, f"{key} attribute mismatch"