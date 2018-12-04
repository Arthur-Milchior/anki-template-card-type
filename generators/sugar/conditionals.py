from ..child import SingleChild
from ..leaf import emptyGen
from ..children import MultipleChild

class AtLeastOne(SingleChild):
    """Show the child if there is at least one condition.

    The child is repeated as many time in the card's template as they
    are fields. So use this only for small text, such as
    <table>

    """
    def __init__(self,child, fields):
        super().__init__(child)
        self.fields = fields

    def _getNormalForm(self):
        actual = emptyGen
        child = self.child.getNormalForm()
        for condition in self.fields:
            actual = FilledOrEmpty(condition, filled = child,
                                     empty = actual).getNormalForm()
        return actual
    
class FilledOrEmpty(MultipleChild):
    def __init__(self,field,filledCase = emptyGen, emptyCase = emptyGen, *args, **kwargs):
        self.filledCase = filledCase
        self.emptyCase = emptyCase
        self.field = field
        super().__init__( *args, **kwargs)

    def getChildren(self):
        return frozenset({self.filledCase, self.emptyCase})
        
    def _getNormalForm(self):
        super().normalize()
        return ListElement([
            Requirements(
                self.filledCase.getNormalForm(),
                requireFilledCase = {self.field}
                ),
            Requirements(
                self.emptyCase.getNormalForm(),
                requireEmpty = {self.field}
            )]).getNormalForm()
    
class QuestionOrAnswer(MultipleChild):
    def __init__(self,questionCase = answerGen, answerCase = answerGen, *args, **kwargs):
        self.questionCase = questionCase
        self.answerCase = answerCase
        super().__init__( *args, **kwargs)

    def getChildren(self):
        return frozenset({self.questionCase, self.answerCase})
        
    def _getNormalForm(self):
        super().normalize()
        return ListElement([
            Requirements(
                self.questionCase.getNormalForm(),
                requireQuestion = True
                ),
            Requirements(
                self.answerCase.getNormalForm(),
                requireQuestion = False
            )]).getNormalForm()
    
class PresentOrAbsent(MultipleChild):
    def __init__(self,field,presentCase = emptyGen,absentCase = emptyGen, *args, **kwargs):
        self.presentCase = presentCase
        self.absentCase = absentCase
        self.field = field
        super().__init__(*args, **kwargs)

    def getChildren(self):
        return frozenset({self.presentCase, self.absentCase})
        
    def _getNormalForm(self):
        super().normalize()
        return ListElement([
            Requirements(
                self.presentCase.getNormalForm(),
                inModel = {self.field}
                ),
            Requirements(
                self.absentCase.getNormalForm(),
                absentOfModel = {self.field}
            )]).getNormalForm()
