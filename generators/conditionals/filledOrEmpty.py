import bs4

from ...debug import assertType, debug, debugFun, debugOnlyThisMethod
from ..constants import MANDATORY
from ..generators import addTypeToGenerator, thisClassIsClonable
from ..leaf import emptyGen
from ..listGen import ListElement
from .meta import Dichotomy, FieldChild


@thisClassIsClonable
class Empty(FieldChild):
    """The class which expands differently in function of the question/answer side."""
    def _assumeFieldFilled(self, fields, setMandatoryState):
        if self.field in fields:
            return emptyGen
        else:
            return self.cloneSingle(self.getChild().assumeFieldFilled(fields, setMandatoryState))

    def _assumeFieldEmpty(self, fields, setForbiddenState):
        if self.field in fields:
            return self.getChild().assumeFieldEmpty(fields, setForbiddenState)
        else:
            return self.cloneSingle(self.getChild().assumeFieldEmpty(fields, setForbiddenState))

    def _assumeFieldAbsent(self, field):
        if self.field == field:
            return self.getChild().assumeFieldAbsent(field)
        else:
            return self.cloneSingle(self.getChild().assumeFieldAbsent(field))

    def _restrictToModel(self, fields):
        if self.field in fields:
            return self.cloneSingle(self.getChild().restrictToModel(fields))
        else:
            return self.getChild().restrictToModel(fields)

    def _getWithoutRedundance(self):
        child = self.getChild().getWithoutRedundance()
        child =child.assumeFieldEmpty(self.field, False)
        return self.cloneSingle(child)

    def _createHtml(self, soup):
        childHtml = self.getChild().createHtml(soup)
        assert assertType(childHtml,list)
        return ([bs4.NavigableString(f"{{{{^{self.field}}}}}")]+
                childHtml+
                [bs4.NavigableString(f"{{{{/{self.field}}}}}")])


@thisClassIsClonable
class Filled(FieldChild):
    """The class which expands differently in function of the question/answer side."""
    def _assumeFieldFilled(self, fields, setMandatoryState):
      if self.field in fields:
          return self.getChild().assumeFieldFilled(fields, setMandatoryState)
      else:
          return self.cloneSingle(self.getChild().assumeFieldFilled(fields, setMandatoryState))

    def _assumeFieldEmpty(self, fields, setForbiddenState):
        if self.field in fields:
            return emptyGen
        else:
            return self.cloneSingle(self.getChild().assumeFieldEmpty(fields, setForbiddenState))

    def _assumeFieldAbsent(self, field):
        if self.field == field:
            return self.empty
        else:
            return self.cloneSingle(self.getChild().assumeFieldAbsent(field))

    def _getWithoutRedundance(self):
        child = self.getChild().getWithoutRedundance()
        child = child.assumeFieldFilled(self.field, setMandatoryState = False)
        return self.cloneSingle(child)

    @debugFun
    def _restrictToModel(self,fields):
        if self.field not in fields:
            #debug("self.field({self.field}) not in fields({fields})")
            return emptyGen
        else:
            return self.cloneSingle(self.getChild().restrictToModel(fields))

    def _createHtml(self, soup):
        child = self.getChild().createHtml(soup)
        assert assertType(child,list)
        return ([bs4.NavigableString(f"{{{{#{self.field}}}}}")]+
                child+
                [bs4.NavigableString(f"{{{{/{self.field}}}}}")])

def tupleToFilled(tup):
    if len(tup) == 2:
        field, child = tup
        return Filled(field = field,child = child)
    elif len(tup) == 3:
        field, filled, empty = tup
        if filled is None:
            return Empty(field, empty)
        else:
            return FilledOrEmpty(field, filled, empty)
    else:
        raise Exception(f"Tuple of size {len(tup)}")
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
