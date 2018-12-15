from ..debug import debug, debugFun
import types
typeToGenerator= dict()

def addTypeToGenerator(type,generator):
    typeToGenerator[type]=generator
    
@debugFun
def ensureGen(element, locals_ = None):
    """Element if it is a Gen, or construct it. The type is chosen
    according to typeToGenerator.

    """
    #debug(f"ensureGen({element})", 1)
    ret = None
    if locals_ is None:
        locals_ = dict()
    funs = []
    recCall = 0
    element_original = element
    while isinstance(element,types.FunctionType) or isinstance(element,types.BuiltinFunctionType):
        funs.append(element)
        recCall+=1
        element = eval("element()",globals(),)
        if recCall == 10:
            raise Exception(f"10 successive recursive call during processing of {element_original}. 10 th is {element}")
        if element in funs:
            raise Exception(f"Loop during processing of {element_original}, raising multiple time {elements}.")
    for typ in typeToGenerator:
        if isinstance(element, typ):
            gen = typeToGenerator[typ]
            ret = gen(element)
            #debug(f"has type {typ}, thus use type {gen} and become {ret}", -1)
            break
        else:
            #debug(f"has not type {typ}")
            pass
    if ret is None:
        #debug("has no type we can consider", -1)
        assert False
    return ret

