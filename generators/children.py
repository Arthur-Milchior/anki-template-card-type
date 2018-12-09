import copy
from .generators import Gen, addTypeToGenerator, ensureGen
from .leaf import Literal, Field, Empty, emptyGen
from ..debug import debug, assertType

class MultipleChild(Gen):
    pass
        
class ListElement(MultipleChild):
    def __init__(self,
                 elements = None,
                 isNormal = False,
                  **kwargs):

        """ 
        Keyword arguments:
        nodes -- list of elements. 
                 A string is interpreted as Literal which can be
        omitted. (If it should be kept, then call this list with
        toKeep = True).
        """
        self.rawElements = elements
        self.children = []
        unisNormalChild = False
        for element in elements:
            if not(element):#don't add empty elements.
                continue
            element = ensureGen(element)
            if isinstance(element,Gen):
                self.children.append(element)
                if not element.getIsNormal():
                    unisNormalChild = True
            else:
                raise Exception(element, "is neither string nor Gen.")
        super().__init__(isNormal = isNormal or (not unisNormalChild),
                         
                         **kwargs)
    
    def __repr__(self):
        return f"""ListElement(elements = {repr(self.children)}, {self.params()})"""

    def __eq__(self,other):
        return isinstance(other,ListElement) and self.children == other.children
    
    def getChildren(self):
        #debug(f"{self}.getChildren() = {self.children}")
        return self.children
    
    def _applyRecursively(self,fun,  **kwargs):
        """self, with fun applied to each element. 

        isNormal and versionWithoutRedundancy are passed to class constructor."""
        #debug(f"{self}._applyRecursively({fun.__name__})",1)
        elements = []
        change = False
        for element in self.children:
            #debug(f"""applying {fun.__name__} to {element}""")
            element_ = fun(element)
            #debug(f"""returning {element_}""")
            if element_ != element:
                #debug(f"""changed""")
                change = True
            else:
                #debug(f"""not changed""")
                pass
            if element_:
                #debug("Appending it to elements")
                elements.append(element_)
            else:
                #debug(f"""not appending it""")
                pass
        if not elements:
            ret = emptyGen
        elif len(elements) == 1:
            ret = elements[0]
        elif change:
            ret = ListElement(elements = elements,  **kwargs)
        else:
            ret = self
        #debug(f"self._applyRecursively() returns {ret}",-1)
        return ret

    def _template(self, *args, **kwargs):
        t = ""
        for child in self.children:
            t+= child.template(*args, **kwargs)
        return t
    
addTypeToGenerator(list,ListElement)
class Branch(Gen):
    """The class which expands differently in function of the question/hidden value.

    name -- the name of this question.
    children[isQuestion][isAsked] -- the field to show on the side question/answer of card (depending on isQuestion). Depending on whether this value is asked or not."""
    def __init__(self,
                 name = None,
                 default = None,
                 question = None,
                 answerAsked = None,
                 answerNotAsked = None,
                 answer = None,
                 asked = None,
                 notAsked = None,
                 questionAsked = None,
                 questionNotAsked = None,
                 children = dict(),
                 toClone = None,
                 isNormal = False,
                 **kwargs):
        """
        The value of self.children[isQuestion,isAsked] is:
        {isQuestion}{IsAsked} if it exists.
        {isAsked} if it exists
        {isQuestion} if it exists
        children[isQuestion,isAsked]
        {default} if it exists
        empty otherwise.

        """
        if name is not None:
            self.name = name
        elif toClone is not None and  isinstance(toClone,Branch):
            self.name = toClone.name
        else:
            assert False
        self.children = dict()
        tmp = dict()
        tmp[True,True]= [questionAsked, asked, question, children.get((True,True)), default, emptyGen]
        tmp[True,False] = [questionNotAsked, notAsked, question, children.get((True,False)), default, emptyGen]
        tmp[False,True]= [answerAsked, asked, answer, children.get((False,True)), default, emptyGen]
        tmp[False,False] = [answerNotAsked, notAsked, answer, children.get((False,False)), default, emptyGen]
        notNormalChild = False
        for isQuestionAsked in tmp:
            for value in tmp[isQuestionAsked]:
                if value is not None:
                    child = ensureGen(value)
                    self.children[isQuestionAsked] = child
                    if not child.getIsNormal():
                        notNormalChild = True
                    break
        super().__init__( toClone = toClone, isNormal = isNormal or not notNormalChild,  **kwargs)

    def __repr__(self):
        return f"""Branch(name = {self.name}, children = {repr(self.children)}, {self.params()})"""
    
    def __eq__(self,other):
        return isinstance(other,Branch) and self.name == other.name and self.children == other.children
    
    def getChildren(self):
        return self.children.values()
    
    def _applyRecursively(self,fun, **kwargs):
        children = dict()
        change = False
        shouldKeep = False
        for isQuestionAsked in self.children:
            tmp = fun(self.children[isQuestionAsked])
            assert assertType(tmp,Gen)
            if tmp != self.children[isQuestionAsked]:
                change = True
            if tmp.getToKeep():
                shouldKeep = True
            children[isQuestionAsked] = tmp
        if not shouldKeep:
            return emptyGen
        if not change:
            return self
        return Branch(children = children, **kwargs)
    
    def _assumeFieldInSet(self, field, setName):
        if setName == "Remove" and field == self.name:
            return emptyGen
        return super()._assumeFieldInSet(field,setName)

    def _template(self, tag, soup, isQuestion, asked, hide, **kwargs):
        if hide and self.name in hide:
            return ""
        if asked is None:
            debug("asked is None, this isAsked is False")
            isAsked = False
        else:
            debug(f"asked is {asked}")
            if self.name in asked:
                debug(f"name {self.name} belongs to asked")
                isAsked = True
            else:
                debug(f"name {self.name} does not belong to asked")
                isAsked = False
            debug(f"isQuestion:{isQuestion}, isAsked: {isAsked}")
        ret = self.children[isQuestion,isAsked].template(tag,soup, isQuestion, asked, hide, **kwargs)
        #return ret
        
    
# class RecursiveFields(MultipleChild):
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
        
    
        
        
