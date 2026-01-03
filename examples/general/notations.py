from ...generators import *
from ..util import *
from ..style import *

singleNotationAsked = QuestionnedField("Notation",
                                       emphasizing=decorateQuestion)
def singleNotation(emphasizing=lambda x:x):
    return AskedOrNot("Notation",
                      singleNotationAsked,
                      emphasizing(Field("Notation"))
    )

notationsAsked = decorateQuestion("Notations")

def notationLine(i, emphasizing = lambda x:x):
    notationField = numbered_field("Notation", i)
    return Filled(notationField, LI(QuestionnedField(notationField, emphasizing=emphasizing)))

def allNotations(emphasizing = lambda x:x):
    return UL([notationLine(i, emphasizing) for i in range(1, 5)], addLi=False)

def notations(suffix=None):
    """Show all notations or ask Notations.

    suffix -- sufix if there is a single element
    """
    def notation_content(emphasizing= lambda x:x):
        return FilledOrEmpty("Notation2",
                             allNotations(emphasizing=emphasizing),
                             [singleNotation(emphasizing=emphasizing), suffix])
    notation_shown = AskedOrNot("Notations",
                                QuestionOrAnswer([decorateQuestion("Notation(s) ?"), suffix],
                                                 notation_content(emphasizing = decorateQuestion)),
                                notation_content(emphasizing=decorateName))
    notations_if_filled = Filled("Notation",
                                 notation_shown)
    return Cascade(field="Notations", child=notations_if_filled, cascade={numbered_field("Notation", i) for i in range(1, 5)})

def notationAsked(i):
    """Give all information about given notation and ask notation i"""
    l = []
    for j in range(i + 1, i + 4):
        if j > 4:
            j -= 4
        l.append(Filled(numbered_field("Notation", j), notationLine(j, emphasizing=decorateName)))
    l.append(AskedField(numbered_field("Notation", i), question="Or ?"))
    content = addBoilerplate(UL(l, addLi=False))
    return Filled(f"Notation{i if i > 1 else 2}", content)
