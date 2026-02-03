import sys
sys.path.append('src')

from typing import Annotated
from typer import Typer, Option, Argument, Context

from plankapy.v2.models import *
from plankapy.v2 import Planka

app = Typer()

@app.command(name='Planka Login', no_args_is_help=True, context_settings={})
def login(
    url: Annotated[
        str, 
        Option(
            help='The base url for your planka instance',
            metavar='PLANKA_URL',
        )
    ],
    *,
    username: Annotated[
        str|None, 
        Option(
            help='Planka Username',
        )
    ]=None,
    password: Annotated[
        str|None, 
        Option(
            help='Planka Password',
        )
    ]=None,
    api_key: Annotated[
        str|None, 
        Option(
            help='Planka API Key (preferred)',
            metavar='PLANKA_API_KEY',
        )
    ]=None) -> Planka:
    """Login to a planka instance"""
    planka = Planka(url)
    planka.login(password=password, username=username, api_key=api_key)
    return planka



if __name__ == '__main__':
    app()