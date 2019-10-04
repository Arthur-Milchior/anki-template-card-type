import sys

from .debug import assertType


def firstTruth(l):
    for elt in l:
        if elt:
            return elt

def identity(x):
    return x

def standardContainer(cont):
    if isinstance(cont,list) or isinstance(cont,set)  or isinstance(cont,frozenset):
        return True
    else:
        print(f"""Beware: {cont} is not a container but of type {type(cont)}.""", file=sys.stderr)

def checkField(field):
    assert assertType(field, str)
    if "{" in field or "}" in field:
        raise Exception(f"Field «{field}» contains {{ or }} thus probably unwanted")
    return True
