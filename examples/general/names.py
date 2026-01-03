from ...generators import *
from ..util import *
from ..style import *

singleNameAsked = QuestionnedField("Name",
                                 emphasizing=decorateQuestion)
singleName = AskedOrNot("Name",
                        singleNameAsked,
                        decorateName(Field("Name"))
)

namesAsked = decorateQuestion("Names")

def singleRelatedInformation(i):
    """ A function which asks some information about the i-th name """
    return (lambda f:
            {"child": Parenthesis(DecoratedField(field=f"{f}{i}",
                                                 label=f,
                                                 suffix="",
                                                 classes=f)),
             "filledFields": [f"{f}{i}"]})


def relatedInformations(i=""):
    """List of information about the i-th name to give"""
    return ListFields(fields=[f"Abbreviation", f"French", f"Etymology"],
                      localFun=singleRelatedInformation(i))

def nameLine(i):
    """Give all information about the i-th name"""
    name = f"""Name{empty1(i)}"""
    return Filled(name,
                  LI([
                      AskedOrNot(name,
                                 QuestionnedField(name, emphasizing=decorateQuestion),
                                 QuestionnedField(name, emphasizing=decorateName)),
                      relatedInformations(i)]
                  ))

allNames = UL([nameLine(i) for i in range(1, 5)], addLi=False)

def cascade(child):
    return Cascade("Names",
                child,
                {numbered_field("Name", i) for i in range(1,5)})

"""One name or a list of name

suffix -- after names if there is any
"""
def names(suffix=None):
    """ suffix -- what to put after Name if there is a snigle line"""
    names_content = FilledOrEmpty("Name2", allNames, [singleName, suffix])
    name_shown = AskedOrNot("Names",
                            QuestionOrAnswer([decorateQuestion("Name(s) ?"), suffix],
                                             decorateQuestion(names_content)),
                            names_content)
    return cascade(
        Filled("Name", name_shown))

def nameAsked(i):
    """Give all information about given name and ask name i

    suffix -- after names if there is any
    """
    l = []
    for j in range(i + 1, i + 4):
        if j > 4:
            j -= 4
        l.append(nameLine(j))
    l.append(LI(AskedField(numbered_field("Name", i), question="Or ?")))
    content = addBoilerplate(cascade([UL(l, addLi=False), Filled("Name", hr)]))
    return Filled(f"Name{i if i > 1 else 2}", content)
