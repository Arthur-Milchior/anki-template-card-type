from ...generators import *
from ..util import *
from ..style import *


notation_mj_field = "Notation (mathjax)"
notation_mj = mathjax(bareField(notation_mj_field))

"""The value in Notation or Notation (mathjax)"""
either_notation_field = FilledOrEmpty("Notation", {"Notation"}, notation_mj)

"""The generator if we ask for notation, and there is a single one."""
singleNotationAsked = QuestionnedField("Notation",
                                       emphasizing=decorateQuestion,
                                       child = either_notation_field)

def singleNotation(emphasizing=lambda x:x):
    """The generator if there is a single notation."""
    return AskedOrNot("Notation",
                      singleNotationAsked,
                      emphasizing(notation_mj))

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
    notations_if_filled = FilledOrEmpty("Notation",
                                 notation_shown, Filled(notation_mj_field, notation_shown))
    return Cascade(field="Notations", 
                   child=notations_if_filled, 
                   cascade={numbered_field("Notation", i) for i in range(1, 5)}|{notation_mj_field})

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
