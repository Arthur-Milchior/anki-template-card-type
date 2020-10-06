from ...generators import *
from ..util import *
from .names import names

singleCounterexampleAsked = decorateQuestion("Counterexample")
singleCounterexample = AskedOrNot("Counterexamples",
                        singleCounterexampleAsked,
                        decorateName(Field("Counterexample"))
)

counterexamplesAsked = decorateQuestion("Counterexamples")

def counterexampleLine(i):
    return f"Counterexample{empty1(i)}"

allCounterexamples = UL([counterexampleLine(i) for i in range(1, 5)])
counterexamples = Filled("Counterexample", FilledOrEmpty("Counterexample2", singleCounterexample, allCounterexamples))

def counterexampleAsked(i):
    """Give all information about given counterexample and ask counterexample i"""
    l = []
    for j in range(i + 1, i + 4):
        if j > 4:
            j -= 4
        l.append(counterexampleLine(j))
    l.append(AskedField(f"Counterexample{empty1(i)}", question="Or ?"))
        # ask example 1 separately only if there are multiple examples
    counterexample = addBoilerplate([names(), hr, UL(l)])
    if i == 1:
        # ask counterexample 1 separately only if there are multiple counterexamples
        counterexample = Filled("Counterexample2", counterexample)
    return counterexample


counterexamplesAsked = addBoilerplate(
    [names(suffix=hr), counterexamples], "Counterexample"
).assumeAsked(["Counterexample", "Counterexample2", "Counterexample3", "Counterexample4"])
