from ...utils import standardContainer
from .askedOrNot import Asked
from .multiple import MultipleRequirement
from .questionOrAnswer import QuestionOrAnswer


class HideInSomeQuestions(QuestionOrAnswer):
    """Return child except on the question side when some field from fields is asked"""

    def __init__(self, fields, child):
        if isinstance(fields, str):
            fields = [fields]
        assert standardContainer(fields)
        question = MultipleRequirement(child=child,
                                       requireNotAsked=fields)
        answer = child
        super().__init__(question, answer)


class ShowIfAskedOrAnswer(QuestionOrAnswer):
    """
    `ShowIfAskedOrAnswer(field, child)` is "child" unless it's the question side and "field" is not asked.
    """
    def __init__(self, field, child):
        question = Asked(field, child)
        super().__init__(question, child)
