from ..generators import Gen
from ..list import ListElement

class Parenthesis(ListElement):
    """A generator, with parenthesis around them."""
    def __init__(child, left = "(", right = ")", *args, **kwargs):
        self.child = child
        left = self._ensureGen(left).dontKeep()
        right = self._ensureGen(right).dontKeep()
        debug.__init__([left,child,right], *args, **kwargs)
