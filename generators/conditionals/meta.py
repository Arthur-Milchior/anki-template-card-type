from ..generators import Gen, genRepr, MultipleChildren, SingleChild
from ..leaf import emptyGen, Field
from ...debug import assertType

class FieldChild(SingleChild):
    def __init__(self,
                 field,
                 child,
                 **kwargs):
        if isinstance(field,Field):
            field = field.field
        self.field = field
        assert assertType (self.field, str)
        super().__init__(child, **kwargs)
        
    def cloneSingle(self, child):
        if not child:
            return emptyGen
        if child == self.getChild():
            return self
        return self.classToClone(
            field = self.field,
            child = child)
    
    # def cloneSingle(self, elements):
    #     assert len(elements) == 1
    #     child = elements[0]
    #     if not child:
    #         return emptyGen
    #     if child == self.child:
    #         return self
    #     return self.__class__(
    #         field = self.field,
    #         child = child)
    
    def _repr(self):
        space  = "  "*Gen.indentation
        return f"""{self.__class__.__name__}(
{genRepr(self.field, label = "field")},
{genRepr(self.child, label = "child")},{self.params()})"""
    
    def __eq__(self,other):
        return isinstance(other,self.classToClone) and self.field == other.field and self.getChild() == other.getChild()
    
    def __hash__(self):
        return hash((self.field,super().__hash__()))
