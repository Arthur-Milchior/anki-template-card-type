import copy
from .generator import Gen,addTypeToGenerator

class Leaf(Gen):
    def __init__(self, unRedundated = True, *args, **kwargs):
        # A leaf can never be redundant alone. 
        super().__init__(unRedundated = unRedundated, *args, **kwargs)

    def getChildren(self):
        return frozenset()
        
    def _applyRecursively(self, fun, *args, **kwargs):
        return self

class Empty(Leaf):
    """A generator without any content"""
    def __init__(self,
                 argument = None, #used because ensureGen may call empty with the argument None.
                 toKeep=False,
                 unRedundated = True,
                 normalized = True,
                 *args,
                 **kwargs):
        super().__init__(normalized = normalized,
                         unRedundated = unRedundated,
                         toKeep = toKeep,
                         *args,
                         **kwargs)

    def _template(self, *args, **kwargs):
        return None
    def __eq__(self,other):
        return isinstance(other,Leaf)

emptyGen = Empty()
addTypeToGenerator(type(None),Empty)

class Literal(Leaf):
    """A text to be printed, as-is, unconditionally."""
    def __init__(self,
                 text = None,
                 normalized = True,
                 toKeep = False,
                 toClone = None,
                 *args,
                 **kwargs):
        super().__init__(*args, toKeep = toKeep, unRedundated = True, toClone = toClone, **kwargs)
        if text is not None:
            self.text = text
        elif toClone is not None:
            self.text = toClone.text
        else:
            self.text = ""

    def __eq__(self,other):
        return isinstance(other,Literal) and self.text == other.text
            
    def _isEmpty(self):
        return not text
    
    def _template(self, tag, *args, **kwargs):
        tag.append(self.text)
        return self.text
addTypeToGenerator(str,Literal)

class Field(Leaf):
    def __init__(self,field = None, toKeep = True,toClone = None, *args, **kwargs):
        if field is not None:
            self.field = field
        elif toClone is not None:
            self.field = toClone.field
        else:
            assert False
        self.field = field
        super().__init__(normalized = True, toClone = toClone, toKeep = toKeep, *args, **kwargs)

    def __eq__(self,other):
        return isinstance(other,Field) and self.field == other.field
    
    def _isEmpty(self):
        return False
    
    def _assumeFieldInSet(self, field, setName):
        if field == self.field and (setName == "absentOfModel" or setName == "Empty"):
            return emptyGen
        return self
    
    def restrictToModel(self, model, fields = None):
        fields = fields or modeToFields(model)
        if self.field in fields:
            return self
        else:
            return emptyGen

    def _template(self, tag, *args, **kwargs):
        t = f"""{{{{{self.field}}}}}"""
        tag.append(t)
        return t
