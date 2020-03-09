from ..generators import *
from .general import footer, header

definition_ordinal = TableFields(
    fields=["Definition",
            {"field": "Axiom",
             "classes": "Definition2"}
            ]
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
