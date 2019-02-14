from ..general.head import header
from ..general.foot import footer
from ..general.typ import typDic
from ...generators import *


labelDef= [Filled("Typ",
                  [QuestionnedField("DefType"),
                   " such that "]),
           FilledOrEmpty("Conjdef",
                         QuestionnedField("Conjdef",["Conjdef"]),
                         Filled ("Definition2",
                                 FilledOrEmpty("Typ",
                                               "equivalently",
                                               "Equivalently")))
           ]
labelDef =  Cascade("Definitions",
                    labelDef,
                    {"Conjdef","DefType"})


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
        d = 4*i+j
        content.add("Definition"+("" if d==1 else str(d)))
    definitions = Cascade(name,
                          definitions,
                          content)

other = TableFields(["Construction",
                     "Property",
                     "Cardinal",
                     typDic])

definition = [header,definitions,other,footer]
