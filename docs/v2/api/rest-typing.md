# REST Typing

All Planka API endpoints habe their request/response body typed here using `TypedDict`. This means that at runtime all 
objects here are `dict` objects, but can be statically analyzed by a type checker. 

::: plankapy.v2.api.typ
    options:
        show_if_no_docstring: true