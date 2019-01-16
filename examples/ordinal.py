from ..generators.imports import *
from .general import header, footer


definition_ordinal = TableFields(
    fields = ["Definition", "Axiom"]
)
properties = TableFields(["Admissible",
                          "Cofinality",
                          "Epsilon",
                          "Parity",
                          "Countable",
                          "Limit/successor",
                          "Stationnary",
                          "Regular",
                          "Recursive",
                          "Large countable",
])

ordinal = [header, definition_ordinal, properties, footer]
