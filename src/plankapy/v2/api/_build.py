"""This private module will pull the latest swagger file from plankanban and build out
a typing module using it

Note:
This will all happen on import, so This should only be run either by intentional importing
e.g. `from typing import _build` to re-build the typing module on initialization or on a schedule
"""

import json
from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from typing import Any, Required, TypedDict

import httpx

import os

SWAGGER_URL = "https://plankanban.github.io/planka/swagger-ui/swagger.json"
SWAGGER_FILE = Path("swagger.json")

INIT_MOD = Path("__init__.py")
SCHEMA_MOD = Path("schemas.py")
PATH_MOD = Path("paths.py")
RESPONSES_MOD = Path("responses.py")

TYPES = {
    "string": "str",
    "boolean": "bool",
    "object": "dict[str, Any]",
    "number": "int",
}

if not SWAGGER_FILE.exists():
    print("Getting Most Recent API Spec...")
    SWAGGER_FILE.write_bytes(httpx.get(SWAGGER_URL).read())


class Property(TypedDict, total=False):
    type: Required[str]
    format: str
    nullable: bool
    description: str
    example: str


class Schema(TypedDict):
    type: str
    required: list[str]
    properties: dict[str, Property]


class ContentSchema(TypedDict): ...


class Content(TypedDict):
    schema: ContentSchema


class Response(TypedDict):
    description: str
    content: dict[str, Content]


def load_swagger(fl: Path = SWAGGER_FILE) -> dict[str, Any]:
    return json.load(open(fl, "rb"))


SWG = load_swagger(SWAGGER_FILE)


def get_paths(swg: dict[str, Any]) -> dict[str, Any]:
    return swg["paths"]


def get_schemas(swg: dict[str, Any]) -> dict[str, Schema]:
    return swg["components"]["schemas"]


def get_responses(swg: dict[str, Any]) -> dict[str, Response]:
    return swg["components"]["responses"]


# TODO: Write a generic return type that specifies `item` and optional `includes` keys
# This type should allow TypeVarTuple reference to schema typed dicts.
def yield_paths() -> Generator[str]:
    yield "from __future__ import annotations"
    yield "from httpx import Client"
    yield "from typing import Any"
    yield "from .schemas import *"
    yield ""
    yield "class PlankaEndpoints:"
    yield "\tdef __init__(self, client: Client) -> None:"
    yield "\t\tself.client = client"
    yield ""
    for r, rs in get_paths(SWG).items():
        print(r)
        for typ, info in rs.items():
            oid = info["operationId"]
            params = info.get("parameters", [])
            header = ["self"]
            header.extend(
                [
                    f"{p['name']}: {TYPES.get(p['schema']['type'], 'Any')}"
                    for p in params
                ]
            )
            body = info.get("requestBody")
            # Get item/includes type from here
            # assign a Item[type] or Includes[itemtype, *includetypes] return
            # may need additional response typeshed for includes keys per endpoint
            # response = info["responses"]["200"]

            if not body:
                yield f"\tdef {oid}({', '.join(header)}) -> Any:"
            else:
                yield f"\tdef {oid}({', '.join(header)}, **body: Any) -> Any:"
            yield f'\t\t"""{info["description"]}'
            if params:
                yield ""
                yield f"\t\tArgs:"
                for p in params:
                    yield f"\t\t\t{p['name']} ({TYPES.get(p['schema']['type'])}): {p['description']})"
            if body:
                # yield "\t\t\t**"
                try:
                    schema = body["content"]["application/json"]["schema"]
                except KeyError:
                    schema = body["content"]["multipart/form-data"]["schema"]
                for name, prop in schema["properties"].items():
                    yield f"\t\t\t{name} ({TYPES.get(prop['type'], 'Any')}): {prop['description']}"
            yield '\t\t"""'
            yield "\t\tparams = locals().copy()"
            yield "\t\tparams.pop('self')"
            if not body:
                yield f'\t\treturn self.client.{typ}("api{r}".format(**params))'
            else:
                yield f"\t\tbody = params.pop('body')"
                yield f'\t\treturn self.client.{typ}("api{r}".format(**params), data=body)'
            yield ""


def yield_responses() -> Generator[str]:
    yield "from __future__ import annotations"
    yield ""
    yield "__all__ = ("
    yield '\t"PlankaError",'
    for i in get_responses(SWG):
        yield f'\t"{i}",'
    yield ")\n"
    yield "class PlankaError(Exception): ..."
    for r, rs in get_responses(SWG).items():
        yield f"\nclass {r}(PlankaError): ..."
        yield f'"""{rs["description"]}"""'


def yield_init() -> Generator[str]:
    _version: str = SWG["info"]["version"]
    yield f'"""{SWG["info"]["title"]} ({_version}) - Generated on {datetime.now().strftime("%a %b %d %Y")}"""'
    yield ""
    yield "from .schema import *"
    yield "from .paths import *"
    yield "from .responses import *"
    yield ""
    yield f'__version__ = "{_version}"'
    # yield f"version = {tuple(int(''.join(p for p in part if p.isdigit())) for part in _version.split('.'))}"
    yield ""


def yield_schema() -> Generator[str]:
    yield "from __future__ import annotations"
    yield "from typing import TypedDict, NotRequired, Any, Literal"
    yield ""
    yield "__all__ = ("
    for c in get_schemas(SWG):
        yield f'\t"{c}",'
    yield ")"
    for c, prop in get_schemas(SWG).items():
        yield f"\nclass {c}(TypedDict):"
        for p, ps in prop["properties"].items():
            t = "Any"
            if "enum" in ps:
                t = f"Literal{ps['enum']}"
            elif ps["type"] in TYPES:
                t = TYPES[ps["type"]]

            if ps["type"] == "array":
                if "items" in ps:
                    if "type" in ps["items"]:
                        t = f"list[{TYPES.get(ps['items']['type'], 'Any')}]"
                if "example" in ps and isinstance(ps["example"], list):
                    t = f"list[Literal{ps['example']}]"

            if p not in prop.get("required", []):
                t = f"NotRequired[{t}]"
            yield f"    {p}: {t}"
            if "description" in ps:
                yield f'    """{ps["description"]}"""'


INIT_MOD.write_text("\n".join(yield_init()))
SCHEMA_MOD.write_text("\n".join(yield_schema()))
PATH_MOD.write_text("\n".join(yield_paths()))
RESPONSES_MOD.write_text("\n".join(yield_responses()))
# Delete the file after it is used
# this ensures that the api typing module
# is always up to date
os.remove(SWAGGER_FILE)
