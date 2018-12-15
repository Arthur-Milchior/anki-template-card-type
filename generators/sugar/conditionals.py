from ..singleChild import SingleChild, Requirement
from ..leaf import emptyGen
from ..multipleChildren import MultipleChildren, ListElement, Name, QuestionOrAnswer
from .sugar import NotNormal

class Branch(Name):
    """The class which expands differently in function of the question/hidden value.

    name -- the name of this question.
    children[isQuestion][isAsked] -- the field to show on the side question/answer of card (depending on isQuestion). Depending on whether this value is asked or not.
    cascadeAsked -- a set of things which will also be considered to be asked if this is asked."""

    def __init__(self,
                 name = None,
                 default = None,
                 question = None,
                 answerAsked = None,
                 answerNotAsked = None,
                 answer = None,
                 asked = None,
                 notAsked = None,
                 questionAsked = None,
                 questionNotAsked = None,
                 children = dict(),
                 toClone = None,
                 isNormal = False,
                 locals_ = None,
                 cascadeAsked = None,
                 **kwargs):
        """
        The value of self.children[isQuestion,isAsked] is:
        {isQuestion}{IsAsked} if it exists.
        {isAsked} if it exists
        {isQuestion} if it exists
        children[isQuestion,isAsked]
        {default} if it exists
        empty otherwise.

        """
        questionAsked = [questionAsked, asked, question, children.get((True,True)), default, emptyGen]
        questionNotAsked = [questionNotAsked, notAsked, question, children.get((True,False)), default, emptyGen]
        answerAsked = [answerAsked, asked, answer, children.get((False,True)), default, emptyGen]
        answerNotAsked = [answerNotAsked, notAsked, answer, children.get((False,False)), default, emptyGen]
        
        asked = questionAsked if questionAsked == answerAsked else QuestionOrAnswer(questionAsked, answerAsked, **kwargs)
        notAsked = questionNotAsked if questionNotAsked == answerNotAsked else QuestionOrAnswer(questionNotAsked, answerNotAsked, **kwargs)

        super().__init__(name, asked, notAsked, cascadeAsked = cascadeAsked, **kwargs)

class FilledOrEmptyField(ListElement):
    def __repr__(self):
        return """FilledOrEmptyField({self.field},{self.filledCase},{self.emptyCase})"""
    
    def __init__(self,field,filledCase = emptyGen, emptyCase = emptyGen,  **kwargs):
        self.filledCase = filledCase
        self.emptyCase = emptyCase
        self.field = field
        super().__init__([
            Requirement(
                self.filledCase,
                requireFilled = {self.field}
            ),
            Requirement(
                self.emptyCase,
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
        self.child = child
        super().__init__(child)
        self.n = n
        self.fields = fields
        
    def __repr__(self):
        return f"""AtLeastNField({self.child},{self.fields},{self.n})"""

    def _getNormalForm(self):
        if self.n == 0:
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
        self.child = child
        super().__init__(*args, n=1,**kwargs)
class AtLeastTwoField(AtLeastNField):
    def __init__(self,*args,**kwargs):
        self.child = child
        super().__init__(*args, n=2,**kwargs)
        
class FilledField(FilledOrEmptyField):
    def __init__(self, field, child,  **kwargs):
        self.child = child
        super().__init__(field, filledCase = child,  **kwargs)
    def __repr__(self):
        return f"""FilledField({self.field},{self.child})"""
        
class EmptyField(FilledOrEmptyField):
    def __repr__(self):
        return f"""EmptyField({self.field},{self.child})"""
    def __init__(self, field, child,  **kwargs):
        self.child = child
        super().__init__(field, emptyCase = child,  **kwargs)
    
class QuestionField(QuestionOrAnswer):
    def __repr__(self):
        return f"""QuestionField({self.field},{self.child})"""
    def __init__(self, child,  **kwargs):
        self.child = child
        super().__init__(questionCase = child,  **kwargs)

class AnswerField(QuestionOrAnswer):
    def __repr__(self):
        return f"""AnswerField({self.field},{self.child})"""
    def __init__(self, child,  **kwargs):
        self.child = child
        super().__init__(answerCase = child,  **kwargs)
        
class PresentOrAbsentField(ListElement):
    def __repr__(self):
        return f"""PresentOrAbsentField({self.field},{self.presentCase},{self.absentCase})"""
    
    def __init__(self, field, presentCase = emptyGen, absentCase = emptyGen,  **kwargs):
        self.child = child
        self.presentCase = presentCase
        self.absentCase = absentCase
        self.field = field
        elements = super().__init__(
            [
                Requirement(
                    self.presentCase.getNormalForm(),
                    requireInModel = {self.field}
                ),
                Requirement(
                    self.absentCase.getNormalForm(),
                    requireAbsentOfModel = {self.field}
                )]
            , **kwargs)
    
class PresentField(PresentOrAbsentField):
    def __repr__(self):
        return f"""PresentField({self.field},{self.child})"""
    
    def __init__(self, field, child,  **kwargs):
        self.child = child
        super().__init__(field, presentCase = child,  **kwargs)
        
class AbsentField(PresentOrAbsentField):
    def __repr__(self):
        return f"""AbsentField({self.field},{self.child})"""
    def __init__(self, field, child,  **kwargs):
        self.child = child
        super().__init__(field, absentCase = child,  **kwargs)
