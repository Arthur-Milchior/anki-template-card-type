import sys
from copy import copy
from .soupAndHtml import soupFromTemplate, templateFromSoup
from .templates import Template, compile_ as templateCompile
from bs4 import NavigableString
from ..tag import tagContent
from ..debug import debug

def compile_(tag, soup = None, FrontSoup = None, FrontHtml = None,  **kwargs):
    assert FrontSoup is None or FrontHtml is None
    assert FrontSoup is not None or FrontHtml is not None
    if FrontHtml is not None:
        FrontSoup = soupFromTemplate(FrontHtml)
    #debug(f"""frontSide.compile_("{tag}","{FrontSoup}")""",1)
    #(text, newTag) =
    newFrontSoup = copy(FrontSoup)
    templateCompile(newFrontSoup, soup = FrontSoup, **kwargs)
    #debug(f"""newFrontSoup is "{newFrontSoup}" """)
    tag.contents = newFrontSoup.enclose.contents
    #debug(f"""tag becomes "{tag}" """)
    #newText = tagContent(tag.name, tag.attrs, text)
    #debug("",-1)

def clean(tag):
    tag.clean()
    pass
    
Template(["Front Side"], compile_, clean)
