import traceback
import sys
import os
#from . import templates
#from .imports import *

try:
    from . import tests
except:
    st = str(traceback.format_exc())
    st = "\n".join(reversed(str(traceback.format_exc()).split("\n")))
    print(st)
    os._exit(1)
    
from . import browser

