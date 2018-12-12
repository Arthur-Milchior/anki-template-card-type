from ..child import SingleChild
from ..leaf import emptyGen
from ..children import MultipleChild, ListElement
from ..child import Requirement
from .sugar import NotNormal

class FilledOrEmptyField(ListElement):
    def __repr__(self):
        return """FilledOrEmptyField({self.field},{self.filledCase},{self.emptyCase})"""
    
    def __init__(self,field,filledCase = emptyGen, emptyCase = emptyGen,  **kwargs):
        self.filledCase = filledCase
        self.emptyCase = emptyCase
        self.field = field
        super().__init__([
            Requirement(
                self.filledCase.getNormalForm(),
                requireFilled = {self.field}
            ),
            Requirement(
                self.emptyCase.getNormalForm(),
                requireEmpty = {self.field}
            )],  **kwargs)
        

class AtLeastNField(SingleChild, NotNormal):
    """Show the child if at least n of the fields have content.

    If there are m fields, then the length of the text generated is
    O(m choose n). For n=1, it means the text is linear in the number
    of fields. For n=2, it means the text is square in the number of fields.

    So use this only for small text, such as
    <table>.
    """
    def __init__(self, child, fields, n=1):
        super().__init__(child)
        self.n = n
        self.fields = fields
        
    def __repr__(self):
        return f"""AtLeastNField({self.child},{self.fields},{self.n})"""

    def _getNormalForm(self):
        if self.n = 0:
            return self.child.getNormalForm()
        seen = set()
        seen_card = 0
        actual = emptyGen
        for condition in self.fields:
            if seen_card >= self.n-1:
                actual = FilledOrEmptyField(condition,
                                            filledCase = AtLeastNField(self.child, seen, self.n-1),
                                            emptyCase = actual)
            seen_card +=1
            seen.add(condition)
        return actual.getNormalForm()

class AtLeastOneField(AtLeastNField):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, n=1,**kwargs)
class AtLeastTwoField(AtLeastTwoField):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, n=2,**kwargs)
        
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
        return f"""QuestionOrAnswerField({self.field},{self.questionCase},{self.answerCase})"""
    
    def __init__(self, questionCase = emptyGen, answerCase = emptyGen,  **kwargs):
        self.questionCase = questionCase
        self.answerCase = answerCase
        super().__init__([
            Requirement(
                self.questionCase.getNormalForm(),
                requireQuestion = True
            ),
            Requirement(
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
        
class PresentOrAbsentField(ListElement):
    def __repr__(self):
        return f"""PresentOrAbsentField({self.field},{self.presentCase},{self.absentCase})"""
    
    def __init__(self, field, presentCase = emptyGen, absentCase = emptyGen,  **kwargs):
        self.presentCase = presentCase
        self.absentCase = absentCase
        self.field = field
        elements = super().__init__(
            [
                Requirement(
                    self.presentCase.getNormalForm(),
                    inModel = {self.field}
                ),
                Requirement(
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
