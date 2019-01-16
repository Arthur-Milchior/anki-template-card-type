from ..generators import Gen, genRepr, MultipleChildren, SingleChild, NotNormal
from ..leaf import emptyGen, Field
from ..list import ListElement
from ...debug import assertType
import sys
from ...utils import checkField

class FieldChild(SingleChild):
    def __init__(self,
                 field,
                 child,
                 isMandatory = False,
                 **kwargs):
        if isinstance(field,Field):
            field = field.field
        checkField(field)
        self.field = field
        assert assertType (self.field, str)
        super().__init__(child,
                         localMandatories = {field} if isMandatory else frozenset(),
                         **kwargs)
        
    def _removeName(self, field):
        checkField(field)
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().removeName(field))
        
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
        return isinstance(other,self.classToClone) and self.field == other.field and super()._outerEq(other)
    
    def __hash__(self):
        return hash((self.field,super().__hash__()))

    
def Dichotomy(positiveClass,negativeClass,name=""):
    # def init(field, positiveCase, negativeCase, *args, isMandatory = False):
    #     mandatories = {field} if isMandatory else frozenset() 
    #     return ListElement([positiveClass(field, positiveCase, isMandatory=isMandatory),
    #                         negativeClass(field, negativeCase, isMandatory=isMandatory)])
    class Foo(ListElement):        
        def __init__(self, field, positiveCase, negativeCase, *args, isMandatory = False, **kwargs):
            self.positiveCase = positiveCase
            self.negativeCase = negativeCase
            self.field = field
            self.isMandatory = isMandatory
            self.mandatories = {self.field} if self.isMandatory else frozenset()
            pos = positiveClass(self.field,
                                self.positiveCase,
                                isMandatory=self.isMandatory)
            neg = negativeClass(self.field,
                                self.negativeCase,
                                isMandatory=self.isMandatory)
            super().__init__([pos, neg])
    Foo.__name__ = name
    return Foo
