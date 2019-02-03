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
other = TableFields(["Construction",
                     "Property",
                     "Cardinal",
                     typDic])

definition = [header,definitions,other,footer]
