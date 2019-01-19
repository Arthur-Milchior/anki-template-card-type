from .meta import FieldChild
from ..generators import thisClassIsClonable, SingleChild
from ...debug import debugFun, debug
from ..listGen import ListElement

@thisClassIsClonable
class Question(SingleChild):
    """The class which expands only on the question side"""
    def _assumeQuestion(self, changeStep = False):
        return self.getChild().assumeQuestion(changeStep = changeStep)
    def _assumeAnswer(self, changeStep = False):
        return None
    def _createHtml(self, *args, **kwargs):
        raise ExceptionInverse("At this stage, Question must be removed")
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().assumeQuestion().getWithoutRedundance())
    
@thisClassIsClonable
class Answer(SingleChild):
    """The class which  expands only on the answer side."""
    @debugFun
    def _assumeQuestion(self, changeStep = False):
        return None
    def _assumeAnswer(self, changeStep = False):
        return self.getChild().assumeAnswer(changeStep = changeStep)
    def _createHtml(self, *args, **kwargs):
        raise ExceptionInverse("At this stage, Answer must be removed")
    def _getWithoutRedundance(self):
        return self.cloneSingle(self.getChild().assumeAnswer().getWithoutRedundance())
    
class QuestionOrAnswer(ListElement):
    """The class which expands differently in function of the question/answer side."""
    def __init__(self,
                 question = None,
                 answer = None,
                 **kwargs):
        self.question = question
        self.answer = answer
        super().__init__([Question(question), Answer(answer)], **kwargs)
