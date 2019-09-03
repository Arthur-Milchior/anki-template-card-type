from ..generators import *
from .general import footer, header

extends = PotentiallyNumberedFields(fieldPrefix = "Extends",
                                    classes = "Definition2",
                                    greater = 2)

axioms = PotentiallyNumberedFields(fieldPrefix = "Axiom",
                                    classes = "Definition3",
                                   greater = 10)

properties = TableFields(["Complete",
                          "Categorical",
                          "Closed"])

models = PotentiallyNumberedFields(fieldPrefix = "Model",
                                   greater = 4)


definition_theory = Cascade("Definition",
                            [DecoratedField("Vocabulary",
                                            classes = "Definition3",
                                            suffix=hr),
                             extends,
                             axioms],
                             cascade = {"Vocabulary","Extendss","Axioms"})

theory = [header, definition_theory, models, properties, footer]
