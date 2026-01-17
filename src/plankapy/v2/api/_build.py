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
SCHEMA_MOD = Path("schemas.py") # Schema for each planka object

PATH_MOD = Path("paths.py") # Endpoints
ASYNC_PATH_MOD = Path("async_paths.py") # Async Endpoints
TYPES_MOD = Path("types.py") # Typing for response/request json
ERRORS_MOD = Path("errors.py") # Error implementations

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

REQUESTS: dict[str, Any] | None = None
RESPONSES: dict[str, Any] | None = None
def yield_paths() -> Generator[str]:
    """This is a beautiful function. My god is it a mess I'm sorry"""
    
    yield "from __future__ import annotations"
    yield "from typing import ("
    yield "\tLiteral,"
    yield "\tUnpack,"
    yield ")"
    yield "from httpx import Client"
    yield "from .schemas import *"
    yield "from .types import *"
    yield ""
    yield '__all__ = ("PlankaEndpoints",)'
    yield ""
    yield "class PlankaEndpoints:"
    yield "\tdef __init__(self, client: Client) -> None:"
    yield "\t\tself.client = client"
    yield ""
    
    kwarg_reqs: dict[str, list[str]] = {}
    resps: dict[str, list[str]] = {}
    for r, rs in get_paths(SWG).items():
        for typ, info in rs.items():
            oid = info["operationId"]
            params = info.get("parameters", [])
            header = ["self"]
            header.extend(
                [
                    f"{p['name']}: {TYPES.get(p['schema']['type'], 'Any')}"
                    if "enum" not in p["schema"]
                    else f"{p['name']}: Literal{p['schema']['enum']}"
                    for p in params
                    if p.get('required', False)
                ]
            )
            optional_params = [p for p in params if not p.get('required', False)]
            body = info.get("requestBody")
                    
            # Get item/includes type from here
            # assign a Item[type] or Includes[itemtype, *includetypes] return
            # may need additional response typeshed for includes keys per endpoint
            response = info["responses"]["200"]
            r_schema = response['content']['application/json']['schema']
            r_props = r_schema['properties']
            # Make sure Included gets added before the Response
            has_item = False
            has_included = False
            has_items = False
            resps[f'Response_{oid}'] = []
            resps[f'Response_{oid}'].append(f'"""{response["description"]}"""')
            if 'included' in r_props:
                has_included = True
                resps[f'Included_{oid}'] = []
                r_included = r_props['included']
                r_i_props = r_included.get('properties')
                for p_name, prop in r_i_props.items():
                    if prop["type"] ==  "array":
                        if '$ref' in prop['items']:
                            t = prop['items']['$ref'].split('/')[-1]
                            resps[f'Included_{oid}'].append(f'{p_name}: list[{t}]')
                        elif 'allOf' in prop['items']:
                            base_type = prop['items']['allOf'][0]['$ref'].split('/')[-1]
                            additional_keys = [
                                f'{prop_name}: {TYPES.get(prop["type"])}\n\t"""{prop["description"]}"""'
                                if prop["type"] != 'array'
                                else
                                f'{prop_name}: list[{TYPES.get(prop["items"]["type"])}]\n\t"""{prop["description"]}"""'
                                for obj in prop['items']['allOf'][1:]
                                for prop_name, prop in obj['properties'].items()
                            ]
                            resps[f'Included_{oid}_all({base_type})'] = additional_keys
                            resps[f'Included_{oid}'].append(f'{p_name}: list[Included_{oid}_all]\n\t"""{prop["description"]}"""')
                        else:
                            if prop['type'] == 'array':
                                resps[f'Included_{oid}'].append(f'{p_name}: list[{TYPES.get(prop['items']['type'], 'Any')}]\n\t"""{prop['description']}"""')
                            else:
                                resps[f'Included_{oid}'].append(f'{p_name}: list[{TYPES.get(prop['type'], 'Any')}]\n\t"""{prop['description']}"""')
                                
            if 'item' in r_props:
                has_item = True
                r_item = r_props['item']
                r_i_props = r_item.get('properties')

                if 'allOf' in r_item:
                    base_type = r_item['allOf'][0]['$ref'].split('/')[-1]
                    additional_keys = [
                        f'{prop_name}: {TYPES.get(prop["type"])}\n\t"""{prop["description"]}"""'
                        if prop["type"] != 'array'
                        else
                        f'{prop_name}: list[{TYPES.get(prop["items"]["type"])}]\n\t"""{prop["description"]}"""'
                        for obj in r_item['allOf'][1:]
                        for prop_name, prop in obj['properties'].items()
                    ]
                    resps[f'Item_{oid}({base_type})'] = additional_keys

                elif '$ref' in r_item:
                    has_item = False # Direct reference
                    resps[f'Response_{oid}'].append(f"item: {r_item['$ref'].split('/')[-1]}")

                elif 'properties' in r_item:
                    resps[f'Item_{oid}'] = []
                    for p_name, prop in r_item.get('properties', {}).items():
                        if 'enum' in prop:
                            t = f"Literal{prop['enum']}"
                        else:
                            t = TYPES.get(prop['type'], 'Any')
                        resps[f'Item_{oid}'].append(f"{p_name}: {t}")
                else:
                    has_item = False
                    resps[f'Response_{oid}'].append(f'item: {TYPES.get(r_item["type"])}\n\t"""{r_item['description']}"""')
            
            if 'items' in r_props:
                has_items = True
                r_items = r_props['items']
                r_i_props = r_items.get('properties')
                
                if 'allOf' in r_items['items']:
                    base_type = r_items['items']['allOf'][0]['$ref'].split('/')[-1]
                    additional_keys = [
                        f'{prop_name}: {TYPES.get(prop["type"])}\n\t"""{prop["description"]}"""'
                        if prop["type"] != 'array'
                        else
                        f'{prop_name}: list[{TYPES.get(prop["items"]["type"])}]\n\t"""{prop["description"]}"""'
                        for obj in r_items['items']['allOf'][1:]
                        for prop_name, prop in obj['properties'].items()
                    ]
                    resps[f'Items_{oid}({base_type})'] = additional_keys
            
                else:
                    resps[f'Items_{oid}'] = []
                    #for p_name, prop in r_items.get('properties', {}).items():
                    if r_items['type'] == 'array':
                        if '$ref' in r_items['items']:
                            has_items = False
                            t = r_items['items']['$ref'].split('/')[-1]
                            resps[f'Response_{oid}'].append(f'items: list[{t}]')
            
            if has_items or has_item or has_included:
                if has_item:
                    resps[f'Response_{oid}'].append(f'item: Item_{oid}')
                if has_items:
                    resps[f'Response_{oid}'].append(f'items: list[Items_{oid}]')
                if has_included:
                    resps[f'Response_{oid}'].append(f'included: Included_{oid}')
            
            if not body and not optional_params:
                yield f"\tdef {oid}({', '.join(header)}) -> Response_{oid}:"
            else:
                yield f"\tdef {oid}({', '.join(header)}, **kwargs: Unpack[Request_{oid}]) -> Response_{oid}:"
            yield f'\t\t"""{info["description"]}'
            if params or body:
                yield ""
                yield f"\t\tArgs:"
            if params:
                for p in params:
                    if "enum" in p["schema"]:
                        t = f"Literal{p['schema']['enum']}"
                    else:
                        t = p["schema"]["type"]
                    if p.get('required', False):
                        yield f"\t\t\t{p['name']} ({TYPES.get(t, t)}): {p['description']})"
                    else:
                        yield f"\t\t\t{p['name']} ({TYPES.get(t, t)}): {p['description']}) (optional)"
                        
            if body or optional_params:
                r_typing = f"Request_{oid}"
                kwarg_reqs[r_typing] = []
                if optional_params:
                    for p in optional_params:
                        if 'enum' in p:
                            t = f"Literal{p['enum']}"
                        else:
                            t = TYPES.get(p['schema']['type'], 'Any')
                        kwarg_reqs[r_typing].append(f'{p["name"]}: NotRequired[{t}]\n\t"""{p["description"]}"""')
                if body:
                    try:
                        schema = body["content"]["application/json"]["schema"]
                    except KeyError:
                        schema = body["content"]["multipart/form-data"]["schema"]
                    kwarg_required = schema.get('required', []) 
                    for name, prop in schema["properties"].items():
                        if "enum" in prop:
                            yield f"\t\t\t{name} (Literal{prop['enum']}): {prop['description']}"
                            if name in kwarg_required:
                                kwarg_reqs[r_typing].append(f'{name}: Literal{prop['enum']}\n\t"""{prop['description']}"""')
                            else:
                                kwarg_reqs[r_typing].append(f'{name}: NotRequired[Literal{prop['enum']}]\n\t"""{prop['description']}"""')
                        else:
                            p_type = TYPES.get(prop['type'], 'Any')
                            yield f"\t\t\t{name} ({p_type}): {prop['description']}"
                            if name in kwarg_required:
                                kwarg_reqs[r_typing].append(f'{name}: {p_type}\n\t"""{prop['description']}"""')
                            else:
                                kwarg_reqs[r_typing].append(f'{name}: NotRequired[{p_type}]\n\t"""{prop['description']}"""')
            
            errors = {code: r for code, r in info['responses'].items() if code != '200'}
            if errors:
                yield ""
                yield "\t\tNote:"
                yield "\t\t\tAll status errors are instances of `httpx.HTTPStatusError` at runtime (`response.raise_for_status()`). "
                yield "\t\t\tPlanka internal status errors are included here for disambiguation"
                yield ""
                yield "\t\tRaises:"
                for e_code, e in errors.items():
                    yield f"\t\t\t{e.get('$ref', 'Error').split('/')[-1]}: {int(e_code)} " + e.get('description', '')
                    
            yield '\t\t"""'
            yield "\t\targs = locals().copy()"
            yield "\t\targs.pop('self')"
            if not body and not optional_params:
                yield f'\t\tresp = self.client.{typ}("api{r}".format(**args))'
            elif body and not optional_params:
                yield f"\t\tkwargs = args.pop('kwargs')"
                yield f'\t\tresp = self.client.{typ}("api{r}".format(**args), data=kwargs)'
            elif optional_params or body:
                yield f"\t\tkwargs = args.pop('kwargs')"
                if optional_params:
                    yield f'\t\tvalid_params = {tuple([p['name'] for p in optional_params])}'
                    yield f'\t\tpassed_params = ''{k: v for k, v in kwargs.items() if k in valid_params if isinstance(v, str | int | float)}'
                if optional_params and body:
                    yield f'\t\tresp = self.client.{typ}("api{r}".format(**args), params=passed_params, data=kwargs)'
                elif optional_params:
                    yield f'\t\tresp = self.client.{typ}("api{r}".format(**args), params=passed_params)'
                elif body:
                    yield f'\t\tresp = self.client.{typ}("api{r}".format(**args), data=kwargs)'
            
            yield "\t\tresp.raise_for_status()"
            yield "\t\treturn resp.json()"
            yield ""

    # Store for writing to types module
    global REQUESTS, RESPONSES
    REQUESTS = kwarg_reqs
    RESPONSES = resps

