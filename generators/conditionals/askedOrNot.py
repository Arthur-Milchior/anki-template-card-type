from .meta import FieldChild
from ..generators import thisClassIsClonable
from ...debug import debugFun, debug
from ..list import ListElement

@thisClassIsClonable
class Asked(FieldChild):
    """The class which expands only if its field is asked."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().getWithoutRedundance().assumeAsked(self.field))

    def _assumeAsked(self, field):
        if self.field == field:
            child = self.getChild().assumeAsked(field)
            return child
        else:
            return self.cloneSingle(self.getChild().assumeAsked(field))
    def _assumeNotAsked(self, field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().assumeAsked(field))

    def _noMoreAsk(self):
        return None
        
    def _removeName(self, field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().removeName(field))
        
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("Asked._applyTag should not exists")

    
@thisClassIsClonable
class NotAsked(FieldChild):
    """The class which expands only if its field is not asked."""
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().getWithoutRedundance().assumeNotAsked(self.field))
    
    def _assumeNotAsked(self, field):
        if self.field == field:
            return self.getChild().assumeAsked(field)
        else:
            return self.cloneSingle(self.getChild().assumeAsked(field))

    @debugFun
    def _removeName(self, field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().removeName(field))

    def _noMoreAsk(self):
        return self.getChild().noMoreAsk()
                
    def _assumeAsked(self, field):
        if self.field == field:
            return None
        else:
            return self.getChild().assumeAsked(field)
        
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("NotAsked._applyTag should not exists")

@thisClassIsClonable
class Cascade(FieldChild):
    def __init__(self, *args, cascade = frozenset(), **kwargs):
        super().__init__(*args, **kwargs)
        self.cascade = cascade

    def _getNormalForm(self):
        if not self.cascade:
            return self.child.getNormalForm()
        else:
            return super()._getNormalForm()
        
    def _removeName(self, field):
        if self.field == field:
            return None
        else:
            return self.cloneSingle(self.getChild().removeName(field))

    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("NotAsked._applyTag should not exists")

    def _assumeAsked(self,field):
        if self.field == field:
            child = self.getChild().assumeAsked(field)
            for cascaded in self.cascade:
                child = child.assumeAsked(cascaded)
            return child
        return self

    def _assumeNotAsked(self,field):
        if self.field == field:
            return None
        else:
            return self

    def _noMoreAsk(self):
        return self.getChild()

        
    
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
        askedGen = Cascade(field = field, child = asked, cascade = cascade)
        askedGen = Asked(field = field, child = askedGen)
        notAskedGen = NotAsked(field = field,child = notAsked)
        super().__init__([askedGen, notAskedGen ], **kwargs)
