from ..generators.imports import *
from .general import contextOrDeck

def _question(questionFieldPrefix, fieldToQuestion, actualQuestion, questionToAnswer, answerPrefix):
    """Intuitively, it is ```{{questionFieldPrefix}} fieldToQuestion
    <class>actualQuestion</class> questionToAnswer {{answerPrefix}}```
    Prefix are suffixed with i, and the questions is asked only if there is enough information.

    """
    def fun(i=""):
        questionField = f"{questionFieldPrefix}{i}"
        answer = f"{answerPrefix}{i}"
        return FromAndTo(questionField, fieldToQuestion, actualQuestion, questionToAnswer, answer)
    return fun

_abbreviation = _question("Abbreviation", " is the ", "abbreviation", " of ", "Name")
_etymology = _question("Name", "'s ", "etymology", " is ", "Etymology")
def _language(question, answer, language):
    return _question(question," in ", language, " is ", answer)
_french= _language("Name","French","French")
_english= _language("French","Name","English")

french = _french()
french2=_french("2")
english = _english()
english2=_english("2")
abbreviation = _abbreviation()
abbreviation2 = _abbreviation("2")
abbreviation3 = _abbreviation("3")
etymology = _etymology()
etymology2 = _etymology("2")
