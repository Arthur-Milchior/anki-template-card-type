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
    loc = stack()[1].frame.f_locals
    # try:
    leftEval = eval(left, glob, loc)
    # except NameError as n:
    #     print(f"""glob is {glob}""")
    #     raise
    rightEval = eval(right,glob,loc)
    if leftEval == rightEval:
        return True
    debug(f"""{left} evaluates as \n"{leftEval}".\n"{rightEval}"\n is the value of {right}, they are distinct.""")
    return False

def assertType(element,types):
    if not isinstance(types,list):
        types = [types]
    for typ in types:
        if isinstance(element,typ):
            return True
    debug(f""" "{element}"'s type is {type(element)}, which is not a subtype of {types}""")
    return False
