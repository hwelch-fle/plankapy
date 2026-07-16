from __future__ import annotations

from httpx import Response

from . import (
    paths,
    # typ,
    # pro_schemas as ps,
)


def raise_planka_err(resp: Response) -> None:
    paths.raise_planka_err(resp)


# For implememtation of Planka Pro endpoints
class PlankaEndpoints(paths.PlankaEndpoints): ...
