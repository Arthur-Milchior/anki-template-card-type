from ..singleChild import SingleChild, Requirement
from ..leaf import emptyGen
from ..multipleChildren import MultipleChildren, ListElement, Name, QuestionOrAnswer
from .sugar import NotNormal
from ...utils import firstTruth

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
                 cascadeAsked = frozenset(),
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
        self.inputs = dict()
        def addIfNotNone(key, value):
            if value is not None:
                self.inputs[key] = value
        addIfNotNone("default", default)
        addIfNotNone("question", question)
        addIfNotNone("answerAsked", answerAsked)
        addIfNotNone("answerNotAsked", answerNotAsked)
        addIfNotNone("answer", answer)
        addIfNotNone("asked", asked)
        addIfNotNone("notAsked", notAsked)
        addIfNotNone("questionAsked", questionAsked)
        addIfNotNone("questionNotAsked", questionNotAsked)
        addIfNotNone("children", children)
        addIfNotNone("cascadeAsked", cascadeAsked)
        addIfNotNone("name", name)
 
        questionAsked = firstTruth([questionAsked, asked, question, children.get((True,True)), default, emptyGen])
        questionNotAsked = firstTruth([questionNotAsked, notAsked, question, children.get((True,False)), default, emptyGen])
        answerAsked = firstTruth([answerAsked, asked, answer, children.get((False,True)), default, emptyGen])
        answerNotAsked = firstTruth([answerNotAsked, notAsked, answer, children.get((False,False)), default, emptyGen])
        
        asked = questionAsked if questionAsked == answerAsked else QuestionOrAnswer(questionAsked, answerAsked, **kwargs)
        notAsked = questionNotAsked if questionNotAsked == answerNotAsked else QuestionOrAnswer(questionNotAsked, answerNotAsked, **kwargs)

        super().__init__(name = name,
                         asked = asked,
                         notAsked = notAsked,
                         cascadeAsked = cascadeAsked,
                         **kwargs)

    # def __repr__(self):
    #     t= f"Branch("
    #     for key in self.inputs:
    #         t+=f"{key}: {self.inputs[key]}, "
    #     t+=")"
    #     return t

class FilledOrEmptyField(ListElement):
    # def __repr__(self):
    #     return """FilledOrEmptyField({self.field},{self.filledCase},{self.emptyCase})"""
    
    def __init__(self,field,filledCase = emptyGen, emptyCase = emptyGen,  **kwargs):
        self.filledCase = filledCase
        self.emptyCase = emptyCase
        self.field = field
        super().__init__([
            Requirement(
                child = self.filledCase,
                requireFilled = {self.field}
            ),
            Requirement(
                child = self.emptyCase,
                requireEmpty = {self.field}
            )],  **kwargs)
        

class FilledField(FilledOrEmptyField):
    def __init__(self, field, child,  **kwargs):
        self.child = child
        super().__init__(field, filledCase = child,  **kwargs)
    # def __repr__(self):
    #     return f"""FilledField({self.field},{self.child})"""
        
class EmptyField(FilledOrEmptyField):
    def __init__(self, field, child,  **kwargs):
        self.child = child
        super().__init__(field, emptyCase = child,  **kwargs)
    # def __repr__(self):
    #     return f"""EmptyField({self.field},{self.child})"""
    
class QuestionField(QuestionOrAnswer):
    def __init__(self, child,  **kwargs):
        self.child = child
        super().__init__(questionCase = child,  **kwargs)
    # def __repr__(self):
    #     return f"""QuestionField({self.field},{self.child})"""

class AnswerField(QuestionOrAnswer):
    def __init__(self, child,  **kwargs):
        self.child = child
        super().__init__(answerCase = child,  **kwargs)
    # def __repr__(self):
    #     return f"""AnswerField({self.field},{self.child})"""
        
class PresentOrAbsentField(ListElement):
    def __init__(self, field, presentCase = emptyGen, absentCase = emptyGen,  **kwargs):
        self.child = child
        self.presentCase = presentCase
        self.absentCase = absentCase
        self.field = field
        elements = super().__init__(
            [
                Requirement(
                    child = self.presentCase.getNormalForm(),
                    requireInModel = {self.field}
                ),
                Requirement(
                    child = self.absentCase.getNormalForm(),
                    requireAbsentOfModel = {self.field}
                )]
            , **kwargs)
    # def __repr__(self):
    #     return f"""PresentOrAbsentField({self.field},{self.presentCase},{self.absentCase})"""
    
class PresentField(PresentOrAbsentField):
    def __init__(self, field, child,  **kwargs):
        self.child = child
        super().__init__(field, presentCase = child,  **kwargs)
    # def __repr__(self):
    #     return f"""PresentField({self.field},{self.child})"""
        
class AbsentField(PresentOrAbsentField):
    def __init__(self, field, child,  **kwargs):
        self.child = child
        super().__init__(field, absentCase = child,  **kwargs)
    # def __repr__(self):
    #     return f"""AbsentField({self.field},{self.child})"""
