import copy
from .structures import Gen
from .structures.leaf import Literal, Field
from .structures.child import Requirements, AtLeastOne

class MultipleChild(Gen):
    def __init__(self, children, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.children = children
        self.normalizedChildren = None
    def _mustache(self, *args, **kwargs):
        t = ""
        for child in self.children:
            t+= child.mustache(*args, **kwargs)
        return t

    def getNormalizedChilden(self):
        """Memoize the normal form of children. Return it."""
        if self.normalizedChildren is None:
            self.normalizedChildren = [child.normalize() for child in self.children]
        return self.normalizedChildren
    
class ListElement(MultipleChild):
    def __init__(self, elements = None, *args, **kwargs):
        """ 
        Keyword arguments:
        nodes -- list of elements. 
                 A string is interpreted as Literal which can be
        omitted. (If it should be kept, then call this list with
        toKeep = True).
        """
        self.rawElements = elements
        for element in elements:
            if isinstance(element,str):
                element = Literal(element)
            if isinstance(element,Gen):
                self.children.append(element)
            else:
                raise Exception(element, "is neither string nor Gen.")
        super().__init__(self, self.children, *args, **kwargs)

    def _getNormalForm(self):
        return ListElement(self.getNormalizedChilden() , normalized = True)

    def _toKeep(self):
        for element in self.elements:
            if element.toKeep():
                return True
        return False
    
    def _restrictFields(self,fields,empty,hasContent):
        elements = []
        for element in self.elements:
            element = element.restrictFields(fields,empty,hasContent)
            if element.toKeep():
                elements.append(element)
        return ListElement(element, normalized = True)
            
    def _mustache():
        pass

            
# class RecursiveFields(MultipleChild):
#     """

#     descriptions -- prefix, infix, suffix, by level"""
#     def __init__(self,
#                  fields,
#                  descriptions ,
#                  name = "",
#                  hideSuccessor = False,
#                  *args,
#                  **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields = fields
#         self.name = name
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
        
    
        
        
