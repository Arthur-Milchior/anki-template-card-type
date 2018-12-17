import copy
import types
from .constants import *
from .generators import Gen, modelToFields, modelToFields
from .ensureGen import addTypeToGenerator
from ..debug import debug, assertType, debugFun, ExceptionInverse
from bs4 import NavigableString
from html import escape

class Leaf(Gen):
    """
    The class of generators with no child.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @debugFun
    def getChildren(self):
        return frozenset()

    @debugFun
    def clone(self, elements = []):
        assert elements == []
        return self

emptyGen = None
class Empty(Leaf):
    """A generator without any content"""
    instance = None
    def __hash__(self):
        return 0
    def __init__(self,
                 *args,#required, because EnsureGen may give an argument
                 toKeep=False,
                 state = EMPTY,
                 createOther = False,
                 init = None,
                 **kwargs):
        if createOther:
            pass
        elif Empty.instance is None and init:
            Empty.instance = self
        else:
             raise ExceptionInverse("Calling Empty")
        super().__init__(state = state,
                         toKeep = toKeep,
                         **kwargs)
    
    def __repr__(self):
        if self == emptyGen:
            return "emptyGen"
        else:
            return f"""Empty(createOther = True, {self.params()})"""

    def _applyTag(self, tag, soup):
        pass
    
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
def constEmpty(x):
    return emptyGen
addTypeToGenerator(type(None),constEmpty)

class Literal(Leaf):
    """A text to be printed, as-is, unconditionally."""
    def __init__(self,
                 text = None,
                 state = TEMPLATE_APPLIED,
                 **kwargs):
        if text is None:
            text = ""
        self.text = text
        if not self.text:
            state == EMPTY
        super().__init__(state = state,
                         **kwargs)
    
    def __hash__(self):
        return hash(self.text)

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
    
    def _applyTag(self, tag, soup):
        #debug(f"appending text {self.text} to {tag}")
        tag.append(NavigableString(escape(self.text)))
        #return self.text
addTypeToGenerator(str,Literal)

class Field(Leaf):
    def __init__(self,
                 field = None,
                 toKeep = True,
                 typ = None,
                 cloze = None,
                 state = WITHOUT_REDUNDANCY,
                 **kwargs):
        if typ is None:
            typ = False
        if cloze is None:
            cloze = False
        self.typ = typ
        self.cloze = cloze
        if isinstance(field,Field):
            field = field.field
        elif isinstance(field,set):#required so that {{foo}} becomes Field(foo)
            assert len(field)==1
            elt = s.pop()
            s.add(elt)
            assert len(elt) == 1
            field = elt.pop
            elt.add(field)
        else:
            assert assertType(field, str)
        self.field = field
        super().__init__(state = state,
                         toKeep = toKeep,
                         **kwargs)
    def __hash__(self):
        return hash(self.field)

    def __eq__(self,other):
        return isinstance(other,Field) and self.field == other.field
    
    def __repr__(self):
        return f"""Field(field = "{self.field}", type = {self.typ}, cloze = {self.cloze}, {self.params()})"""

    def _assumeFieldEmpty(field):
        if field == self.field:
            return emptyGen
        else:
            return self
    def _assumeFieldAbsent(field):
        if field == self.field:
            return emptyGen
        else:
            return self
    @debugFun
    def _restrictToModel(self, fields):
        if self.field in fields:
            ret = self
        else:
            #debug(f"""Field {self.field} not in fields""")
            ret =emptyGen
        return ret
            
    def _applyTag(self, tag, *args, **kwargs):
        typ = "type:" if self.typ else ""
        cloze = "cloze:" if self.typ else ""
        t = NavigableString(f"""{{{{{typ}{cloze}{self.field}}}}}""")
        tag.append(t)

addTypeToGenerator(set, Field)


