from ..general.head import header
from ..general.foot import footer
from ..general.typ import typDic
from ...generators import *


labelDef= [Filled("DefType",
                  [QuestionnedField("DefType",
                                    isMandatory=True),
                   " such that "]),
           FilledOrEmpty("Conjdef",
                         QuestionnedField("Conjdef",["Conjdef"]),
                         Filled ("Definition2",
                                 FilledOrEmpty("Typ",
                                               "equivalently",
                                               "Equivalently")))
           ]
labelDef =  Cascade("Definitions",
                    Cascade("Conjdef",
                            labelDef,
                            {"DefType"}),
                    {"Conjdef"})


definitions = ("Definition",
               [PotentiallyNumberedFields(fieldPrefix = "Definition",
                                          greater = 16,
                                          label = labelDef,
                                          infix = ""),
                hr])

for i in range(1,4):
    name = "Part"+("" if i==1 else str(i))
    content = set()
    for j in range(4):
        d = 4*(i-1)+j
        content.add("Definition"+("" if d==1 else str(d)))
    definitions = Cascade(name,
                          definitions,
                          content)

other = TableFields([{"field":"Construction",
                      "showIfAskedOrAnswer":True},
                     {"field":"Property",
                      "showIfAskedOrAnswer":True},
                     {"field":"Cardinal",
                      "showIfAskedOrAnswer":True},
                     typDic])

definition = [header,definitions,other,footer]
