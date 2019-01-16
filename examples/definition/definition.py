from ..general import header, footer, typDic
from ...generators.imports import *

labelDef= FilledOrEmpty("Conjdef",
                        Cascade("Definitions",[": ",QuestionnedField("Conjdef",["Conjdef"])],["Conjdef"]),
                        Filled ("Definition2","Equivalently: "))


definitions = ("Definition",
               [PotentiallyNumberedFields(fieldPrefix="Definition",
                                          greater=16,
                                          label=labelDef),
                hr])
other = TableFields(["Construction",
                     "Property",
                     typDic])

definition = [header,definitions,other,footer]

