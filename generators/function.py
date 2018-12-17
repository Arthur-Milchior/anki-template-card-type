from .generators import Gen
from .ensureGen import addTypeToGenerator
from ..debug import debugFun, debugInit
import types

class Function(Gen):
    @debugInit
    def __init__(self,
                 fun,
                 value = None,
                 processed = None):
        self.value = value
        if processed is None:
            self.processed = value is not None
        else:
            self.processed = processed
        self.fun = fun
        super().__init__()

    def __repr__(self):
        if self.processed:
            return f"""Function({self.value})"""
        else:            
            return f"""Function({self.fun})"""

    def __hash__(self):
        return hash(self.fun)

    def __eq__(self, other):
        return isinstance(other, Function) and self.fun == other.fun

    @debugFun
    def _callOnChildren(self, *args, **kwargs):
        value = self.getValue()
        return value.callOnChildren(*args, **kwargs)

    @debugFun
    def _applyTag(self, tag, soup):
        self.getValue().applyTag(tag, soup)
        
    @debugFun
    def getState(self):
        return self.getValue().getState()
    
    @debugFun
    def getValue(self):
        if not self.processed:
            self.value = self.fun()
            self.processed = True
        return self.value

addTypeToGenerator(types.FunctionType, Function)
addTypeToGenerator(types.BuiltinFunctionType, Function)
