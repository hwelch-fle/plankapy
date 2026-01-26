from .v1 import (
    Planka as Planka, 
    PasswordAuth as PasswordAuth
)
from warnings import warn

def warn_version(func):
    def inner(*args, **kwargs):
        warn('If using v1 Planka, please use from plankapy.v1 import Planka')
        return func(*args, **kwargs)
    return inner

# TODO: Make this not warn when importing using `plankapy.v1`
Planka.__init__ = warn_version(Planka.__init__)
PasswordAuth.__init__ = warn_version(PasswordAuth.__init__)
