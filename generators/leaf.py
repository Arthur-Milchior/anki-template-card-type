import copy
from .generators import Gen,addTypeToGenerator, modelToFields
from ..debug import debug, assertType
from bs4 import NavigableString
from html import escape

class Leaf(Gen):
    def __init__(self,  containsRedundant = True, **kwargs):
        # A leaf can never be redundant alone. 
        super().__init__(containsRedundant = containsRedundant,  **kwargs)
        
    def getChildren(self):
        return frozenset()
        
    def _applyRecursively(self, fun,  **kwargs):
        return self

class Empty(Leaf):
    """A generator without any content"""
    instance = None
    def __init__(self,
                 *args,#required, because EnsureGen may give an argument
                 toKeep=False,
                 containsRedundant = True,
                 isNormal = True,
                 isEmpty = True,
                 createOther = False,
                 init = False,
                 **kwargs):
        if createOther:
            pass
        elif Empty.instance is None and init:
            Empty.instance = self
        else:
            raise Exception("Calling Empty")
        super().__init__(isNormal = isNormal,
                         containsRedundant = containsRedundant,
                         toKeep = toKeep,
                         isEmpty = isEmpty,
                         **kwargs)

    def __repr__(self):
        if self == emptyGen:
            return "emptyGen"
        else:
            return f"""Empty(createOther = True, {self.params()})"""

    def _template(self, *args,  **kwargs):
        return None
    
    def __eq__(self,other):
        #debug(f"{self!r} == {other!r}",1)
        l = isinstance(other,Empty)
        #if l:
            #debug("other is Empty")
        #else:
            #debug("other is not Empty but {type(other)}")
        #debug("",-1)
        return l

emptyGen = Empty(init = True)
addTypeToGenerator(type(None),lambda x: emptyGen)

class Literal(Leaf):
    """A text to be printed, as-is, unconditionally."""
    def __init__(self,
                 text = None,
                 isNormal = True,
                 toKeep = False,
                 toClone = None,
                 isEmpty = None,
                 **kwargs):
        super().__init__(
                         toKeep = toKeep,
                         containsRedundant = True,
                         toClone = toClone,
                         isEmpty = isEmpty or (isEmpty is None and not text),
                         **kwargs)
        if text is not None:
            self.text = text
        elif toClone is not None and isinstance(toClone,Literal):
            self.text = toClone.text
        else:
            self.text = ""

    def __repr__(self):
        return f"""Literal(text = "{self.text}", {self.params()})"""
    
    def __eq__(self,other):
        #debug(f"""{self!r} == {other!r}, self being Literal""",1)
        if not isinstance(other,Literal):
            #debug("other is not a Literal")
            ret= False
        elif self.text != other.text:
            #debug(f"{self.text} is distinct from {other.text}")
            ret= False
        else:
            #debug(f"they are equal")
            ret = True
        #debug("",-1)
        return ret
    
    def _template(self, tag, *args, **kwargs):
        #debug(f"appending text {self.text} to {tag}")
        tag.append(NavigableString(escape(self.text)))
        #return self.text
    
addTypeToGenerator(str,Literal)

class Field(Leaf):
    def __init__(self,
                 field = None,
                 toKeep = True,
                 toClone = None,
                 isEmpty = False,
                 **kwargs):
        if field is not None:
            assert assertType(field,str)
            self.field = field
        elif toClone is not None and isinstance(toClone,Field):
            self.field = toClone.field
        else:
            assert False
        self.field = field
        super().__init__(isNormal = True,
                         isEmpty = isEmpty,
                         toClone = toClone,
                         toKeep = toKeep,
                         
                         **kwargs)

    def __eq__(self,other):
        return isinstance(other,Field) and self.field == other.field
    
    def __repr__(self):
        return f"""Field(field = "{self.field}", {self.params()})"""
    
    def _assumeFieldInSet(self, field, setName):
        if field == self.field and (setName == "absentOfModel" or setName == "Empty"):
            return emptyGen
        return self
    
    def _restrictToModel(self, model, fields = None):
        #debug(f"""{self}.restrictToModel({model["name"]}, {fields})""",1)
        if not fields:
            fields = modelToFields(model)
            #debug(f"""Fields is None, become {fields}""")
        if self.field in fields:
            #debug(f"""Field {self.field} in fields""")
            ret = self
        else:
            #debug(f"""Field {self.field} not in fields""")
            ret =emptyGen
        #debug(f"restrictToModel() returns {ret}",-1)
        return ret

    def _template(self, tag, *args, **kwargs):
        t = f"""{{{{{self.field}}}}}"""
        tag.append(t)
        return t
