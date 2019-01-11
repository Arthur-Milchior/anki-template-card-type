from .general import header, footer
from ..generators.imports import *

labelDef=[Label("Definition",["Definition"]),
          FilledOrEmpty("Conjdef",
                      Cascade("Definitions",[": ",QuestionnedField("Conjdef",["Conjdef"])],["Conjdef"]),
                      Filled ("Definition2","Equivalently: "))
]

definitions = ("Definition",
               [PotentiallyNumberedFields(fieldPrefix="Definition",
                                          greater=16,
                                          label=labelDef),
                hr])
other = TableFields(["Construction", "Property",("Typ","Type")])

definition = [header,definitions,other,footer]

