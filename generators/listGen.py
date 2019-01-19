import copy
from .generators import Gen, shouldBeKept, genRepr, thisClassIsClonable, MultipleChildren
from .constants import *
from .ensureGen import addTypeToGenerator
from ..debug import debug, assertType, debugFun, ExceptionInverse, debugInit, debugOnlyThisMethod

 
@thisClassIsClonable
class ListElement(MultipleChildren):
    @debugInit
    def __init__(self,
                 elements = None,
                 **kwargs):
        """ 
        Keyword arguments:
        elements -- list of elements
        """
        # self.childEnsured = False
        assert assertType(elements,list)
        self.elements = elements
        super().__init__(**kwargs)
        self.changeElements()

        
    def changeElements(self):
        truthyElements = []
        # someToKeep = False
        for element in self.elements:
            if element:
                element = self._ensureGen(element)
                truthyElements.append(element)
                # if element.getToKeep() is not False:
                #     someToKeep = True
        if len(truthyElements)==0:# or not someToKeep:
            self.elements = []
            self.setState(EMPTY)
        else:
            self.elements= truthyElements

    def clone(self, elements):
        l= ListElement(elements)
        if not l.elements:
            return None
        elif len(l.elements) is 1:
            child = l.elements[0]
            return child
        else:
            return l
        
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

    def _innerEq(self,other):
        return self.elements == other.elements
    def _outerEq(self,other):
        return isinstance(other,ListElement) and len(self.elements) == len(other.elements) and super()._outerEq(other)
    def _firstDifference(self,other):
        for i in range(len(self.elements)):
            ret = self.elements[i].firstDifference(other.elements[i])
            if ret is not None:
                return ret
        return None
    
    @debugFun
    def _getChildren(self):
        # if self.childEnsured == False:
        #     for i in range(len(self.elements)):
        #         self.elements[i] = self._ensureGen(self.elements[i])
        #     self.childEnsured = True
        return self.elements

    @debugFun
    def _createHtml(self, *args, **kwargs):
        l = []
        for child in self.elements:
            l+= child.createHtml(*args, **kwargs)
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
        
    
        
        
