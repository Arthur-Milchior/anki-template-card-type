from ...generators import *
from ..util import *
from ..style import *
from .names import names

singleCounterexampleAsked = QuestionnedField("Counterexample")
singleCounterexample = AskedOrNot("Counterexample",
                        singleCounterexampleAsked,
                        decorateName(Field("Counterexample"))
)

def counterexampleLine(i):
    counterExampleField = f"Counterexample{empty1(i)}"
    return Filled(counterExampleField, QuestionnedField(counterExampleField, emphasizing=decorateQuestion))

allCounterexamples = UL([counterexampleLine(i) for i in range(1, 5)])
counterexamples = Filled("Counterexample", FilledOrEmpty("Counterexample2", allCounterexamples, singleCounterexample))

def counterexampleAsked_(i):
    """Give all information about given counterexample and ask counterexample i"""
    l = []
    for j in range(i + 1, i + 4):
        if j > 4:
            j -= 4
        l.append(counterexampleLine(j))
    l.append(AskedField(f"Counterexample{empty1(i)}", question="Or ?"))
    return UL(l, addLi=False)

def counterexampleAsked(i):
    return Filled(f"Counterexample{empty1(i)}",
                  Filled("Counterexample2",
                         addBoilerplate(
                             [
                                 names(),
                                 hr,
                                 decorateSection("Counter-example(s)"),
                                 counterexampleAsked_(i)]
                         )))


def counterexamplesAskedParam(content=names(suffix=hr)):
    return addBoilerplate(
        [content, DecoratedField("Counterexample", child=counterexamples)],  "Counterexample"
    )

counterexamplesAsked = counterexamplesAskedParam()
