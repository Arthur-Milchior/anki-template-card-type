import re
from inspect import stack

shouldDebug = False
def startDebug():
    global shouldDebug
    shouldDebug = True
    print("Debug started")
def endDebug():
    global shouldDebug
    shouldDebug = False
    print("Debug ended")
    
indentation = 0
def debug(text, indentToAdd=0):
    if not shouldDebug:
        return
    global indentation
    indentToPrint = indentation
    t = " "*indentToPrint
    if indentToAdd>0:
        t+= "{<"
    space = " "
    newline = "\n"
    t+= re.sub(newline,newline+space,text)
    print (t)
    indentation +=indentToAdd
    if indentToAdd<0:
        indentToPrint +=indentToAdd
        print((" "*indentToPrint)+">}")




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
    print(f"""\n\n{left} evaluates as \n"{leftEval}".\n"{rightEval}"\n is the value of {right}, they are distinct.""")
    return False

def assertType(element,types):
    if not isinstance(types,list):
        types = [types]
    for typ in types:
        if isinstance(element,typ):
            return True
    print(f""" "{element}"'s type is {type(element)}, which is not a subtype of {types}""")
    return False


def debugFun(fun):
    def aux(*args, **kwargs):
        t = f"{fun.__qualname__}("
        first = False
        def comma(text):
            nonlocal first, t
            if not first:
                first = True
            else:
                t+=", "
            t+=text
        for arg in args:
            comma(f"{arg}")
        for kw in kwargs:
            comma(f"{kw}={kwargs[kw]}")
        t+=")"
        debug(f"{t}",1)
        ret = fun(*args, **kwargs)
        debug(f"returns {ret}",-1)
        return ret
    aux.__name__ = f"debug_{fun.__name__}"
    aux.__qualname__ = f"debug_{fun.__qualname__}"
    return aux


