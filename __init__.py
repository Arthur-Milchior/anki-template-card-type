import os
import sys
import traceback

from . import browser

#from . import templates
#from .imports import *

try:
    from . import tests
except:
    st = str(traceback.format_exc())
    st = "\n".join(reversed(str(traceback.format_exc()).split("\n")))
    print(st)
    os._exit(1)
