import sys
from html import escape

from bs4 import NavigableString

from ..debug import debug
from .templates import Template

"""Templates for string. Not clear why this would be usefull"""

def compile_(tag, *args, **kwargs):
    string = tag.attrs.get("string")
    tag.append(NavigableString(escape(string)))
    pass

def clean(tag):
    tag.clear()
    pass
    
Template(["string"], compile_, clean)
