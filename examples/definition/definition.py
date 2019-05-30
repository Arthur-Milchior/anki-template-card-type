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
               PotentiallyNumberedFields(fieldPrefix = "Definition",
                                          greater = 16,
                                          label = labelDef,
                                         infix = ""))

definitions_names = ["Definition"]+[f"Definition{i}" for i in range(2,17) ]

definitions = ("All",
               AtLeastOneField(definitions,
                               definitions_names,
                               asked = True,
                               otherwise = {"All"}
               ),
               definitions)

for i in range(1,5):
    name = "Part"+("" if i==1 else str(i))
    content = set()
    for j in range(1,5):
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
music = Asked("Definition",Question({"Music"}))

definition = [header,definitions,other,footer, music]
