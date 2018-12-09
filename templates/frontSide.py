import sys
from copy import copy
from . import templates
from bs4 import NavigableString
from ..tag import tagContent
from ..debug import debug

def compile_(tag, soup = None, FrontSoup = None, **kwargs):
    #debug(f"""frontSide.compile_("{tag}","{FrontSoup}")""",1)
    assert FrontSoup is not None
    #(text, newTag) =
    newFrontSoup = copy(FrontSoup)
    templates.compile_(newFrontSoup, soup = FrontSoup, **kwargs)
    #debug(f"""newFrontSoup is "{newFrontSoup}" """)
    tag.contents = newFrontSoup.enclose.contents
    #debug(f"""tag becomes "{tag}" """)
    #newText = tagContent(tag.name, tag.attrs, text)
    #debug("",-1)

def clean(tag):
    pass
    
templates.addKindOfTemplate("Front Side", sys.modules[__name__])
