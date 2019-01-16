from .multiple import MultipleRequirement
from .questionOrAnswer import QuestionOrAnswer
from ...utils import standardContainer

class HideInSomeQuestions(QuestionOrAnswer):
    """Return child except on the question side when some field from fields is asked"""
    def __init__(self,fields,child):
        if isinstance(fields,str):
            fields=[fields]
        assert standardContainer(fields)
        question = MultipleRequirement(child = child,
                                       requireNotAsked = fields)
        answer = child
        super().__init__(question,answer)
