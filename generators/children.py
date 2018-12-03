import copy
from .generator import Gen, addTypeToGenerator, ensureGen
from .leaf import Literal, Field, Empty, emptyGen

class MultipleChild(Gen):
    pass
        
class ListElement(MultipleChild):
    def __init__(self,
                 elements = None,
                 normalized = False,
                 *args, **kwargs):

        """ 
        Keyword arguments:
        nodes -- list of elements. 
                 A string is interpreted as Literal which can be
        omitted. (If it should be kept, then call this list with
        toKeep = True).
        """
        self.rawElements = elements
        unnormalizedChild = False
        for element in elements:
            if not(element):#don't add empty elements.
                continue
            element = ensureGen(element)
            if isinstance(element,Gen):
                self.children.append(element)
                if not element.isNormal():
                    unnormalizedChild = True
            else:
                raise Exception(element, "is neither string nor Gen.")
        super().__init__(self,
                         self.children,
                         normalized = normalized or (not unnormalizedChild),
                         *args,
                         **kwargs)

    def getChildren(self):
        return self.children
    
    def _applyRecursively(self,fun, *args, **kwargs):
        """self, with fun applied to each element. 

        normalized and unRedundanted are passed to class constructor."""
        elements = []
        change = False
        for element in self.elements:
            element_ = fun(element)
            if element != element:
                change = True
            if element:
                elements.append(element)
        if not elements:
            return emptyGen
        if len(elements) == 1:
            return elements[0]
        if change:
            return ListElement(elements = elements, *args, **kwargs)
        else:
            return self

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
                 children = None,
                 toClone = None,
                 normalized = False,
                 *args,
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
        elif toClone is not None:
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
                    if not child.isNormal():
                        notNormalChild = True
                    break
        super().__init__( toClone = toClone, normalized = normalized or not notNormalChild, *args, **kwargs)

    def getChildren(self):
        return self.children.values()
    
    def _applyRecursively(fun, **kwargs):
        children = dict()
        change = False
        shouldKeep = False
        for isQuestionAsked in self.children:
            tmp = fun(self.children[isQuestionAsked])
            if tmp != self.children[isQuestionAsked]:
                change = True
            if tmp.toKeep():
                shouldKeep = True
            children[isQuestionAsked] = tmp
        if not shouldKeep:
            return emptyGen
        if not change:
            return self
        return Branch(children = children, **kwargs)
    
    def _assumeFieldInSet(self, field, set):
        if set == "Remove" and field == self.name:
            return emptyGen
        return super()._assumeFieldInSet(field,set)

    def _template(self, asked = None, hide = None, isQuestion = False):
        if hide and self.name in hide:
            return ""
        isAsked = asked and self.name in asked
        return self.children[question,isAsked].template(asked = asked, hide = hide, isQuestion=isQuestion)
        
    
# class RecursiveFields(MultipleChild):
#     """

#     descriptions -- prefix, infix, suffix, by level"""
#     def __init__(self,
#                  fields,
#                  descriptions ,
#                  hideSuccessor = False,
#                  *args,
#                  **kwargs):
#         super().__init__(*args, **kwargs)
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
        
    
        
        
