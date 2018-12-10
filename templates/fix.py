import sys
from ..debug import debug
from . import templates
"""The content of this tag is never changed. Neither during compilation nor during cleaning. The full template may be deleted if it occurs inside another template."""

def compile_(tag, soup = None, isQuestion = None, model = None, objects = None, frontText = None, **kwargs):
    pass

def clean(tag):
    pass
    
templates.addKindOfTemplate("fix", sys.modules[__name__])
templates.addKindOfTemplate("fixed", sys.modules[__name__])
