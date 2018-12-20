import re
from inspect import stack
optimize = False
mayDebug = True

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
def debug(text, indentToAdd=0, force = False, level =1):
    if not shouldDebug and not force:
        return
    global indentation
    glob = stack()[level].frame.f_globals
    loc = stack()[level].frame.f_locals
    text = eval(f"""f"{text}" """,glob,loc)
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

nbInsideThis = 0
def debugInsideThisMethod(fun):
    def aux_debugInsideThisMethod(*args, **kwargs):
        global nbInsideThis
        startDebug()
        nbInsideThis+=1
        ret = fun(*args, **kwargs)
        nbInsideThis -=1
        if nbInsideThis ==0:
            endDebug()
        return ret
    return aux_debugInsideThisMethod

def debugOnlyThisMethod(fun):
    return debugFun(fun, (lambda text,indentToAdd = 0: debug(text, indentToAdd, force = True, level=2)))

def assertEqual(left, right):
    if left == right:
        return True
    print(f"""\n\nReceived\n«{left}»\nwhich is distinct from expected\n«{right}»\n""")
    return False

# def assertEqualString(left, right):
#     glob = stack()[1].frame.f_globals
#     loc = stack()[1].frame.f_locals
#     # try:
#     leftEval = eval(left, glob, loc)
#     # except NameError as n:
#     #     print(f"""glob is {glob}""")
#     #     raise
#     rightEval = eval(right,glob,loc)
#     if leftEval == rightEval:
#         return True
#     print(f"""\n\n{left} evaluates as \n"{leftEval}".\n"{rightEval}"\n is the value of {right}, they are distinct.""")
#     return False

def assertType(element,types):
    if not isinstance(types,list):
        types = [types]
    for typ in types:
        if isinstance(element,typ):
            return True
    print(f""" "{element}"'s type is {type(element)}, which is not a subtype of {types}""")
    return False


def debugFun(fun, debug=debug):
    if not mayDebug:
        return fun
    def aux_debugFun(*args, **kwargs):
        nonlocal debug
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
        debug("{t}",1)
        ret = fun(*args, **kwargs)
        debug("returns {ret}",-1)
        return ret
    aux_debugFun.__name__ = f"debug_{fun.__name__}"
    aux_debugFun.__qualname__ = f"debug_{fun.__qualname__}"
    return aux_debugFun


def debugInit(fun):
    if not mayDebug:
        return fun
    def aux_debugInit(self, *args, **kwargs):
        t = f"{fun.__name__}("
        needSeparator = False
        def comma(text):
            nonlocal needSeparator, t
            if not needSeparator:
                needSeparator = True
            else:
                t+=", "
            t+=text
        isSelf = True
        for arg in args:
            if isSelf:
                isSelf = False
                continue
            comma(f"{arg}")
        for kw in kwargs:
            comma(f"{kw}={kwargs[kw]}")
        t+=")"
        debug("{t}",1)
        fun(self, *args, **kwargs)
        debug("returns {self}",-1)
    aux_debugInit.__name__ = f"debug_{fun.__name__}"
    aux_debugInit.__qualname__ = f"debug_{fun.__qualname__}"
    return aux_debugInit


class ExceptionInverse(Exception):
    def  __init__(self,text):
        self.text = "\n".join(reversed((str(text)+"\n").split("\n")))

    def __str__(self):
        return f"Exception: {self.text}"
