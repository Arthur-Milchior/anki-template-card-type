from .general import header, footer
from ..generators.imports import *

increaseRelation=QuestionnedField(field="Smaller to greater",
                                  child=FilledOrEmpty("Smaller to greater",
                                                      {"Smaller to greater"},
                                                      "implies"))
decreaseRelation=QuestionnedField(field="Greater to smaller",
                                  child=FilledOrEmpty("Greater to smaller",
                                                      {"Greater to smaller"},
                                                      FilledOrEmpty("Smaller to greater",
                                                                    {"Smaller to greater"},
                                                                    "implied by")))

def connexion(nb,side,default="and"):
    return Filled(f"{side}{nb+1}",
                  [FilledOrEmpty(f"Connect {side}{nb}",
                                 {f"Connect {side}{nb}"},
                                 default),
                   QuestionnedField(f"{side}{nb+1}")])

def bigSide(side):
    return [{f"Prefix {side}"},
            QuestionnedField(f"{side}0"),
            connexion(0,side),
            connexion(1,side),
            connexion(2,side,default=FilledOrEmpty(f"Connect {side}0",
                                                   {f"Connect {side}0"},
                                                   "and"))]
smaller=bigSide("Smaller")
greater=bigSide("Greater")

increaseList = [QuestionnedField("smallest"),
                smaller,
                QuestionnedField("Intermediate"),
                greater,
                QuestionnedField("Greatest"),
                QuestionnedField("Equivalent"),
                QuestionnedField("Equivalent2"),
                QuestionnedField("Equivalent3"),
]
decreaseList=list(reversed(increaseList))
def alternate(list,relation):
    l=[list[0]]
    for i in range(1,len(list)):
        l.append(relation)
        l.append(list[i])
    return AskedOrNot("Definition",
                      "???",
                      l)

def longLine(list,relation):
    return [header,alternate(list,relation),hr, footer]
        
increase=longLine(increaseList,increaseRelation)
decrease=longLine(decreaseList,decreaseRelation)

def relation(left,right):
    if left<right:
        relation = increaseRelation
        asked="Smaller to greater"
    elif right<left:
        relation = decreaseRelation
        asked="Greater to smaller"
    else:
        assert False
    relation.assumeAsked(asked)
    leftField=increaseList[left]
    rightField=increaseList[right]
    return [header, leftField,relation,rightField,hr,footer]
    
