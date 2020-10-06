from ...generators import *
from ..util import *

singleNameAsked = DecoratedField("Name",
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
    return Filled(name, [decorateName(Field(name)), relatedInformations(i)])

allNames = UL([nameLine(i) for i in range(1, 5)])

def cascade(child):
    return Cascade("Names",
                child,
                {f"Name{empty1(i)}" for i in range(1,5)})

"""One name or a list of name

suffix -- after names if there is any
"""
def names(suffix=None):
    return cascade(
        Filled("Name", [
            FilledOrEmpty("Name2", allNames, singleName),
            suffix
        ]))

def nameAsked(i):
    """Give all information about given name and ask name i

    suffix -- after names if there is any
    """
    l = []
    for j in range(i + 1, i + 4):
        if j > 4:
            j -= 4
        l.append(nameLine(j))
    if i == 1:
        i = ""
    l.append(LI(AskedField(f"Name{i}", question="Or ?")))
    return addBoilerplate(cascade([UL(l, addLi=False), Filled("Name", hr)]))
