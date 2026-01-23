import sys
sys.path.append('../../src')

import plankapy.v2 as plankapy

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import (
        Any, 
        TypeVar,
        _Generic, # type: ignore
        _TypedDict, # type: ignore
    )
    _T = TypeVar('_T', bound=_TypedDict)
    _M = TypeVar('_M', bound=plankapy.models.PlankaModel[Any])
else:
    _T = object
    _M = object
    _TypedDict = object
    _Generic = object



planka = plankapy.Planka(client=plankapy.Client(base_url='http://localhost:1337'))
planka.logon(api_key='ykiLbBGA_uCD6qJ7XYIXpCcvMfpsdI86uDMpA6jyn')

VERBOSE = True

def _get_model_schema(model: type[plankapy.models.PlankaModel[_T]]) -> _TypedDict:
    """Helper function that introspects the Generic TypedDict bases for a model"""
    bases: tuple[Any, ...] = getattr(model, '__orig_bases__')
    generic: _Generic = bases[0]
    
    generic_args: tuple[Any, ...] = getattr(generic, '__args__')
    typed_dict: _TypedDict = generic_args[0]
    return typed_dict


def _get_optional(typed_dict: _TypedDict) -> set[str]:
    """TypedDict.__optional_keys__ is not evaluated in this context, so we need to check the ForwardRef
    of each key for NotRequired (which is the first part of the type hint)
    """
    return {
        k
        for k in (typed_dict.__required_keys__ | typed_dict.__optional_keys__)
        if typed_dict.__annotations__[k].__forward_arg__.startswith('NotRequired')
    }


def _test_schema(model: _M,  # type: ignore
                *, 
                sys_keys: set[str]|None=None) -> None:
    """Test a plankapy model schema against a Planka server
    
    Args:
        model (PlankaModel): A model instance to test
        sys_keys (set[str]|None): Additional keys that the system attaches to responses
        
    Tests:
        1) Model has all keys marked as `Required` in the TypedDict schema
        2) Response keys are all defined in the Model or passed `sys_keys` set
    """
    model_schema = _get_model_schema(type(model))
    req_keys = set(model_schema.__required_keys__)
    opt_keys = _get_optional(model_schema)
    # Ensure that the required keys don't contain optional keys
    req_keys = req_keys - opt_keys
    
    if not sys_keys:
        sys_keys = set()
    
    model_keys = set(model.schema.keys())
    
    try:
        # Test required
        assert req_keys.issubset(model_keys), f'Missing from Response: {req_keys ^ model_keys}'
        
        # Test Missing
        assert model_keys.issubset(req_keys | opt_keys | sys_keys), f'Undefined in Schema: {model_keys ^ (req_keys | opt_keys | sys_keys)}'
    except AssertionError as e:
        if VERBOSE:
            print(f'{model.__class__.__name__}: FAIL ({e})')
            return
        
    if VERBOSE:
        print(f'{model.__class__.__name__}: PASS')


def find_and_test_model(models: list[_M], name: str='Unknown') -> _M | None:
    for model in models:
        _test_schema(model)
        return model
    print(f'!! Unable to find {name} for testing !!')


def test_schemas():

    find_and_test_model([planka.me], 'User (current)')
    find_and_test_model(planka.webhooks, 'Webhook')
    find_and_test_model([planka.config], 'Config')
    find_and_test_model(planka.notifications, 'Notification')
    
    # Require A Project
    assert (project := find_and_test_model(planka.projects, 'Project'))
    find_and_test_model(project.notification_services, 'NotificationServices')
    find_and_test_model(project.base_custom_field_groups, 'BaseCustomFieldGroup')
    find_and_test_model(project.users, 'User (other)')
    find_and_test_model(project.background_images, 'BackgroundImage')
    find_and_test_model(project.board_memberships, 'BoardMembership')
    
    # Require a Board
    assert (board := find_and_test_model(project.boards, 'Board'))
    find_and_test_model(board.active_lists, 'List (active)')
    find_and_test_model(board.closed_lists, 'List (closed)')
    find_and_test_model([board.archive_list], 'List (archive)')
    find_and_test_model([board.trash_list], 'List (trash)')
    find_and_test_model(board.attachments, 'Attachment')
    find_and_test_model(board.labels, 'Label')
    find_and_test_model(board.card_labels, 'CardLabel')
    find_and_test_model(board.card_memberships, 'CardMembership')
    find_and_test_model(board.board_memberships, 'BoardMembership')
    find_and_test_model(board.task_lists, 'TaskList')
    find_and_test_model(board.tasks, 'Task')
    find_and_test_model(board.custom_field_groups, 'CustomFieldGroup')
    find_and_test_model(board.custom_fields, 'CustomField')
    find_and_test_model(board.custom_field_values, 'CustomFieldValue')
    
    # Require a Card
    assert (card := find_and_test_model(board.cards, 'Card'))
    find_and_test_model(card.comments, 'Comment')
    find_and_test_model(card.actions, 'Action')

if __name__ == '__main__':
    test_schemas()