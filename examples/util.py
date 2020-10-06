from .general.footer import footer
from .general.header import header
from ..generators import *

def question(questionFieldPrefix, fieldToQuestion, actualQuestion, questionToAnswer, answerPrefix):
    """Intuitively, it is ```{{questionFieldPrefix}} fieldToQuestion
    <class>actualQuestion</class> questionToAnswer {{answerPrefix}}```
    Prefix are suffixed with i, and the questions is asked only if there is enough information.

    """
    def fun(i=""):
        questionField = f"{questionFieldPrefix}{i}"
        answer = f"{answerPrefix}{i}"
        return FromAndTo(questionField, fieldToQuestion, actualQuestion, questionToAnswer, answer, prefix=header, classes=answerPrefix, suffix=footer)
    return fun        



def addBoilerplate(gen, askedAndMandatory=[]):
    if (isinstance(askedAndMandatory, str) ):
        askedAndMandatory = [askedAndMandatory]
    gen = [header, gen, footer]
    for asked in askedAndMandatory:
        gen = Filled(asked, gen)
    for mandatory in askedAndMandatory:
        gen.assumeAsked(mandatory)
    return gen

def empty1(i):
    if i == 1:
        return ""
    return str(i)

decorateQuestion = H3
decorateName = H2
