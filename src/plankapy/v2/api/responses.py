from __future__ import annotations
from httpx import HTTPStatusError

__all__ = (
    "PlankaError",
    "Conflict",
    "Forbidden",
    "NotFound",
    "Unauthorized",
    "UnprocessableEntity",
    "ValidationError",
)

class PlankaError(HTTPStatusError): ...

class Conflict(PlankaError): ...
"""Request conflicts with current state of the resource"""

class Forbidden(PlankaError): ...
"""Access forbidden - insufficient permissions"""

class NotFound(PlankaError): ...
"""Resource not found"""

class Unauthorized(PlankaError): ...
"""Authentication required or invalid credentials"""

class UnprocessableEntity(PlankaError): ...
"""Request contains semantic errors or validation failures"""

class ValidationError(PlankaError): ...
"""Request validation failed due to missing or invalid parameters"""