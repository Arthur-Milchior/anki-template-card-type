from .structures.child import SingleChild

class AtLeastOne(SingleChild):
    """Show the child if there is at least one condition.

    The child is repeated as many time in the card's template as they
    are conditions. So use this only for small text, such as
    <table>

    """
    def __init__(self,child, conditions):
        super().__init__(child)
        self.conditions = conditions

    def _getNormalForm(self):
        actual = emptyGen
        child = self.child.getNormalForm()
        for condition in self.conditions:
            actual = FilledOrEmpty(condition, filled = child,
                                     empty = actual).getNormalForm()
        return actual
    
class FilledOrEmpty(MultipleChild):
    def __init__(self,field,filled = emptyGen,empty = emptyGen, *args, **kwargs):
        self.filled = filled
        self.empty = empty
        self.field = field
        super().__init__( *args, **kwargs)

    def getChildren(self):
        return frozenset({self.filled, self.empty})
    def getFilled(self):
        return self.filled
    def getEmpty(self):
        return self.empty
        
    def _getNormalForm(self):
        super().normalize()
        return ListElement([
            Requirements(
                self.getFilled().getNormalForm(),
                requireFilled = {self.field}
                ),
            Requirements(
                self.getEmpty().getNormalForm(),
                requireEmpty = {self.field}
            )]).getNormalForm()
    
class PresentOrAbsent(MultipleChild):
    def __init__(self,field,present = emptyGen,absent = emptyGen, *args, **kwargs):
        self.present = present
        self.absent = absent
        self.field = field
        super().__init__(*args, **kwargs)

    def getChildren(self):
        return frozenset({self.present, self.absent})
    def getPresent(self):
        return self.present
    def getAbsent(self):
        return self.absent
        
    def _getNormalForm(self):
        super().normalize()
        return ListElement([
            Requirements(
                self.getPresent().getNormalForm(),
                inModel = {self.field}
                ),
            Requirements(
                self.getAbsent().getNormalForm(),
                absentOfModel = {self.field}
            )]).getNormalForm()
