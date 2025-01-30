# plankapy
A Python API for [Planka](https://github.com/plankanban/planka)

![PyPI - License](https://img.shields.io/pypi/l/plankapy)

![PyPI - Version](https://img.shields.io/pypi/v/plankapy) ![PyPI - Downloads](https://img.shields.io/pypi/dw/plankapy) ![GitHub last commit](https://img.shields.io/github/last-commit/hwelch-fle/plankapy)

[![Release](https://github.com/hwelch-fle/plankapy/actions/workflows/python-publish.yml/badge.svg)](https://github.com/hwelch-fle/plankapy/actions/workflows/python-publish.yml) [![Docs](https://github.com/hwelch-fle/plankapy/actions/workflows/docs.yml/badge.svg)](https://github.com/hwelch-fle/plankapy/actions/workflows/docs.yml) 


## Installation
```bash
pip install plankapy
```

## Documentation
The full documentation can be found [here](https://hwelch-fle.github.io/plankapy/).

All Interfaces are documented in the [API](https://hwelch-fle.github.io/plankapy/interfaces/Planka/) section.

## Features
### No Keys Required
Planka models have all been implemented as Python objects. This means that you can access all the properties of a resource as if it were a Python object:
```python
>>> project.name
'Project 1'

>>> project.managers
[User(id=1, username='username', ...), User(id=2, username='username2', ...), ...]
```

### Disambiguation of resource attributes and methods
All models have type hints for every property and attribute, meaning you don't have to guess what a method or property will return. When using a modern IDE, this allows for extensive code completion and prevents you from having to remember what every property and method returns.

### Synced by Default
All included resources are accessible through object properties that send out a request to the server when accessed. This means that you can access up to date information about a resource without having to manually refresh it.
```python
>>> list1 = board.lists[0]
>>> list2 = board.lists[1]

>>> list1.cards
[Card(id=1, name='Card 1', ...), Card(id=2, name='Card 2', ...)]

>>> list2.cards
[]

>>> list1.cards[0].move(list2)

>>> list1.cards
[Card(id=2, name='Card 2', ...)]

>>> list2.cards
[Card(id=1, name='Card 1', ...)]
```


### Edit with Context
Because all stored objects maintain the attributes assigned to them on their creation, direct attribute editing is *not* synced with the server resource. To mitigate this a `.editor()` context manager is provided that refreshes the resource on entry and updates the resource on exit.

#### Direct editing of attributes fails to update the resource
```python
>>> c1 = list1.cards[0]
>>> c1.name = "New Name"
>>> c1.name
'New Name'

# Get the resource again to see that the name has not changed
>>> c2 = list1.cards[0]
>>> c2.name
'Card 1'
```
#### Context editing updates the resource after exiting the context
```python
>>> c1 = list1.cards[0]
>>> with c1.editor():
...     c1.name = "New Name"

>>> c1.name
'New Name'

# Get the resource again to see that the name has changed
>>> c2 = list1.cards[0]

>>> c2.name
'New Name'
```

## Usage
Getting started with plankapy is as simple as creating a `Planka` object and passing it your authentication method. From there, you can access all the resources available to your logged in user account.

```python
>>> from plankapy import Planka, PasswordAuth

>>> planka = Planka("https://planka.example.com", PasswordAuth("username", "password"))

>>> planka.me
User(id=1, username='username', ...)

>>> planka.projects
[Project(id=1, name='Project 1', ...), Project(id=2, name='Project 2', ...), ...]
```

## License
This project is licensed under the AGPLv3 License - see the [LICENSE](LICENSE) file for details.

