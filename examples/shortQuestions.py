from ..generators import *
from .general import contextOrDeck, short_header

def _question(questionFieldPrefix, fieldToQuestion, actualQuestion, questionToAnswer, answerPrefix):
    """Intuitively, it is ```{{questionFieldPrefix}} fieldToQuestion
    <class>actualQuestion</class> questionToAnswer {{answerPrefix}}```
    Prefix are suffixed with i, and the questions is asked only if there is enough information.

    """
    def fun(i=""):
        questionField = f"{questionFieldPrefix}{i}"
        answer = f"{answerPrefix}{i}"
        return FromAndTo(questionField, fieldToQuestion, actualQuestion, questionToAnswer, answer,prefix= short_header,classes=answerPrefix)
    return fun

_abbreviation = _question("Abbreviation", " is the ", "abbreviation", " of ", "Name")
_etymology = _question("Name", "'s ", "etymology", " is ", "Etymology")
def _language(question, answer, language):
    return _question(question," in ", language, " is ", answer)
_french= _language("Name","French","French")
_english= _language("French","Name","English")
_toAbbreviation=_question("Name", "'s ", "abbreviation", " is ", "Abbreviation")
_represented=_question('Represents', ' ', 'is represented by', ' ', 'Name')

french = _french()
french2=_french("2")
english = _english()
english2=_english("2")
abbreviation = _abbreviation()
abbreviation2 = _abbreviation("2")
abbreviation3 = _abbreviation("3")
etymology = _etymology()
etymology2 = _etymology("2")
toAbbreviation = _toAbbreviation()
toAbbreviation2 = _toAbbreviation("2")
represented = _represented()
represented2 = _represented("2")
