from typing import List, Optional, Union
from .general.footer import footer
from .general.header import header
from ..generators import *


def bareField(name):
    return Field(name, useClasses=False)

def bareFieldOrDefault(name, default):
    return FilledOrEmpty(name, bareField(name), default)

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



def addBoilerplate(gen, 
                   asked: Union[str, List[str]]=[],
                   extra_variables: Optional[Gen] = None):
    if (isinstance(asked, str) ):
        asked = [asked]
    gen = ListElement([header, gen, footer(extra_variables=extra_variables)])
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

def numbered_field(field_name, i):
    """Return field_name suffixed with i, unless i == 1"""
    return f"{field_name}{empty1(i)}"

def code(languageField):
    """A function which add tag ensuring that the child is interpreted as code in language `language` or given in the field
    `languageField`."""
    def aux(child, **kwargs):
        return FilledOrEmpty(languageField,
                      PRE(
                          child=CODE(
                              child=child,
                              attrs={"class": "{{" + languageField + "}}"},
                              **kwargs
                          ),
                          **kwargs
                      ),
                      child)
    return aux