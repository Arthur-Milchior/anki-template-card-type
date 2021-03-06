from ...debug import debug, debugFun
from ..generators import thisClassIsClonable
from ..listGen import ListElement
from .meta import Dichotomy, FieldChild


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

    def _assumeFieldFilled(self, fields, setMandatoryState):
        if self.field in fields:
            return emptyGen
        else:
            return self.assumeFieldFilled(fields, setMandatoryState)

    def _getWithoutRedundance(self):
        child = self.getChild().getWithoutRedundance()
        child = child.assumeFieldAbsent(self.field)
        return self.cloneSingle(child)

    @debugFun
    def _restrictToModel(self, fields):
        if self.field in fields:
            return None
        else:
            return self.getChild().restrictToModel(fields)

    def _createHtml(self, soup):
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
    def _restrictToModel(self, fields):
        if self.field in fields:
            return self.getChild().restrictToModel(fields)
        else:
            return None

    def _createHtml(self, soup):
        assert False
# class PresentOrAbsent(ListElement):
#     def __init__(self, field, presentCase = None, absentCase = None,  **kwargs):
#         self.presentCase = presentCase
#         self.absentCase = absentCase
#         self.field = field
#         super().__init__([
#             Present(field = field, child = presentCase),
#             Absent(field = field, child = absentCase),],  **kwargs)


PresentOrAbsent = Dichotomy(Present, Absent, "PresentOrAbsent")
