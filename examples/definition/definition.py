from ..general.head import header
from ..general.foot import footer
from ..general.typ import typDic
from ...generators import *

labelDef= FilledOrEmpty("Conjdef",
                        Cascade("Definitions",
                                [QuestionnedField("Conjdef",["Conjdef"]),": "],
                                ["Conjdef"]),
                        Filled ("Definition2",
                                "Equivalently: "))


definitions = ("Definition",
               [PotentiallyNumberedFields(fieldPrefix = "Definition",
                                          greater = 16,
                                          label = labelDef,
                                          infix = ""),
                hr])
other = TableFields(["Construction",
                     "Property",
                     typDic])

definition = [header,definitions,other,footer]

