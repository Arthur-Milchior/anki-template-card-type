from ..generators import *
from .general import header

def _question(questionFieldPrefix, fieldToQuestion, actualQuestion, questionToAnswer, answerPrefix):
    """Intuitively, it is ```{{questionFieldPrefix}} fieldToQuestion
    <class>actualQuestion</class> questionToAnswer {{answerPrefix}}```
    Prefix are suffixed with i, and the questions is asked only if there is enough information.

    """
    def fun(i=""):
        questionField = f"{questionFieldPrefix}{i}"
        answer = f"{answerPrefix}{i}"
        return FromAndTo(questionField, fieldToQuestion, actualQuestion, questionToAnswer, answer, prefix=short_header, classes=answerPrefix)
    return fun


_represented = _question('Represents', ' ', 'is represented by', ' ', 'Name')
