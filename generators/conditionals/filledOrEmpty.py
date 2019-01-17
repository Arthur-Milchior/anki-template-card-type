import bs4
from ..generators import thisClassIsClonable
from ...debug import debugFun, debug, debugOnlyThisMethod
from .meta import FieldChild, Dichotomy
from ..generators import addTypeToGenerator
from ..leaf import emptyGen
from ..listGen import ListElement

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

    def _applyTag(self, soup):
        return ([bs4.NavigableString(f"{{{{^{self.field}}}}}")]+
                self.child.applyTag(soup)+
                [bs4.NavigableString(f"{{{{/{self.field}}}}}")])

        
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
        
    def _applyTag(self, soup):
        return ([bs4.NavigableString(f"{{{{#{self.field}}}}}")]+
                self.child.applyTag(soup)+
                [bs4.NavigableString(f"{{{{/{self.field}}}}}")])

def tupleToFilled(tup):
    assert len(tup) == 2
    field, child = tup
    return Filled(field = field,child = child)
addTypeToGenerator(tuple, tupleToFilled)
#It is useful to be able to create Filled from generators. Thus it should be in typeToGenerator. Tuple is a type not yet used, which have sens.
    
# class FilledOrEmpty(ListElement):
#     # def __repr__(self):
#     #     return """FilledOrEmpty({self.field},{self.filledCase},{self.emptyCase})"""
    
#     def __init__(self, field, filledCase = emptyGen, emptyCase = emptyGen,  **kwargs):
#         self.filledCase = filledCase
#         self.emptyCase = emptyCase
#         self.field = field
#         super().__init__([
#             Filled(field = field, child = filledCase),
#             Empty(field = field, child = emptyCase)],  **kwargs)

FilledOrEmpty = Dichotomy(Filled,Empty,"FilledOrEmpty")
