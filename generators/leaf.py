import copy
import types
from .constants import *
from .generators import Gen, modelToFields, modelToFields, genRepr, thisClassIsClonable
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
    def _getChildren(self):
        return frozenset()

    @debugFun
    def clone(self, elements = []):
        assert elements == []
        return self
    def _outerEq(self,other):
        return self==other
    def _firstDifference(self,other):
        return None
    

emptyGen = None
@thisClassIsClonable
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
    
    def _repr(self):
        if self == emptyGen:
            return "emptyGen"
        else:
            return f"""Empty(createOther = True,{self.params()})"""

    def _applyTag(self, soup):
        return None
    
    def __eq__(self,other):
        #debug("{self!r} == {other!r}",1)
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

@thisClassIsClonable
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

    def _repr(self):
            return f"""Literal(text = "{self.text}",{self.params()})"""
    
    def __eq__(self,other):
        if not isinstance(other,Literal):
            return False
        return self.text == other.text
    
    def _applyTag(self, soup):
        #debug("appending text {self.text} to {tag}")
        return NavigableString(escape(self.text))
        #return self.text
addTypeToGenerator(str,Literal)

@thisClassIsClonable
class Field(Leaf):
    def __init__(self,
                 field = None,
                 toKeep = True,
                 typ = None,
                 cloze = None,
                 state = WITHOUT_REDUNDANCY,
                 special = False,
                 **kwargs):
        self.special = special
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
        self.field = field
        assert assertType(field, str)
        self.dealWithClozeAndType()
        self.dealWithSpecial()
        super().__init__(state = state,
                         toKeep = toKeep,
                         **kwargs)
        

    def dealWithClozeAndType(self):
        if self.field.startswith("type:"):
            print(f"""Beware: you used "type:" in prefix of your field name. Please use "typ= True" in the Field object creator instead. "type:" is removed from the name.""", file=sys.stderr)
            self.typ = True
            self.field = self.field[5:]
        if self.field.startswith("cloze:"):
            print(f"""Beware: you used "cloze:" in prefix of your field name. Please use "cloze= True" in the Field object creator instead. "cloze:" is removed from the name.""", file=sys.stderr)
            self.cloze = True
            self.field = self.field[6:]
        
    def dealWithSpecial(self):
        specialName = self.field in {"FrontSide":"frontside", "Tags":"tags", "Type":"typ", "Deck":"deck", "Card":"card"}
        if specialName and not self.special:
            print(f"""Beware: you use field "{self.field}", which is a special field. If you want to use this special field, use the constant "{specialName(self.field)}".""", file=sys.stderr)
        if not self.special and specialName:
            print(f"""Beware: you want to create a special field, which does not belong to {specialName}, thus is not a special name.""", file=sys.stderr)
        if self.special:
            if self.typ:
                print(f"""Beware: you want to have "type:" before a special field {self.field}, this makes no sens.""", file=sys.stderr)
            if self.typ:
                print(f"""Beware: you want to have "cloze:" before a special field {self.field}, this makes no sens.""", file=sys.stderr)
                
            
        
        
    def __hash__(self):
        return hash(self.field)

    def __eq__(self,other):
        return isinstance(other,Field) and self.field == other.field
    
    def _repr(self):
        t= f"""Field(field = "{self.field}","""
        if self.typ:
            t+="\n"+genRepr(self.typ, label="type")+","
        if self.cloze:
            t+="\n"+genRepr(self.cloze, label="cloze")+","
        if self.special:
            t+="\n"+genRepr(self.special, label="special")+","
        t+=self.params()+")"
        return t

    def _assumeFieldEmpty(field):
        if field == self.field:
            if self.special:
                print(f"""Beware: you assert that special name {self.field} is empty, which makes no sens.""", file=sys.stderr)
            return emptyGen
        else:
            return self
    def _assumeFieldAbsent(field):
        if field == self.field:
            if self.special:
                print(f"""Beware: you assert that special name {self.field} is absent, which makes no sens.""", file=sys.stderr)
            return emptyGen
        else:
            return self
    @debugFun
    def _restrictToModel(self, fields):
        if self.field in fields:
            if self.special:
                print(f"""Beware: your model has a field {self.field} which is also the name of a special field.""", file=sys.stderr)
            ret = self
        else:
            #debug("""Field {self.field} not in fields""")
            ret =emptyGen
        return ret
            
    def _applyTag(self, *args, **kwargs):
        typ = "type:" if self.typ else ""
        cloze = "cloze:" if self.typ else ""
        return NavigableString(f"""{{{{{typ}{cloze}{self.field}}}}}""")

addTypeToGenerator(set, Field)
frontside = Field("FrontSide", special = True)
tags = Field("Tags", special = True)
typ = Field("Type", special = True)
deck = Field("Deck", special = True)
card = Field("Card", special = True)


