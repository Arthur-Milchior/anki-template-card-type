from typing import List, Union
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
        return addBoilerplate(
            FromAndTo(questionField, fieldToQuestion, actualQuestion, questionToAnswer, answer, classes=answerPrefix),
            {questionField, answer})
    return fun        



def addBoilerplate(gen, asked: Union[str, List[str]]=[]):
    if (isinstance(asked, str) ):
        asked = [asked]
    gen = ListElement([header, gen, footer])
    for asked in asked:
        gen = Filled(asked, gen)
    # for mandatory in askedAndMandatory:
    #     gen = gen.assumeAsked(mandatory)
    return gen

def empty1(i):
    """Return the number, or nothing if the input is 1"""
    if i == 1:
        return ""
    return str(i)
