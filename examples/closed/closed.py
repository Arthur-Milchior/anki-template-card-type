from ...generators import *
from ...generators.ensureGen import ensureGen
from ..general import footer, header

from ..util import *
from ..style import *

_label = [Field("Name", isMandatory=True), " "]

def _no(i):
    return Filled(f"Not{empty1(i)}",
                    "not ")

def _construction(i, onAnswer=None):
    construction = f"Construction{empty1(i)}"
    if onAnswer is None:
        onAnswer = lambda x: x
    return Filled(construction,
                  [hr, onAnswer(Field(construction))])

def _counterExample(i, onAnswer=None):
    counterExample = f"CounterExample{empty1(i)}"
    if onAnswer is None:
        onAnswer = lambda x: x
    return Filled(counterExample, [hr, onAnswer(Field(counterExample))])


def _shortLine(i, onAnswer=None):
    """ is {{not}} closed under {{under}} when {{condition}}.
    onAnswer -- what to do to important part of the answer"""
    if onAnswer is None:
        onAnswer = lambda x: x
    empty_i = empty1(i)
    underField = f"Under{empty_i}"
    conditionField = f"Condition{empty_i}"
    closureField = f"Closure{empty_i}"
    closure = FilledOrEmpty(closureField,
                            FilledOrEmpty(f"Not{empty1(empty_i)}",
                                          _no(empty_i),
                                          [" ", {closureField}, " "],
                            ),
                            [" is ", _no(empty_i), " closed under "])
    return [
        closure,
        onAnswer(Field(underField)),
        Filled(conditionField, [" when ", onAnswer(Field(conditionField))]),
    ]


def _line(i, onAnswer=None):
    """ is {{not}} closed under {{under}} when {{condition}}.
    onAnswer -- what to do to important part of the answer"""
    if onAnswer is None:
        onAnswer = lambda x: x
    return [
        _shortLine(i, onAnswer=onAnswer),
        _counterExample(i, onAnswer),
        _construction(i, onAnswer),
    ]

def closedWhen(i):
    i = empty1(i)
    underField = f"Under{i}"
    conditionField = f"Condition{i}"
    closureField = f"Closure{i}"
    closure = FilledOrEmpty(closureField, [" ", {closureField}, " "], " is closed under ")
    question = [closure, Field(underField), decorateQuestion(" when ")]
    answer = [" ", _line(i, onAnswer=decorateQuestion)]
    return addBoilerplate([_label, QuestionOrAnswer(question, answer)], underField)

nbClosure = 11
def closedMissing(i):
    l = []
    for j in range (i+1, i+nbClosure):
        if j > nbClosure:
            j -= nbClosure
        underField = f"Under{empty1(j)}"
        l.append(Filled(underField, LI(_shortLine(j))))
    l.append(
        LI(QuestionOrAnswer(decorateQuestion("and ?"),
                            _shortLine(i, onAnswer=decorateQuestion)
    )))
    return addBoilerplate([
        _label,
        UL(l, addLi=False),
    ],
                          {f"Under{empty1(i)}"}
    )

def closedWhenConstruction(i):
    construction = f"Construction{empty1(i)}"

    content = addBoilerplate([_label, _shortLine(i), hr, QuestionOrAnswer( H3("Proof?"), {construction})])
    return Filled(construction, content)

def closedWhenCounterExample(i):
    counterExample = f"CounterExample{empty1(i)}"
    content = addBoilerplate([_label, _shortLine(i), hr, QuestionOrAnswer( H3("Counter-example?"), {counterExample})])
    return Filled(counterExample, content)


allCloses = addBoilerplate(
    [_label,
     QuestionOrAnswer([" is ", br, decorateQuestion("closed under"), "?"],
                      UL([Filled(f"Under{empty1(j)}", LI(_shortLine(j, onAnswer=decorateQuestion))) for j in range(1,nbClosure+1)]
                         , addLi=False))]
)
