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
                        "clasess":["Generating_function1"]},
                       {"field":"EGF",
                        "clasess":["Generating_function2"]},
                       "Asymptotically"
],
                      name="Numeric"
)
bijection = DecoratedField("Bijection")
symbolic = TableFields(["Name",
                        "French"
                        "Notation",
                        "Abbreviation"
                        "Equation",
                        "Nth element"],
                       greater=2,
                       name="Symbolic")

combinatorics = [short_header, numberic, bijection, symbolic, footer]
