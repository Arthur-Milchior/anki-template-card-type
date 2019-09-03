import sys
from copy import copy

from bs4 import NavigableString

from ..debug import debug
from ..tag import tagContent
from .soupAndHtml import soupFromTemplate, templateFromSoup
from .templates import Template
from .templates import compile_ as templateCompile


def compile_(tag, soup = None, FrontSoup = None, FrontHtml = None,  **kwargs):
    """We should receive the front either as HTML string or as a soup. Soup will be generated if we get html. If both are None, the front is empty"""
    assert FrontSoup is None or FrontHtml is None
    assert tag is not None
    if FrontHtml is not None:
        FrontSoup = soupFromTemplate(FrontHtml)
    if FrontSoup is None:
        return
    newFrontSoup = copy(FrontSoup)
    templateCompile(newFrontSoup, soup = FrontSoup, recompile=True, **kwargs)
    tag.contents = newFrontSoup.contents


def clean(tag):
    tag.clear()
    pass
    
Template(["Front Side"], compile_, clean)
