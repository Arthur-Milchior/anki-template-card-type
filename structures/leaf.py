import copy
from .structures.child import Requirement
from .structures.generator import Gen

class Leaf(Gen):
    def __init__(self, *args, **kwargs):
        # A leaf can never be redundant alone. 
        super().__init__(unRedundanted = True, *args, **kwargs)

    def getChildren(self):
        return frozenset()

    def _applyRecursively(self, fun,*args,*kwargs):
        return self

class Empty(Leaf):
    """A generator without any content"""
    def __init__(self,
                 toKeep=False,
                 unRedundanted = True,
                 normalized = True,
                 *args,
                 **kwargs):
        super().__init__(normalized = normalized,
                         unRedundanted = unRedundanted,
                         toKeep = toKeep,
                         *args,
                         **kwargs)

    def _template(self, *args,*kwargs):
        return ""

emptyGen = Empty()

class Literal(Leaf):
    """A text to be printed, as-is, unconditionally."""
    def __init__(self,
                 text = None,
                 normalized = True,
                 toKeep = False,
                 toClone = None,
                 *args,
                 **kwargs):
        super.__init__(*args, toKeep = toKeep, unRedundanted = True, toClone = toClone, **kwargs)
        if text is not None:
            self.text = text
        elif toClone is not None:
            self.text = toClone.text
        else:
            self.text = ""
            
    def _isEmpty(self):
        return not text
    
    def _template(self, *args,*kwargs):
        return self.text

class Field(Leaf):
    def __init__(self,field = None, toKeep = True,toClone = None, *args,*kwargs):
        if field is not None:
            self.field = field
        elif toClone is not None:
            self.field = toClone.field
        else:
            assert False
        self.field = field
        super.__init__(normalized = True, toClone = toClone, toKeep = toKeep, *args,*kwargs)

    def _isEmpty(self):
        return False
    
    def _assumeFieldInSet(self, field, set):
        if field == self.fied and (set == "absentOfModel" or set == "Empty"):
            return emptyGen
        return self
    
    def restrictToModel(self,fields):
        if self.field in fields:
            return self
        else:
            return emptyGen

    def _template(self, *args,*kwargs):
        return f"""{{{{{self.field}}}}}"""
