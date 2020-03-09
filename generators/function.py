import types

from ..debug import debugFun, debugInit
from .ensureGen import addTypeToGenerator
from .generators import Gen


class Function(Gen):
    @debugInit
    def __init__(self,
                 fun,
                 value=None,
                 processed=None):
        self.value = value
        if processed is None:
            self.processed = value is not None
        else:
            self.processed = processed
        self.fun = fun
        super().__init__()

    def _repr(self):
        if self.processed:
            return f"""Function({self.value})"""
        else:
            return f"""Function({self.fun})"""

    def __hash__(self):
        return hash(self.fun)

    def _innerEq(self, other):
        return self.fun == other.fun

    def _outerEq(self, other):
        return isinstance(other, Function) and super().__outerEq(self, other)

    def _firstDifference(self, other):
        return None

    @debugFun
    def _callOnChildren(self, *args, **kwargs):
        value = self.getValue()
        return value.callOnChildren(*args, **kwargs)

    @debugFun
    def _createHtml(self, soup):
        return self.getValue().createHtml(soup)

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
