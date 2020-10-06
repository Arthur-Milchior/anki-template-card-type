from ...generators import *
from ...generators.ensureGen import ensureGen
from ..general import footer, header

from ..util import *

_label = [Field("Name", isMandatory=True), " "]

def _no(i):
    return Filled(f"Not{empty1(i)}",
                    "not ")

def _line(i, onAnswer=None):
    """ is {{not}} closed under {{under}} when {{condition}}.
    onAnswer -- what to do to important part of the answer"""
    if onAnswer is None:
        onAnswer = lambda x: x
    i = empty1(i)
    underField = f"Under{i}"
    conditionField = f"Condition{i}"
    return [" is ", _no(i), " closed under ", onAnswer(Field(underField)), Filled(conditionField, [" when ", onAnswer(Field(conditionField))])]

def closedWhen(i):
    i = empty1(i)
    underField = f"Under{i}"
    conditionField = f"Condition{i}"
    question = [" is closed under ", Field(underField), decorateQuestion(" when ")]
    answer = [" ", _line(i, onAnswer=decorateQuestion)]
    return addBoilerplate([_label, QuestionOrAnswer(question, answer)], underField)

nbClosure = 11
def closedMissing(i):
    l = []
    for j in range (i+1, i+nbClosure):
        if j > nbClosure:
            j -= nbClosure
        underField = f"Under{empty1(j)}"
        l.append(Filled(underField, LI(_line(j))))
    l.append(
        LI(QuestionOrAnswer(decorateQuestion("and ?"),
                            _line(i, onAnswer=decorateQuestion)
    )))
    return addBoilerplate([_label, UL(l, addLi=False)])

allCloses = addBoilerplate(
    [_label,
     QuestionOrAnswer([" is ", br, decorateQuestion("closed under"), "?"],
                      UL([Filled(f"Under{empty1(j)}", LI(_line(j, onAnswer=decorateQuestion))) for j in range(1,nbClosure+1)]
                         , addLi=False))]
)

# def no(i):
#     """ ??? on question side if asked
#     "no" or "" otherwise. I.e. indicate negation correctly"""
#     filled = Filled(f"Not{empty1(i)}",
#                     "not ")
#     alo = AtLeastOneField(fields=[f"Condition{empty1(i)}", f"Under{empty1(i)}", f"Unders", "Conditions"],
#                           asked=True,
#                           child=markOfQuestion,
#                           otherwise=filled)
#     return QuestionOrAnswer(alo,
#                             filled)


# def when(i):
#     """ 
#     "when {{condition}}" on answer side.
#     Nothing on question side if no restriction
#     <H2>when</H2> on question side if Condition{i} asked"""
#     answer = DecoratedField(field=f"Condition{empty1(i)}",
#                             label="when ",
#                             classes="Condition",
#                             infix="",
#                             emphasizing=decorateQuestion,
#                             suffix="",
#                             isMandatory=True)
#     question = [Label("when",
#                       fields=[f"Condition{empty1(i)}", f"Under{empty1(i)}"],
#                       classes=["Condition"],
#                       emphasizing=decorateQuestion,
#     ),
#                 markOfQuestion]
#     alo = AtLeastOneField(fields=[f"Condition{empty1(i)}", f"Under{empty1(i)}"],
#                           asked=True,
#                           child=question,
#                           otherwise=answer)
#     return QuestionOrAnswer(alo,
#                             answer)


# def closedUnder(i):
#     """
#     "is closed under bar" if asked
#     or 
#     "is (not) closed under" """
#     # {{prefix}} not {{closure}}. 
#     withClosure = [FilledOrEmpty(f"Prefix{empty1(i)}",
#                             Field(f"Prefix{empty1(i)}"),
#                             ""),
#               " ",
#               no(i),
#               " ",
#               Field(f"Closure{empty1(i)}")]
#     # is not closed under
#     withoutClosure = ["is ", no(i), " closed under"]
#     return DecoratedField(field=f"Under{empty1(i)}",
#                           label=FilledOrEmpty(f"Closure{empty1(i)}",
#                                               withClosure,
#                                               withoutClosure),
#                           classes="Under",
#                           infix="",
#                           suffix="",
#                           isMandatory=True)


# def line(i):
#     """ "Closed under bar when ???"
#     or "closed under bar when foo" """
#     return [closedUnder(i), " ", when(i)]


# """ List of cases under which {name} is closed."""
# _closed = NumberedFields(fieldPrefix="Under",
#                          greater=11,
#                          label=label,
#                          localFun=(lambda i: {"child": LI(line(str(i))),
#                                               "questions": {f"Under{empty1(i)}"},
#                                               "filledFields": [f"Under{empty1(i)}"]}),
#                          unordered=True,
#                          )


# def _counterExample(i=""):
#     """Show a counter example on answer side only  """
#     return Answer(DecoratedField(field=f"CounterExample{empty1(i)}",
#                                  label="Counter example",
#                                  suffix=hr))


# closeds = addBoilerplate(_closed)


# def closed(i=""):
#     """ {{name}} is {{not}} closed under {{closed}} when ???{{when}}. <hr>{{counterExample}}"""
#     return addBoilerplate(
#         [label,
#          ensureGen(line(str(i))).assumeAsked(f"Condition{empty1(i)}"),
#          hr,
#          _counterExample(i)], f"Under{empty1(i)}")
