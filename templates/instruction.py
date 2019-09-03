import sys

from ..debug import debug
from .templates import Template


def compile_(*args, objects = None, **kwargs):
    if objects is None:
        objects = dict()
    instr = tag.get("instr")
    if instr:
        exec(instr, globals(), objects)
    pass

def clean(tag):
    pass
    
Template(["instructions","instr"], compile_, clean)
