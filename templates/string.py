import sys
from ..debug import debug
from .templates import Template
from bs4 import NavigableString
from html import escape

"""Templates for string. Not clear why this would be usefull"""

def compile_(tag, *args, **kwargs):
    string = tag.attrs.get("string")
    tag.append(NavigableString(escape(string)))
    pass

def clean(tag):
    tag.clear()
    pass
    
Template(["string"], compile_, clean)
