from ..list import MultipleChildren
from ..generators import Gen, genRepr
#, ensureReturnGen, memoize
from ..leaf import emptyGen

class SingleChild(MultipleChildren):
    def __init__(self, child = None, toKeep = None, **kwargs):
        self.child = child
        super().__init__(toKeep = toKeep, **kwargs)

    @debugFun
    def clone(self, elements):
        assert len(elements)==1
        child = elements[0]
        return self.cloneSingle(child)

    @debugFun
    def cloneSingle(self, child):
        if not child:
            return emptyGen
        if child == self.getChild():
            return self
        return self.classToClone(child = child)
    
    @debugFun
    def getChild(self):
        self.child = self._ensureGen(self.child)
        return self.child
    
    # @ensureReturnGen
    # #@debugFun
    # @memoize()
    # def getChild(self):
    #     return self.child
        
    @debugFun
    def _getChildren(self):
        return [self.getChild()]
    def __hash__(self):
        return hash((self.__class__,self.child))
    
    def _repr(self):
        space = "  "*Gen.indentation
        t= f"""{self.__class__.__name__}(
{genRepr(self.child, label="child")},{self.params()})"""
        return t
    
    def __eq__(self,other):
        """It may require to actually compute the child"""
        return isinstance(other,SingleChild) and self.getChild() == other.getChild()
    

class FieldChild(SingleChild):
    def __init__(self,
                 field,
                 child,
                 **kwargs):
        self.field = field
        assert assertType (field, str)
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
