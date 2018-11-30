import copy
from .structures import Gen
from .leaf import empty

class SingleChild(Gen):
    def __init__(self, child, *args, **kwargs):
        self.child = child
        super().__init__( *args, **kwargs)

    def _getNormalForm(self):
        self.normalizedChild = self.child.getNormalForm()
        

        
class Requirement(SingleChild):
    """Ask child, if all elements of present are present, and those of absent are absent.

    An element of present already parent's present

    """
    def __init__(self,
                 child,
                 requireds = frozenset(),
                 forbidden = frozenset(),
                 *args,
                 **kwargs):
        # newPresent =requireds  - self.presentFixedInParent()
        # newAbsent = absent - self.presentFixedInParent()
        #present = newPresent, absent = newAbsent,
        super().__init__(child,*args, **kwargs)
        self.requireds = requireds
        self.forbidden = forbidden
        #self.contradiction = (requireds & self.absentInParent()) or (forbidden & self.presentInParent())

    def _getNormalForm(self):
        super().normalize()
        normal = copy.copy(self)
        normal.normalized = True
        normal.child = self.normalizedChild
        return normal
        
    def _toKeep(self):
        return self.child.toKeep()
        
    def _mustache(self,asked = None, question = None):
        t = self.child.mustache(asked = asked, question = question)
        if not t:
            return ""
        for (set, symbol) in [
                (self.requireds,"#"),
                (self.rejecteds,"^")
        ]:
            for element in set:
                t = f"{{{{{symbol}{element}}}}}{t}{{{{/{element}}}}}"
        return t

    def _restrictFields(self, fields, empty, hasContent):
        if (self.forbidden & hasContent) or (self.requireds & empty) or (self.requireds - fields):
            return empty
        considered = (empty|hasContent)
        childRestricted = self.child.restrictFields(fields,empty|forbidden,hasContent|requireds)
        if not childRestricted:
            return empty
        return Requirements(child=childRestricted, requireds = self.requireds - considered, forbidden = (self.forbidden - considered) & fields, normalized = True)
