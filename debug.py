import re
from inspect import stack

indentation = 0
def debug(text, indentToAdd=0):
    global indentation
    indentToPrint = indentation
    if indentToAdd>0:
        sep = "{"
    elif indentToAdd==0:
        sep = ""
    else:
        sep = "}"
        indentToPrint -=1
    space = " "*indentToPrint
    newline = "\n"
    print (f"""{space}{sep}{re.sub(newline,newline+space,text)}""")
    indentation +=indentToAdd
    pass


def assertEqual(left, right):
    glob = stack()[1].frame.f_globals
    leftEval = eval(left,glob)
    rightEval = eval(right,glob)
    if leftEval == rightEval:
        return True
    debug(f"""{left} evaluates as \n"{leftEval}".\n"{rightEval}"\n is the value of {right}, they are distinct.""")
    return False

def assertType(element,typ):
    if isinstance(element,typ):
        return True
    else:
        debug(f""" "{element}"'s type is {type(element)}, which is not a subtype of {typ}""")
        return False
