# plankapy V2
A python 3 based API for controlling a self-hosted Planka instance

## Concept
The original plankapy code is basically justa wrapper around the requests module, this re-write attemps to make it a more fully flegded API implementation that adheres more closely to Python standards

## New Features
### Auth Injection
After having some issues with how a Plankapy instance is initialized using different authentication methods, it was decided to move authentication into an injected Auth class
```python
auth = PasswordAuth('Demo', 'password')
token_auth = TokenAuth('<access_token>')

planka = Planka('http://my.planka.com', auth)

planka.me
>>> User(name='Demo', ...)

```

### Simplified Routes
Originally, all routes were stored in a dictionary, but now the `routes.py` module uses a route registration decorator that's similar to flask.

```python
@register_route('GET', '/*')
def get_index(self) -> Route: ...
```
The method and route are directly above the function header and can be more easily modified and new routes can be added.

These routes are not meant to be exposed to the end user, but instead used in the `plankapy.py` root module when implementing interfaces for Models:

```python
class Board(_Board):

@property
def included(self) -> JSONHandler.JSONResponse:
    # Bind the property to an endpoint
    route = self.routes.get_board(id=self.id)

    # Call the route object to get the JSON response
    return route()['included']
```

### Data Models
All objects returned by API calls are now modeled as python objects. These objects handle updating and modifying their associated enpoints and can iterate over their included objects:
```python
planka = Planka(...)

planka.projects
>>> [Project(id=...), Project(id=...), ...]

for project in planka.projects:
    print(project.name)
    for board in project.boards:
        print('\t'+board.name)

>>> Project 1
>>>     Board A
>>>     BoardB
>>> Project 2
>>>     Board A
>>>     ...
```

### Context Editing
Because each model holds the endpoints for modifying itself, a context manager was created so an object can be directly modified and the modifiation are sent as a PATCH request after the context is `__exit__` ed
```python
card.description
>>> "Hello"

with card.editor()
    card.description += " World"

card.description
>>> "Hello World"
```

### Type Hinting and Literals
All models have the required values clearly marked as Required, All constants use `typing.Literal` so it's clear what the valid options are (e.g. Background Gradients, Label Colors, List Sort Modes, etc.)
```python
# Intellisense will parse the valid gradients from the literal
# and give you a list of valid options
project.set_background_gradient('blue')
```

### Refreshing
All updates made through plankapy will be instantly available to you in the object you called `.update()` on. To keep synced with the instance and changes made through the site, a `.refresh()` metho is provided to make sure the data in your object is up to date.

All implemented `@property` attributes (linked to the `'included'` key of a response) are refreshed immediately when accessed. This means that maintaining a lambda expresion that accesses that property will keep the data up to date.
```python
# Expression to get realtime lists
my_lists = lambda: project.boards[0].lists

for _list in my_lists():
    print(_list.name)

# Using explicit `refresh()`
my_list = board.list[0]

# Sync changes from Planka
my_list.refresh()

```

# Future Plans

### Implement Async
Currenty all operatons are run syncronously. 

However, the interface itself is atomized on individual requests, meaning you can wrap a series of operations in async functions. I will currently leave that activity to the user, but will probably create some simple recipes at some point (like batch updating every card with a specific tag)

### Implement Pickling
Because we have a fuly bi-directional model, we can grab a snapshot of Planka in Python, then pickle that object. This is not yet implemented, but we could theoretically implement the pickling process in the `Model` base class

# Contributing
I'm open to anyone helping out, for now I'm going to keep this version on he v2/v2-working branches. Until it is fleshed out enough to release. I don't want to break any code written in the original `plankapy` v1 release, but with enough warning I think it's okay. Will likely time the relase of this version with the release of Planka 2.0


