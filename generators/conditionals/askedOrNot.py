from .meta import FieldChild
from ..generators import thisClassIsClonable, Gen, genRepr
from ...debug import debugFun, debug, debugOnlyThisMethod, debugInit,debugOnlyThisInit
from ..list import ListElement
from ...utils import standardContainer

@thisClassIsClonable
class Asked(FieldChild):
    """The class which expands only if its field is asked."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().getWithoutRedundance().assumeAsked(self.field))

    def _assumeAsked(self, field, modelName):
        if self.field == field:
            child = self.getChild().assumeAsked(field, modelName)
            return child
        else:
            return self.cloneSingle(self.getChild().assumeAsked(field,modelName))
    def _assumeNotAsked(self, field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().assumeNotAsked(field))

    def _noMoreAsk(self):
        return None
        
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("Asked._applyTag should not exists")

    
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

    def _assumeAsked(self, field,modelName):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().assumeAsked(field,modelName))
        
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("NotAsked._applyTag should not exists")

@thisClassIsClonable
class Cascade(FieldChild):
    @debugInit
    #@debugOnlyThisInit
    def __init__(self, field, child, cascade, **kwargs):
        self.cascade = cascade
        assert isinstance(field,str)
        assert standardContainer(cascade)
        assert cascade
        super().__init__(field, child, **kwargs)
        
    def _repr(self):
        space  = "  "*Gen.indentation
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
            field = self.field,
            child = child,
            cascade = self.cascade)
        
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("NotAsked._applyTag should not exists")

    def _assumeAsked(self,field,modelName):
        if self.field == field:
            child = self.getChild().assumeAsked(field,modelName)
            for cascaded in self.cascade:
                child = child.assumeAsked(cascaded,modelName)
            return child
        else:
            return self.cloneSingle(self.getChild().assumeAsked(field,modelName))

    def _assumeNotAsked(self,field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().assumeNotAsked(field))

    def _noMoreAsk(self):
        return self.getChild().noMoreAsk()

        
    
class AskedOrNot(ListElement):
    """The class which expands differently in function of whether a name is asked or not."""
    def __init__(self,
                 field,
                 asked = None,
                 notAsked = None,
                 cascade = frozenset(),
                 **kwargs):
        self.asked = asked
        self.notAsked = notAsked
        askedGen = Cascade(field = field, child = asked, cascade = cascade) if cascade else asked
        askedGen = Asked(field = field, child = askedGen)
        notAskedGen = NotAsked(field = field,child = notAsked)
        super().__init__([askedGen, notAskedGen ], **kwargs)
