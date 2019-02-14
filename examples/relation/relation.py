from ..general import header, footer
from ...generators import *


"""{{Smaller to greater}} if field else "implies" """
foe=FilledOrEmpty("Smaller to greater",
                  {"Smaller to greater"},
                  "implies")
qf=QuestionnedField(field = "Smaller to greater",
                    child = foe,
                    classes = "Definition")
increaseRelation = Parenthesis(left = " ",
                              right = " ",
                               child = qf)

"""{{Greater to smaller}} if field else {{Smaller to greater}} if field else "Implied by" """
foe = FilledOrEmpty("Smaller to greater",
                    {"Smaller to greater"},
                    "implied by")
foe = FilledOrEmpty("Greater to smaller",
                    {"Greater to smaller"},
                    foe)
qf = QuestionnedField(field = "Greater to smaller",
                      child = foe,
                      classes = "Definition")
decreaseRelation = Parenthesis(left = " ",
                               right = " ",
                               child = qf)


def connexion(nb,side,default = "and"):
    """{{Connect sidenb}} if field, else (default = "And").
    {{field side(nb+1)}}"""
    return Filled(f"{side}{nb+1}",
                  [Parenthesis(left = " ", right = " ",
                               child = FilledOrEmpty(f"Connect {side}{nb}",
                                                   {f"Connect {side}{nb}"},
                                                   default)),
                   QuestionnedField(f"{side}{nb+1}",classes="Definition2")])

def bigSide(side):
    """side0 connect0 side1 connect1 side2 connect2 side3"""
    l=[{f"Prefix {side}"},
       QuestionnedField(f"{side}0",classes="Side"),
       connexion(0,side),
       connexion(1,side),
       connexion(2,side,default = FilledOrEmpty(f"Connect {side}0",
                                                {f"Connect {side}0"},
                                                "and")),
       {f"Suffix {side}"},]
    foe=FilledOrEmpty(f"{side}0",
                      l,
                      CLASS("Error",f"Error, {side}0 is empty"))
    return Cascade(field=f"{side}s",
                   cascade={f"{side}{i}" for i in range(4)},
                   child= foe)
greater = bigSide("Greater")
smaller = bigSide("Smaller")
listOfSideFieldNames = ["Smallest",
                        "Smaller0",
                        "Intermediate",
                        "Greater0",
                        "Greatest",
                        "Equivalent",
                        "Equivalent2",
                        "Equivalent3",
                        "Smaller1",
                        "Greater1",
                        "Smaller2",
                        "Greater2",
                        "Smaller3",
                        "Greater4",
]



def df(fieldName,suffix = None,prefix = None):
    return DecoratedField(label = "",infix = None,field = fieldName,suffix = suffix,prefix = prefix,classes="Side")
listOfSideFields = [df("Smallest"),
                    smaller,
                    df("Intermediate"),
                    greater,
                    df("Greatest"),
                    df("Equivalent"),
                    df("Equivalent2"),
                    df("Equivalent3")]

increasing_ = [df("Smallest",suffix = increaseRelation),
               smaller,
               increaseRelation,
               df("Intermediate",suffix = increaseRelation),
               greater,
               df("Greatest",prefix = increaseRelation),
               df("Equivalent",prefix = increaseRelation),
               df("Equivalent2",prefix = increaseRelation),
               df("Equivalent3",prefix = increaseRelation)]
decreasing_ = [
    df("Equivalent3", suffix = decreaseRelation),
    df("Equivalent2", suffix = decreaseRelation),
    df("Equivalent", suffix = decreaseRelation),
    df("Greatest", suffix = decreaseRelation),
    greater,
    df("Intermediate", prefix = decreaseRelation),
    decreaseRelation,
    smaller,
    df("Smallest", prefix = decreaseRelation),
]


def longLine(line):
    line = [header,
            AskedOrNot("Definition",
                       QuestionOrAnswer(markOfQuestion,
                                        line),
                       line),
            hr,
            ShowIfAskedOrAnswer("Construction",
                                DecoratedField("Construction",
                                               classes = "Definition3",
                                               suffix=hr)),
            footer]
    return AtLeastOneField(asked = True,
                           fields = listOfSideFieldNames,
                           child = [Empty("Hide sides","Suspend this card"),line],
                           otherwise = line)

increasing = longLine(increasing_)
decreasing = longLine(decreasing_)


def relation(left,right):
    if left<right:
        relation = increaseRelation
        asked = "Smaller to greater"
    elif right<left:
        relation = decreaseRelation
        asked = "Greater to smaller"
    else :
        assert False
    relation = relation.getNormalForm().assumeAsked(asked)
    leftField = listOfSideFields[left]
    rightField = listOfSideFields[right]
    leftFieldName = listOfSideFieldNames[left]
    rightFieldName = listOfSideFieldNames[right]
    l = [header, leftField,relation,rightField,hr,footer]
    empty = [Empty("Hide middle","Suspend this card"),l]
    filled = Filled(leftFieldName,Filled(rightFieldName,empty))
    return filled
