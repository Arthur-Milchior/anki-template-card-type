from ..generators import Gen
from ..list import ListElement

class Parenthesis(ListElement):
    """A generator, with parenthesis around them."""
    def __init__(child, left = "(", right = ")", *args, **kwargs):
        self.child = child
        debug.__init__([left,child,right], *args, **kwargs)
