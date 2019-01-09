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
        
    def _cloneSingle(self, child):
        return self.classToClone(
            field = self.field,
            child = child)
    
    def _repr(self):
        space  = "  "*Gen.indentation
        return f"""{self.__class__.__name__}(
{genRepr(self.field, label = "field")},
{genRepr(self.child, label = "child")},{self.params()})"""
    
    def _outerEq(self,other):
        return isinstance(other,self.classToClone) and self.field == other.field
    
    def __hash__(self):
        return hash((self.field,super().__hash__()))
