import sys
from ..debug import debug
from . import templates
from bs4 import NavigableString
"""Templates for string. Not clear why this would be usefull"""

def compile_(tag, *args, **kwargs):
    string = tag.attrs.get("string")
    tag.append(NavigableString(string))
    pass

def clean(tag):
    tag.clear()
    pass
    
templates.addKindOfTemplate("string", sys.modules[__name__])
