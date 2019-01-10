from .general import header, footer
from ..generators.imports import *

labelDef=FilledOrEmpty("Conjdef",
                       Cascade("Definitions",QuestionnedField("Conjdef"),["Conjdef"]),
                       "Definition(s)")
definitions = PotentiallyNumberedFields(fieldPrefix="Definition",
                                        greater=16,
                                        label=labelDef
)
other = TableFields(["Construction", "Property", "Representation"])

definition = [header,definitions,other,footer]

