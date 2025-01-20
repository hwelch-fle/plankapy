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
