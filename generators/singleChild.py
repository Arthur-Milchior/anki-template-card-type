from bs4 import BeautifulSoup, NavigableString
import copy
import sys
from .constants import *
from .generators import Gen, modelToFields, shouldBeKept, genRepr, ensureReturnGen, memoize, thisClassIsClonable
from .leaf import emptyGen
from ..tag import singleTag, tagContent
from ..debug import debug, assertType, debugFun, ExceptionInverse
from .multipleChildren import MultipleChildren

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
    
@thisClassIsClonable
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
        return hash((self.tag,self.attrs,self.getChild()))

    @debugFun
    def cloneSingle(self, child):
        if child == self.getChild():
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
        #debug("self.tag = {self.tag}")
        #debug("self.attrs = {self.attrs}")
        newtag = soup.new_tag(self.tag, **self.attrs)
        #debug("New tag is {newtag}")
        self.getChild().applyTag(newtag, soup)
        #debug("New tag became {newtag}")
        tag.append(newtag)
        #debug("Tag became {tag}")

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
        
         
@thisClassIsClonable
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
            return self.getChild().assumeFieldAbsent(field)
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
            return self.getChild().restrictToModel(fields)
        

    def _applyTag(self, tag, soup):
        assert False

@thisClassIsClonable
class Present(FieldChild):
    """The class which expands only if a field is contained in a model."""
    def _assumeFieldPresent(self, field):
        if self.field == field:
            return self.getChild().assumeFieldPresent(field)
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
            return self.getChild().restrictToModel(fields)
        else:
            return emptyGen
        
    def _applyTag(self, tag, soup):
        assert False

@thisClassIsClonable
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
        self.child.applyTag(tag, soup)
        tag.append(NavigableString(f"{{{{/{self.field}}}}}"))

        
@thisClassIsClonable
class Filled(FieldChild):
    """The class which expands differently in function of the question/answer side."""
    def _assumeFieldFilled(self, field):
        if self.field == field:
            return self.getChild().assumeFieldFilled(field)
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
            #debug("self.field({self.field}) not in fields({fields})")
            return emptyGen
        else:
            return self.cloneSingle(self.getChild().restrictToModel(fields))
        
    def _applyTag(self, tag, soup):
        assert soup is not None
        tag.append(NavigableString(f"{{{{#{self.field}}}}}"))
        self.child.applyTag(tag, soup)
        tag.append(NavigableString(f"{{{{/{self.field}}}}}"))
    
@thisClassIsClonable
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
    
@thisClassIsClonable
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

@thisClassIsClonable
class Asked(FieldChild):
    """The class which expands only if its field is asked."""
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().getWithoutRedundance().assumeAsked(self.field))

    def _assumeAsked(self, field):
        if self.field == field:
            return self.getChild().assumeAsked(field)
        else:
            return self.cloneSingle(self.getChild().assumeAsked(field))
    def _assumeNotAsked(self, field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().assumeAsked(field))

    def _noMoreAsk(self):
        return None
        
    def _removeName(self, field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().removeName(field))
        
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("Asked._applyTag should not exists")

    
@thisClassIsClonable
class NotAsked(FieldChild):
    """The class which expands only if its field is not asked."""
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().getWithoutRedundance().assumeNotAsked(self.field))
    
    def _assumeNotAsked(self, field):
        if self.field == field:
            return self.getChild().assumeAsked(field)
        else:
            return self.cloneSingle(self.getChild().assumeAsked(field))

    @debugFun
    def _removeName(self, field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().removeName(field))

    def _noMoreAsk(self):
        return self.getChild().noMoreAsk()
                
    def _assumeAsked(self, field):
        if self.field == field:
            return None
        else:
            return self.getChild().assumeAsked(field)
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("NotAsked._applyTag should not exists")
    