def yield_async_paths() -> Generator[str]:
    for line in yield_paths():
        if '__init__' not in line:
            line = line.replace('def ', 'async def ')
        if 'PlankaEndpoints' in line:
            line = line.replace('PlankaEndpoints', 'AsyncPlankaEndpoints')
        line = line.replace(': Client', ': AsyncClient')
        line = line.replace('import Client', 'import AsyncClient')
        line = line.replace('resp = ', 'resp = await ')
        yield line

def yield_types() -> Generator[str]:
    yield "from __future__ import annotations"
    yield "from typing import ("
    yield "\tAny,"
    yield "\tLiteral,"
    yield "\tTypedDict,"
    yield "\tNotRequired,"
    yield ")"
    yield "from .schemas import *"
    yield ""
    if REQUESTS:
        yield ""
        yield "# Request Typing"
        for c_name, attrs in REQUESTS.items():
            yield f"class {c_name}(TypedDict):"
            for attr in attrs:
                yield f"\t{attr}"
            yield ""
        yield ""

    if RESPONSES:
        yield ""
        yield "# Response Typing"
        for r_name, attrs in RESPONSES.items():
            if not attrs:
                continue
            if '(' in r_name:
                yield f"class {r_name}:"
            else:
                yield f"class {r_name}(TypedDict):"
            
            for attr in attrs:
                yield f"\t{attr}"
            yield ""
        yield ""

