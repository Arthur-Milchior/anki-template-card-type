from bs4 import BeautifulSoup, NavigableString
import copy
import sys
from .constants import *
from .generators import Gen, modelToFields, shouldBeKept, genRepr
from .leaf import emptyGen
from ..tag import singleTag, tagContent
from ..debug import debug, assertType, debugFun, ExceptionInverse
from .multipleChildren import MultipleChildren

class SingleChild(MultipleChildren):
    def __init__(self, child = None, toKeep = None, **kwargs):
        self.child = child
        self.childComputed = False
        super().__init__(toKeep = toKeep, **kwargs)

    def clone(self, elements):
        assert len(elements)==1
        child = elements[0]
        return self.cloneSingle(child)

    def cloneSingle(self, child):
        if not child:
            return emptyGen
        if child == self.child:
            return self
        return self.__class__(child = child)
    
    # def cloneSingle(self, elements):
    #     assert len(elements) ==1
    #     child = elements[0]
    #     if not child:
    #         return emptyGen
    #     if child == self.child:
    #         return self
    #     return self.__class__(child = child)
    
    def getChild(self):
        if not self.childComputed:
            self.child = self._ensureGen(self.child)
            self.childComputed = True
        return self.child
        
    def getChildren(self):
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
    
class HTML(SingleChild):
    """A html tag, and its content.

    A tag directly closed, such as br or img, should have child emptyGen
    (default value). Values are escaped.
    If child is an Empty object, then toKeep is assumed to be
    true."""

    def __init__(self,
                 tag = None,
                 atom = False,
                 attrs={},
                 **kwargs):
        assert assertType(tag,str)
        self.tag = tag
        self.attrs = attrs
        toKeep = atom is True
        self.atom = atom
        super().__init__(toKeep = toKeep, **kwargs)

    @debugFun
    def isEmpty(self):
        return ((not self.atom) and self.getChild().isEmpty())

    def __hash__(self):
        return hash((self.tag,self.attrs,self.child))

    @debugFun
    def cloneSingle(self, child):
        if child == self.child:
            return self
        if not child and not self.atom:
            return emptyGen
        return HTML(tag = self.tag,
                    attrs = self.attrs,
                    child = child,
                    atom = self.atom
        )
    
    # @debugFun
    # def cloneSingle(self, elements):
    #     assert len(elements)==1
    #     element = elements[0]
    #     if element == self.child:
    #         return self
    #     if not element and not self.atom:
    #         return emptyGen
    #     return HTML(tag = self.tag,
    #                 attrs = self.attrs,
    #                 child = element,
    #                 atom = self.atom
    #     )
    
    def _repr(self):
        space = "  "*Gen.indentation
        t= f"""HTML("{self.tag}","""
        if self.attrs:
            t+= "\n"+genRepr(self.attrs, label ="attrs")+","
        if self.child:
            t+= "\n"+genRepr(self.child, label ="child")+","
        if self.atom:
            t+= "\n"+genRepr(self.atom, label ="atom")+","
        t+=self.params()+")"
        return t

    def __eq__(self,other):
        return super().__eq__(other) and isinstance(other,HTML) and self.tag == other.tag and self.attrs == other.attrs

    @debugFun
    def _applyTag(self, tag, soup):
        #debug(f"self.tag = {self.tag}")
        #debug(f"self.attrs = {self.attrs}")
        newtag = soup.new_tag(self.tag, **self.attrs)
        #debug(f"New tag is {newtag}")
        if not self.emptyTag:
            self.child.applyTag(newtag, soup)
        #debug(f"New tag became {newtag}")
        tag.append(newtag)
        #debug(f"Tag became {tag}")

