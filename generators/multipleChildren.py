import copy
from .generators import Gen, shouldBeKept
from .constants import *
from .ensureGen import addTypeToGenerator
from ..debug import debug, assertType, debugFun, ExceptionInverse
from .leaf import emptyGen

class MultipleChildren(Gen):
    #@debugFun
    def __init__(self, toKeep = None,  **kwargs):
        super().__init__(**kwargs)
        if toKeep is None:
            allFalse = True
            for element in self.getChildren():
                shouldIt = shouldBeKept(element)
                if shouldIt is True:
                    toKeep = True
                    allFalse = False
                    break
                if shouldIt is None:
                    allFalse = None
            if allFalse:
                toKeep = False
        if toKeep is True:
            self.doKeep()
        elif toKeep is False:
            self.dontKeep()
            
 
class ListElement(MultipleChildren):
    #@debugFun
    def __init__(self,
                 elements = None,
                 toKeep = None,
                 **kwargs):
        """ 
        Keyword arguments:
        elements -- list of elements
        """
        self.childEnsured = False
        debug(f"ListElement({elements})",1)
        self.elements = elements
        super().__init__(toKeep = toKeep, **kwargs)
        debug("",-1)
        
    def clone(self, elements):
        truthyElements = []
        for element in elements:
            if element:
                truthyElements.append(element)
        if len(truthyElements)==0:
            return emptyGen
        elif len(truthyElements)==1:
            return truthyElements[0]
        else:
            return ListElement(truthyElements)
        
    def __repr__(self):
        return f"""ListElement({self.elements}, {self.params()})"""

    def __eq__(self,other):
        return isinstance(other,ListElement) and self.elements == other.elements
    
    @debugFun
    def getChildren(self):
        if self.childEnsured == False:
            for i in range(len(self.elements)):
                self.elements[i] = self._ensureGen(self.elements[i])
            self.childEnsured = True
        return self.elements

    @debugFun
    def _applyTag(self, *args, **kwargs):
        for child in self.elements:
            child.applyTag(*args, **kwargs)
            
addTypeToGenerator(list,ListElement)

class Name(Gen):
    """The class which expands differently in function of whether name is asked, hidden, neither."""
    def __init__(self,
                 name = None,
                 asked = None,
                 notAsked = None,
                 cascadeAsked = frozenset(),
                 **kwargs):
        assert assertType(name, str)
        assert assertType(cascadeAsked, frozenset)
        for cascading in cascadeAsked:
            assert assertType(cascading, str)
        self.name = name
        self.cascadeAsked = cascadeAsked
        
        self.asked = asked
        self.notAsked = notAsked
        self.childEnsured = False
        super().__init__(**kwargs)

    def clone(self, elements):
        assert len(elements) ==2
        asked, notAsked = elements
        if not asked and not notAsked:
            return emptyGen
        if asked == self.asked and notAsked == self.notAsked:
            return self
        return Name(name = self.name,
                    asked = asked,
                    notAsked = notAsked,
                    cascadeAsked = self.cascadeAsked)
       
    
    def __repr__(self):
        return f"""Name(name = "{self.name}", asked = {self.asked}, notAsked = {self.notAsked}, {self.params()})"""
    
    def __eq__(self,other):
        return isinstance(other,Name) and self.name == other.name and self.asked == other.asked and self.notAsked == other.notAsked
    
    def getChildren(self):
        if not self.childEnsured:
            self.asked = self._ensureGen(self.asked)
            self.notAsked = self._ensureGen(self.notAsked)
            self.childEnsured = True
        return (self.asked, self.notAsked)

    def _template(self, asked = frozenset(), hide = frozenset()):
        if self.name in hide:
            return None
        if self.name in asked:
            asked = asked | self.cascadeAsked
            child = self.asked
        else:
            child = self.notAsked
        return child.template(asked = asked, hide = hide)
        
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("Name._applyTag should not exists")
    
# class RecursiveFields(MultipleChildren):
#     """

#     descriptions -- prefix, infix, suffix, by level"""
#     def __init__(self,
#                  fields,
#                  descriptions ,
#                  hideSuccessor = False,
#                  
#                  **kwargs):
#         super().__init__( **kwargs)
#         self.fields = fields
#         self.descriptionsOriginal =copy.deepcopy(descriptions)
#         self.descriptions = descriptions
#         self.hideSuccessor = hideSuccessor
#         self.stringToField(self.descriptions, 0)

#     def stringToField(self, elements, level):
#         for i in range(len(elements)):
#             element = elements[i]
#             if isinstance(element,list):
#                 self.stringToField(element, level+1)
#             elif isinstance(element,Field):
#                 pass
#             elif isinstance(element,str):
#                 elements[i] = Field(
#                     element, prefix =
#                     prefix = level[i]["prefix"],
#                     suffix = level[i]["suffix"],
#                     separator = level[i].get(separator, " : "))
        
    
        
        
