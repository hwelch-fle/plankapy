from __future__ import annotations
from typing import Any
from httpx import HTTPStatusError

__all__ = (
    "PlankaError",
    "ERRORS",
    "Conflict",
    "Forbidden",
    "NotFound",
    "Unauthorized",
    "UnprocessableEntity",
    "ValidationError",
)

class PlankaError(HTTPStatusError):
    def __init__(self, parent: HTTPStatusError, *args: Any, **kwargs: Any) -> None:
        response_json: dict[str, str] = parent.response.json()
        message = response_json.get('message', 'NO_MESSAGE')
        super().__init__(message, request=parent.request, response=parent.response)
        for problem in response_json.get('problems', []):
            self.add_note(problem)


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

ERRORS: dict[str, type[PlankaError]] = {
    'E_CONFLICT': Conflict,
    'E_FORBIDDEN': Forbidden,
    'E_NOT_FOUND': NotFound,
    'E_UNAUTHORIZED': Unauthorized,
    'E_UNPROCESSABLE_ENTITY': UnprocessableEntity,
    'E_MISSING_OR_INVALID_PARAMS': ValidationError,
}
