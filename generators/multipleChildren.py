import copy
from .generators import Gen, shouldBeKept, genRepr, thisClassIsClonable
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
            
 
@thisClassIsClonable
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
        debug("ListElement({elements})",1)
        self.elements = [element for element in elements if element]
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
        
    def _repr(self):
        space  = "  "*Gen.indentation
        t = f"""ListElement(["""
        first = True
        for element in self.elements:
            if first:
                first = False
            else:
                t+=","
            t+="\n"
            t+=genRepr(element)
        t+=f"""],{self.params()})"""
        return t

    def __eq__(self,other):
        return isinstance(other,ListElement) and self.elements == other.elements
    
    @debugFun
    def _getChildren(self):
        if self.childEnsured == False:
            for i in range(len(self.elements)):
                self.elements[i] = self._ensureGen(self.elements[i])
            self.childEnsured = True
        return self.elements

    @debugFun
    def _applyTag(self, *args, **kwargs):
        l = []
        for child in self.elements:
            l+= child.applyTag(*args, **kwargs)
        return l
            
addTypeToGenerator(list,ListElement)

    
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
        
    
        
        
