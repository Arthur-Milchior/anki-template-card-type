from ..generators.imports import *
from .general import header, footer


extends = PotentiallyNumberedFields(fieldPrefix = "Extends", greater = 2)
axioms = PotentiallyNumberedFields(fieldPrefix = "Axiom", greater = 10)
properties = TableFields(["Complete",
                          "Categorical",
                          "Closed"])
models = PotentiallyNumberedFields(fieldPrefix = "Model", greater = 4)


definition_theory = Cascade("Definition",
                            [DecoratedField("Vocabulary"),
                             extends,
                             axioms],
                             cascade = ["Vocabulary","Extendss","Axioms"])
theory = [header, definition_theory, models, properties, footer]
