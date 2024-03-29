from ...debug import (assertType, debug, debugFun, debugInit,
                      debugOnlyThisInit, debugOnlyThisMethod)
from ...utils import standardContainer
from ..generators import Gen, genRepr, thisClassIsClonable
from ..listGen import ListElement
from .meta import Dichotomy, FieldChild


@thisClassIsClonable
class Asked(FieldChild):
    """The class which expands only if its field is asked."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().getWithoutRedundance().assumeAsked(self.field))

    def _assumeAsked(self, fields, modelName, changeState):
        if self.field in fields:
            child = self.getChild().assumeAsked(fields, modelName, changeState)
            return child
        else:
            return self.cloneSingle(self.getChild().assumeAsked(fields, modelName, changeState))

    def _assumeNotAsked(self, field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().assumeNotAsked(field))

    def _noMoreAsk(self):
        return None

    def _createHtml(self, *args, **kwargs):
        raise ExceptionInverse("Asked._createHtml should not exists")


@thisClassIsClonable
class NotAsked(FieldChild):
    """The class which expands only if its field is not asked."""

    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().getWithoutRedundance().assumeNotAsked(self.field))

    def _assumeNotAsked(self, field):
        if self.field == field:
            return self.getChild().assumeNotAsked(field)
        else:
            return self.cloneSingle(self.getChild().assumeNotAsked(field))

    def _noMoreAsk(self):
        return self.getChild().noMoreAsk()

    def _assumeAsked(self, fields, modelName, changeState):
        if self.field in fields:
            return None
        else:
            return self.cloneSingle(self.getChild().assumeAsked(fields, modelName, changeState))

    def _createHtml(self, *args, **kwargs):
        raise ExceptionInverse("NotAsked._createHtml should not exists")


@thisClassIsClonable
class Cascade(FieldChild):
    """Is field is asked, assume that all elements of cascade are asked in child"""
    @debugInit
    # @debugOnlyThisInit
    def __init__(self, field, child, cascade, **kwargs):
        assert assertType(cascade, set)
        self.cascade = cascade
        assert isinstance(field, str)
        assert standardContainer(cascade)
        assert cascade
        super().__init__(field, child, **kwargs)

    def _repr(self):
        space = "  "*Gen.indentation
        return f"""{self.__class__.__name__}(
{genRepr(self.field, label = "field")},
{genRepr(self.cascade, label = "cascade")},
{genRepr(self.child, label = "child")},{self.params()})"""

    @debugFun
    def _getNormalForm(self):
        if not self.cascade:
            return self.child.getNormalForm()
        else:
            return super()._getNormalForm()

    def _cloneSingle(self, child):
        return self.classToClone(
            field=self.field,
            child=child,
            cascade=self.cascade)

    def _createHtml(self, *args, **kwargs):
        raise ExceptionInverse("NotAsked._createHtml should not exists")

    def _assumeAsked(self, fields, modelName, changeState):
        if self.field in fields:
            return self.getChild().assumeAsked(fields | self.cascade, modelName, changeState)
        else:
            return self.cloneSingle(self.getChild().assumeAsked(fields, modelName, changeState))

    def _assumeNotAsked(self, field):
        if self.field == field:
            return self.getChild().assumeNotAsked(field)
        else:
            return self.cloneSingle(self.getChild().assumeNotAsked(field))

    def _noMoreAsk(self):
        return self.getChild().noMoreAsk()


# class AskedOrNot(ListElement):
#     """The class which expands differently in function of whether a name is asked or not."""
#     def __init__(self,
#                  field,
#                  asked = None,
#                  notAsked = None,
#                  cascade = frozenset(),
#                  **kwargs):
#         self.asked = asked
#         self.notAsked = notAsked
#         askedGen = Cascade(field = field, child = asked, cascade = cascade) if cascade else asked
#         askedGen = Asked(field = field, child = askedGen)
#         notAskedGen = NotAsked(field = field,child = notAsked)
#         super().__init__([askedGen, notAskedGen ], **kwargs)
AskedOrNot = Dichotomy(Asked, NotAsked, "AskedOrNot")
