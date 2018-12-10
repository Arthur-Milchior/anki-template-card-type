from ..child import SingleChild
from ..leaf import emptyGen
from ..children import MultipleChild, ListElement

class FilledOrEmptyField(ListElement):
    def __repr__(self):
        return """FilledOrEmptyField({self.field},{self.filledCase},{self.emptyCase})"""
    
    def __init__(self,field,filledCase = emptyGen, emptyCase = emptyGen,  **kwargs):
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
            )],  **kwargs)
        
class AtLeastOneField(SingleChild):
    """Show the child if there is at least one condition.

    The child is repeated as many time in the card's template as they
    are fields. So use this only for small text, such as
    <table>

    """
    def __repr__(self):
        return f"""AtLeastOneField({self.child},{self.fields})"""

    def __init__(self,child, fields):
        super().__init__(child)
        self.fields = fields

    def _getNormalForm(self):
        actual = emptyGen
        child = self.child.getNormalForm()
        for condition in self.fields:
            actual = FilledOrEmptyField(condition, filled = child,
                                     isEmpty = actual).getNormalForm()
        return actual

class FilledField(FilledOrEmptyField):
    def __repr__(self):
        return f"""FilledField({self.field},{self.child})"""
    
    def __init__(self, field, child,  **kwargs):
        super().__init__(field, filledCase = child,  **kwargs)
        
class EmptyField(FilledOrEmptyField):
    def __repr__(self):
        return f"""EmptyField({self.field},{self.child})"""
    def __init__(self, field, child,  **kwargs):
        super().__init__(field, emptyCase = child,  **kwargs)
    
class QuestionOrAnswerField(ListElement):
    def __repr__(self):
        return f"""QuestionOrAnswerFieldField({self.field},{self.questionCase},{self.answerCase})"""
    
    def __init__(self, questionCase = emptyGen, answerCase = emptyGen,  **kwargs):
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
            )],  **kwargs)
        
class QuestionField(QuestionOrAnswerField):
    def __repr__(self):
        return f"""QuestionField({self.field},{self.child})"""
    def __init__(self, child,  **kwargs):
        super().__init__(questionCase = child,  **kwargs)

class AnswerField(QuestionOrAnswerField):
    def __repr__(self):
        return f"""AnswerField({self.field},{self.child})"""
    def __init__(self, child,  **kwargs):
        super().__init__(answerCase = child,  **kwargs)
        
    
        
class PresentOrAbsentFieldField(ListElement):
    def __repr__(self):
        return f"""PresentOrAbsentFieldField({self.field},{self.presentCase},{self.absentCase})"""
    
    def __init__(self, field, presentCase = emptyGen, absentCase = emptyGen,  **kwargs):
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
            , **kwargs)
    
class PresentField(PresentOrAbsentField):
    def __repr__(self):
        return f"""PresentField({self.field},{self.child})"""
    
    def __init__(self, field, child,  **kwargs):
        super().__init__(field, presentCase = child,  **kwargs)
        
class AbsentField(PresentOrAbsentField):
    def __repr__(self):
        return f"""AbsentField({self.field},{self.child})"""
    def __init__(self, field, child,  **kwargs):
        super().__init__(field, absentCase = child,  **kwargs)
