from ..debug import debug, debugFun
import types
import sys
typeToGenerator= dict()

def addTypeToGenerator(type,generator):
    typeToGenerator[type]=generator
    
@debugFun
def ensureGen(element, locals_ = None):
    """Element if it is a Gen, or construct it. The type is chosen
    according to typeToGenerator.

    """
    ret = None
    if locals_ is None:
        locals_ = dict()
    funs = []
    recCall = 0
    element_original = element
    for typ in typeToGenerator:
        if isinstance(element, typ):
            gen = typeToGenerator[typ]
            ret = gen(element)
            debug("{element} has type {typ}, thus use function {gen}")
            break
        else:
            debug("{element} has not type {typ}")
            pass
    if ret is None:
        print(f"{element} has type {type(element)} which we can not consider", file=sys.stderr)
        assert False
    return ret


