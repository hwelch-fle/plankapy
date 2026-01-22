# TODO: A Server class that can be bound to a webhook and dispatch functions

from collections.abc import Callable, Generator
from datetime import datetime
from typing import Any
from .interface import Planka
from .api.events import PlankaEvent, PlankaEvents

EventHandler = Callable[[Planka, Any], Any]
"""Type Signature for an Event Handler

Args:
    arg0: Planka
    arg1: EventHook Response
Returns:
    Any: When a handler is triggered, the dispatcher will yield results
"""

EventHandlerMap = dict[PlankaEvent | tuple[PlankaEvent, ...], list[EventHandler]]
"""Mapping of event/events to Handlers

Keys can be a single event or a tuple of events, values are a list of handlers to be called on that event
"""

def print_card_deleted(planka: Planka, hook_response: Any):
    print(f'{planka.me.name} says: Card Deleted: {hook_response}')

def print_card_created(planka: Planka, hook_response: Any):
    print(f'{planka.me.name} says: Card Created: {hook_response}')

def print_card_updated(planka: Planka, hook_response: Any):
    print(f'{planka.me.name} says: Card Updated: {hook_response}')

def print_hello_world(planka: Planka, hook_response: Any):
    print(f'Something happened! Hello World! We\'re doing it again!')

DEFAULT_HANDLERS: EventHandlerMap = {
    'cardCreate': [print_card_created],
    'cardUpdate': [print_card_updated],
    'cardDelete': [print_card_deleted],
    ('cardCreate', 'cardUpdate', 'cardDelete'): [
        print_hello_world, 
        print_card_created, 
        print_card_updated, 
        print_card_deleted
    ],
}

class EventDispatcher:
    """A simple server that creates or binds to an existing webhook and dispatches 
    automation scripts when pinged
    """

    __events__ = PlankaEvents

    def __init__(self, name: str, url: str,
                 *, 
                 planka: Planka, 
                 handlers: EventHandlerMap=DEFAULT_HANDLERS):
        self.handlers = handlers
        self.url = url
        self.planka = planka

    async def run(self):
        """Run the dispatcher (should be in an event loop)"""
        rcvd_event = str()
        rcvd_data: dict[str, Any] = dict()

        for event, handlers in self.handlers.items():
            if (isinstance(event, tuple) and rcvd_event in event) or (rcvd_event == event):
                yield (event, {h.__name__: h(self.planka, rcvd_data) for h in handlers}, datetime.now())