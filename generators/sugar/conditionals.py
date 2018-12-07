from ..child import SingleChild
from ..leaf import emptyGen
from ..children import MultipleChild, ListElement

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
                                     isEmpty = actual).getNormalForm()
        return actual

class FilledOrEmpty(MultipleChild):
    def __init__(self,field,filledCase = emptyGen, emptyCase = emptyGen, *args, **kwargs):
        self.filledCase = filledCase
        self.emptyCase = emptyCase
        self.field = field
        super().__init__([
            Requirements(
                self.filledCase.getNormalForm(),
                requireFilledCase = {self.field}
            ),
            Requirements(
                self.emptyCase.getNormalForm(),
                requireEmpty = {self.field}
            )], *args, **kwargs)
class Filled(FilledOrEmpty):
    def __init__(self, field, child, *args, **kwargs):
        super().__init__(field, filledCase = child, *args, **kwargs)
class Empty(FilledOrEmpty):
    def __init__(self, field, child, *args, **kwargs):
        super().__init__(field, emptyCase = child, *args, **kwargs)
    
class QuestionOrAnswer(MultipleChild):
    def __init__(self, questionCase = emptyGen, answerCase = emptyGen, *args, **kwargs):
        self.questionCase = questionCase
        self.answerCase = answerCase
        super().__init__([
            Requirements(
                self.questionCase.getNormalForm(),
                requireQuestion = True
            ),
            Requirements(
                self.answerCase.getNormalForm(),
                requireQuestion = False
            )], *args, **kwargs)
class Question(QuestionOrAnswer):
    def __init__(self, child, *args, **kwargs):
        super().__init__(questionCase = child, *args, **kwargs)
class Answer(QuestionOrAnswer):
    def __init__(self, child, *args, **kwargs):
        super().__init__(answerCase = child, *args, **kwargs)
        
    
        
class PresentOrAbsent(MultipleChild):
    def __init__(self, field, presentCase = emptyGen, absentCase = emptyGen, *args, **kwargs):
        self.presentCase = presentCase
        self.absentCase = absentCase
        self.field = field
        elements = super().__init__(
            [
                Requirements(
                    self.presentCase.getNormalForm(),
                    inModel = {self.field}
                ),
                Requirements(
                    self.absentCase.getNormalForm(),
                    absentOfModel = {self.field}
                )]
            ,*args, **kwargs)
    
class Present(PresentOrAbsent):
    def __init__(self, field, child, *args, **kwargs):
        super().__init__(field, presentCase = child, *args, **kwargs)
class Absent(PresentOrAbsent):
    def __init__(self, field, child, *args, **kwargs):
        super().__init__(field, absentCase = child, *args, **kwargs)
