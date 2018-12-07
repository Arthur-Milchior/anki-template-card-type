import copy
from .generators import Gen,addTypeToGenerator, modelToFields
from ..debug import debug

class Leaf(Gen):
    def __init__(self, containsRedundant = True, *args, **kwargs):
        # A leaf can never be redundant alone. 
        super().__init__(containsRedundant = containsRedundant, *args, **kwargs)
        
    def getChildren(self):
        return frozenset()
        
    def _applyRecursively(self, fun, *args, **kwargs):
        return self

class Empty(Leaf):
    """A generator without any content"""
    def __init__(self,
                 argument = None,
                 toKeep=False,
                 containsRedundant = True,
                 isNormal = True,
                 *args,
                 **kwargs):
        super().__init__(isNormal = isNormal,
                         containsRedundant = containsRedundant,
                         toKeep = toKeep,
                         *args,
                         **kwargs)

    def __repr__(self):
        return f"""Empty({self.params()})"""

    def _template(self, *args, **kwargs):
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

emptyGen = Empty()
addTypeToGenerator(type(None),Empty)

class Literal(Leaf):
    """A text to be printed, as-is, unconditionally."""
    def __init__(self,
                 text = None,
                 isNormal = True,
                 toKeep = False,
                 toClone = None,
                 isEmpty = None,
                 *args,
                 **kwargs):
        super().__init__(*args,
                         toKeep = toKeep,
                         containsRedundant = True,
                         toClone = toClone,
                         isEmpty = isEmpty or (isEmpty is None and not text),
                         **kwargs)
        if text is not None:
            self.text = text
        elif toClone is not None:
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
        tag.append(self.text)
        return self.text
addTypeToGenerator(str,Literal)

class Field(Leaf):
    def __init__(self,
                 field = None,
                 toKeep = True,
                 toClone = None,
                 isEmpty = False,
                 *args,
                 **kwargs):
        if field is not None:
            self.field = field
        elif toClone is not None:
            self.field = toClone.field
        else:
            assert False
        self.field = field
        super().__init__(isNormal = True,
                         isEmpty = isEmpty,
                         toClone = toClone,
                         toKeep = toKeep,
                         *args,
                         **kwargs)

    def __eq__(self,other):
        return isinstance(other,Field) and self.field == other.field
    
    def __repr__(self):
        return f"""Field(field = "{self.field}", {self.params()})"""
    
    def _assumeFieldInSet(self, field, setName):
        if field == self.field and (setName == "absentOfModel" or setName == "Empty"):
            return emptyGen
        return self
    
    def restrictToModel(self, model, fields = None):
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
