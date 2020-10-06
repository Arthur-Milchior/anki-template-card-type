from ...generators import *
from ..util import *

singleNotationAsked = decorateQuestion("Notation")
singleNotation = AskedOrNot("Notations",
                        singleNotationAsked,
                        decorateName(Field("Notation"))
)

notationsAsked = decorateQuestion("Notations")

def notationLine(i):
    return decorateName(f"Notation{empty1(i)}")

allNotations = UL([notationLine(i) for i in range(1, 5)])
notations = Filled("Notation", FilledOrEmpty("Notation2", singleNotation, allNotations))

def notationAsked(i):
    """Give all information about given notation and ask notation i"""
    l = []
    for j in range(i + 1, i + 4):
        if j > 4:
            j -= 4
        l.append(Filled(f"Notation{empty1(j)}", LI(notationLine(j))))
    l.append(AskedField(f"Notation{empty1(i)}", question="Or ?"))
    return addBoilerplate(UL(l, addLi=False))
