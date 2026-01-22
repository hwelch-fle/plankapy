from __future__ import annotations

from . import paths
from typing import (
    Literal,
    Unpack,
)
from httpx import Client, Response, HTTPStatusError
from .pro_schemas import *
from .typ import *
from .errors import *

def raise_planka_err(resp: Response) -> None:
    paths.raise_planka_err(resp)

# For implememtation of Planka Pro endpoints
class PlankaEndpoints(paths.PlankaEndpoints): ...