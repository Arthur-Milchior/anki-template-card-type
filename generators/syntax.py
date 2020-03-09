from .generators import SingleChild
from .listGen import ListElement


class Parenthesis(SingleChild):
    """A generator, with parenthesis around them."""

    def __init__(self, child, left="(", right=")", *args, **kwargs):
        super().__init__(child=child, *args, **kwargs)
        self.left = self._ensureGen(left)
        self.right = self._ensureGen(right)
        self.left.dontKeep()
        self.right.dontKeep()

    def _getNormalForm(self):
        return self._ensureGen([self.left, self.child, self.right]).getNormalForm()
