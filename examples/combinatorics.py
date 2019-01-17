from .general import short_header, footer
from ..generators.imports import *

definition_combinatorics = TableFields(
    name = "Combinatorics",
    fields = []
)
numeric = TableFields(["Nth value",
                       {"field":"Sequence name",
                        "clasess":["Name"]},
                       {"field":"Sequence french",
                        "clasess":["French"]},
                       {"field":"Sequence notation",
                        "clasess":["Notation"]},
                       {"field":"Sequence abbreviation",
                        "clasess":["Abbreviation"]},
                       "Asymptotically",
                       {"field":"OGF",
                        "clasess":["Definition"]},
                       {"field":"EGF",
                        "clasess":["Definition2"]},
                       "Asymptotically"
],
                      name="Numeric"
)
bijection = DecoratedField("Bijection")
symbolic = TableFields(["Name",
                        "French"
                        "Notation",
                        "Abbreviation"
                        {"field":"Equation",
                         "classes":"Definition"},
                        {"field":"Nth element",
                         "classes":"Nth"}],
                       greater=2,
                       name="Symbolic")

combinatorics = [short_header, numberic, bijection, symbolic, footer]