def yield_errors() -> Generator[str]:
    yield "from __future__ import annotations"
    yield "from httpx import HTTPStatusError"
    yield ""
    yield "__all__ = ("
    yield '\t"PlankaError",'
    for i in get_responses(SWG):
        yield f'\t"{i}",'
    yield ")\n"
    yield "class PlankaError(HTTPStatusError): ..."
    for r, rs in get_responses(SWG).items():
        yield f"\nclass {r}(PlankaError): ..."
        yield f'"""{rs["description"]}"""'


def yield_init() -> Generator[str]:
    _version: str = SWG["info"]["version"]
    yield f'"""{SWG["info"]["title"]} ({_version}) - Generated on {datetime.now().strftime("%a %b %d %Y")}"""'
    yield ""
    yield "from .schemas import *"
    yield "from .paths import *"
    yield "from .async_paths import *"
    yield "from .responses import *"
    yield ""
    yield f'__version__ = "{_version}"'
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


INIT_MOD.write_text("\n".join(map(lambda l: l.replace('\t', '    '), yield_init())))
SCHEMA_MOD.write_text("\n".join(map(lambda l: l.replace('\t', '    '),yield_schema())))
PATH_MOD.write_text("\n".join(map(lambda l: l.replace('\t', '    '),yield_paths())))
ASYNC_PATH_MOD.write_text("\n".join(map(lambda l: l.replace('\t', '    '),yield_async_paths())))
ERRORS_MOD.write_text("\n".join(map(lambda l: l.replace('\t', '    '),yield_errors())))
TYPES_MOD.write_text("\n".join(map(lambda l: l.replace('\t', '    '),yield_types())))
# Delete the file after it is used
# this ensures that the api typing module
# is always up to date
os.remove(SWAGGER_FILE)