class FieldChild(SingleChild):
    def __init__(self,
                 field,
                 **kwargs):
        self.field = field
        assert assertType (field, str)
        super().__init__(**kwargs)
        
    def cloneSingle(self, child):
        if not child:
            return emptyGen
        if child == self.child:
            return self
        return self.__class__(
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
        return isinstance(other,self.__class__) and self.field == other.field and self.child == other.child
    
    def __hash__(self):
        return hash((self.field,super().__hash__()))
        
         
class Absent(FieldChild):
    """The class which expends only if a field is not present in a model."""

    def _restrictToModel(self, fields):
        if self.field in fields:
            return emptyGen
        else:
            return self.cloneSingle(self.getChild().restrictToModel(fields))
    
    def _assumeFieldPresent(self, field):
        if self.field == field:
            return emptyGen
        else:
            return self.cloneSingle(self.getChild().assumeFieldPresent(field))
        
    def _assumeFieldAbsent(self, field):
        if self.field == field:
            return self.child.assumeFieldAbsent(field)
        else:
            return emptyGen
        
    def _assumeFieldFilled(self, field):
        if self.field == field:
            return emptyGen
        else:
            return self.assumeFieldFilled(field)
         
    def _getWithoutRedundance(self):
        child = self.getChild().getWithoutRedundance()
        child = child.assumeFieldAbsent(self.field)
        return self.cloneSingle(child)
        
    @debugFun
    def _restrictToModel(self,fields):
        if self.field in fields:
            return emptyGen
        else:
            return self.child.restrictToModel(fields)
        

    def _applyTag(self, tag, soup):
        assert False

class Present(FieldChild):
    """The class which expands only if a field is contained in a model."""
    def _assumeFieldPresent(self, field):
        if self.field == field:
            return self.child.assumeFieldPresent(field)
        else:
            return self.cloneSingle(self.getChild().assumeFieldPresent(field))
        
    def _assumeFieldAbsent(self, field):
        if self.field == field:
            return emptyGen
        else:
            return self.cloneSingle(self.getChild().assumeFieldAbsent(field))
        
    def _getWithoutRedundance(self):
        child = self.getChild().getWithoutRedundance()
        child = child.assumeFieldPresent(self.field)
        return self.cloneSingle(child)
        
    @debugFun
    def _restrictToModel(self,fields):
        if self.field in fields:
            return self.child.restrictToModel(fields)
        else:
            return emptyGen
        
    def _applyTag(self, tag, soup):
        assert False

class Empty(FieldChild):
    """The class which expands differently in function of the question/answer side."""
    def _assumeFieldFilled(self, field):
        if self.field == field:
            return emptyGen
        else:
            return self.cloneSingle(self.getChild().assumeFieldFilled(field))
        
    def _assumeFieldEmpty(self, field):
        if self.field == field:
            return self.getChild().assumeFieldEmpty(field)
        else:
            return self.cloneSingle(self.getChild().assumeFieldEmpty(field))
        
    def _assumeFieldAbsent(self, field):
        if self.field == field:
            return self.getChild().assumeFieldEmpty(field)
        else:
            return self.cloneSingle(self.getChild().assumeFieldEmpty(field))
         
    def _restrictToModel(self, fields):
        if self.field in fields:
            return self.cloneSingle(self.getChild().restrictToModel(fields))
        else:
            return self.getChild().restrictToModel(fields)
    
    def _getWithoutRedundance(self):
        child = self.getChild().getWithoutRedundance()
        child =child.assumeFieldEmpty(self.field)
        return self.cloneSingle(child)

    def _applyTag(self, tag, soup):
        assert soup is not None
        tag.append(NavigableString(f"{{{{^{self.field}}}}}"))
        self.empty.applyTag(tag, soup)
        tag.append(NavigableString(f"{{{{/{self.field}}}}}"))

        
class Filled(FieldChild):
    """The class which expands differently in function of the question/answer side."""
    def _assumeFieldFilled(self, field):
        if self.field == field:
            return self.child.assumeFieldFilled(field)
        else:
            return self.cloneSingle(self.getChild().assumeFieldFilled(field))
        
    def _assumeFieldEmpty(self, field):
        if self.field == field:
            return emptyGen
        else:
            return self.cloneSingle(self.getChild().assumeFieldEmpty(field))
        
    def _assumeFieldAbsent(self, field):
        if self.field == field:
            return self.empty
        else:
            return self.cloneSingle(self.getChild().assumeFieldEmpty(field))
         
    def _getWithoutRedundance(self):
        child = self.getChild().getWithoutRedundance()
        child = child.assumeFieldFilled(self.field)
        return self.cloneSingle(child)
        
    @debugFun
    def _restrictToModel(self,fields):
        if self.field not in fields:
            #debug(f"self.field({self.field}) not in fields({fields})")
            return emptyGen
        else:
            return self.cloneSingle(self.child.restrictToModel(fields))
        
    def _applyTag(self, tag, soup):
        assert soup is not None
        tag.append(NavigableString(f"{{{{#{self.field}}}}}"))
        self.filled.applyTag(tag, soup)
        tag.append(NavigableString(f"{{{{/{self.field}}}}}"))
    
class Question(SingleChild):
    """The class which expands only on the question side"""
    def _assumeQuestion(self, changeStep = False):
        return self.getChild().assumeQuestion(changeStep = changeStep)
    def _assumeAnswer(self, changeStep = False):
        return emptyGen
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("At this stage, Question must be removed")
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().assumeQuestion())
    
