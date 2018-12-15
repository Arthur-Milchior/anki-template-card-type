import copy
from .generators import Gen, shouldBeKept
from .constants import *
from .ensureGen import addTypeToGenerator
from .leaf import Literal, Field, Empty, emptyGen
from ..debug import debug, assertType, debugFun

class MultipleChildren(Gen):
    @debugFun
    def __init__(self, toKeep = None, **kwargs):
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
        super().__init__(toKeep = toKeep, **kwargs)

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
        debug(f"ListElement({elements})",1)
        self.elements = elements
        super().__init__(toKeep = toKeep, **kwargs)
        debug("",-1)
 
    def __repr__(self):
        return f"""ListElement(elements = {self.elements}, {self.params()})"""

    def __eq__(self,other):
        return isinstance(other,ListElement) and self.elements == other.elements
    
    @debugFun
    def getChildren(self):
        #debug(f"{self}.getChildren() = {self.children}")
        return self.elements
    
    @debugFun
    def _applyRecursively(self, fun, **kwargs):
        """self, with fun applied to each element. 

        isNormal and versionWithoutRedundancy are passed to class constructor."""
        debug(f"{self}._applyRecursively({fun.__name__})",1)
        elements = []
        change = False
        for i in range(len(self.elements)):
            debug(f"Considering position {i}, containing {self.elements[i]}")
            self.elements[i] = self._ensureGen(self.elements[i])
            debug(f"""Once in gen, it becomes "{self.elements[i]}".""")
            debug(f"""applying {fun.__name__} to "{self.elements[i]}".""")
            element_ = fun(self.elements[i])
            debug(f"""element_ now is {element_}""")
            if element_ != self.elements[i]:
                debug(f"""changed""")
                change = True
            else:
                debug(f"""not changed""")
                pass
            if element_:
                debug(f"Appending {element_} to elements")
                elements.append(element_)
            else:
                debug(f"""not appending it""")
                pass
        debug(f"""End of loop. Elements are "{elements}".""")
        if not elements:
            ret = emptyGen
        elif len(elements) == 1:
            ret = elements[0]
        elif change:
            ret = ListElement(elements = elements,  **kwargs)
        else:
            ret = self
        debug(f"self._applyRecursively() returns {ret}",-1)
        return ret

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
                 toClone = None,
                 cascadeAsked = frozenset(),
                 **kwargs):
        if name is not None:
            self.name = name
        elif toClone is not None and  isinstance(toClone,Branch):
            self.name = toClone.name
        else:
            assert False
        self.cascadeAsked = cascadeAsked
        self.asked = asked
        self.notAsked = notAsked
        super().__init__(**kwargs)
    
    def __repr__(self):
        return f"""Name(name = {self.name}, asked = {self.asked}, notAsked = {self.notAsked}, {self.params()})"""
    
    def __eq__(self,other):
        return isinstance(other,Branch) and self.name == other.name and self.asked == other.asked and self.notAsked == other.notAsked
    
    def getChildren(self):
        return frozenset({self.asked, self.notAsked})
    
    def _applyRecursively(self, fun, **kwargs):
        self.asked = ensureGen(self.asked)
        self.notAsked = ensureGen(self.notAsked)
        asked_ = fun(self.asked)
        notAsked_ = fun(self.notAsked)
        if asked_ == self.asked_ and notAsked_ == self.notAsked_:
            return self
        return Name(asked_, notAsked_, **kwargs)

    def _template(self, tag, soup, isQuestion = None, asked = frozenset(), hide = frozenset()):
        assert assertType(isQuestion, bool)
        if self.name in hide:
            return None
        if self.name in asked:
            asked = asked | self.cascadeAsked
            child = self.asked
        else:
            child = self.notAsked
        return child.template(tag, soup, isQuestion = isQuestion, asked = asked, hide = hide)
        
    def _applyTag(self, *args, **kwargs):
        raise Exception("Name._applyTag should not exists")
        
class QuestionOrAnswer(Gen):
    """The class which expands differently in function of the question/answer side."""
    def __init__(self,
                 question = None,
                 answer = None,
                 **kwargs):
        self.question = question
        self.answer = answer
        super().__init__(**kwargs)
        

    def _assumeQuestion(self, isQuestion):
        return self.question if isQuestion else self.answer
    
    def __repr__(self):
        return f"""QuestionOrAnswer("{self.question}", "{self.answer}", {self.params()})"""
    
    def __eq__(self,other):
        return isinstance(other,QuestionAsked) and self.answer == other.answer and self.question == other.question
    
    def getChildren(self):
        return frozenset({self.answer, self.question})
    
    def _applyRecursively(self, fun, **kwargs):
        self.question = ensureGen(question)
        self.answer = ensureGen(answer)
        question_ = fun(self.question)
        answer_ = fun(self.answer)
        if question_ == self.question_ and answer_ == self.answer_:
            return self
        return QuestionOrAnswer(question_, answer_, **kwargs)

    def _applyTag(self, *args, isQuestion = None, **kwargs):
        return self._assumeQuestion(isQuestion).applyTag(*args, isQuestion = None, **kwargs)
    
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
        
    
        
        