class Answer(SingleChild):
    """The class which  expands only on the answer side."""
    @debugFun
    def _assumeQuestion(self, changeStep = False):
        return emptyGen
    def _assumeAnswer(self, changeStep = False):
        return self.getChild().assumeAnswer(changeStep = changeStep)
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("At this stage, Answer must be removed")
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().assumeAnswer())

class Asked(SingleChild):
    """The class which expands differently in function of whether name is asked, hidden, neither."""
    def __init__(self,
                 name = None,
                 cascadeAsked = frozenset(),
                 **kwargs):
        assert assertType(name, str)
        assert assertType(cascadeAsked, frozenset)
        for cascading in cascadeAsked:
            assert assertType(cascading, str)
        self.name = name
        self.cascadeAsked = cascadeAsked
        super().__init__(**kwargs)

    def cloneSingle(self, child):
        if not child:
            return emptyGen
        if child == self.child:
            return self
        return Asked(name = self.name,
                     child = child,
                     cascadeAsked = self.cascadeAsked)

    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().assumeAsked(self.name)).getWithoutRedundance()

    def _assumeAsked(self, name):
        if self.name == name:
            return self.getChild().assumeAsked(name)
        else:
            return self.cloneSingle(self.getChild().assumeAsked(name))
    def _assumeNotAsked(self, name):
        if self.name == name:
            return None
        else:
            return self.getChild().assumeAsked(name)
    
    def _repr(self):
        space = "  " * Gen.indentation
        t= f"""Asked(name = "{self.name}",
{genRepr(self.child, label = "child")}"""
        if self.cascadeAsked:
            t+=f""",\n{genRepr(self.cascadeAsked,"cascadeAsked")}"""
        t+=")"
        return t
    
    def __eq__(self,other):
        return isinstance(other,Asked) and self.name == other.name and self.child == other.child and self.cascadeAsked == other.cascadeAsked
    
    def _template(self, asked = frozenset(), hide = frozenset()):
        if self.name in hide:
            return None
        if self.name in asked:
            asked = asked | self.cascadeAsked
            return child.template(asked = asked, hide = hide)
        else:
            return None
        
        
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("Name._applyTag should not exists")
class NotAsked(SingleChild):
    """The class which expands differently in function of whether name is asked, hidden, neither."""
    def __init__(self,
                 name = None,
                  **kwargs):
        assert assertType(name, str)

        self.name = name
        self.notAsked = notAsked
        super().__init__(**kwargs)

    def cloneSingle(self, child):
        if not child:
            return emptyGen
        if child == self.child:
            return self
        return NotAsked(name = self.name,
                     child = child)
       
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().assumeNotAsked(self.name)).getWithoutRedundance()
    
    def _assumeNotAsked(self, name):
        if self.name == name:
            return self.getChild().assumeAsked(name)
        else:
            return self.cloneSingle(self.getChild().assumeAsked(name))
    def _assumeAsked(self, name):
        if self.name == name:
            return None
        else:
            return self.getChild().assumeAsked(name)
    
    def _repr(self):
        space = "  " * Gen.indentation
        t= f"""NotAsked(name = "{self.name}",
{genRepr(self.child, label = "child")}"""
        t+=")"
        return t
    
    def __eq__(self,other):
        return isinstance(other,NotAsked) and self.name == other.name and self.child == other.child
    
    def _template(self, asked = frozenset(), hide = frozenset()):
        if self.name in hide:
            return None
        if self.name in asked:
            return None
        return self.child.template(asked = asked, hide = hide)
        
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("Name._applyTag should not exists")
    
