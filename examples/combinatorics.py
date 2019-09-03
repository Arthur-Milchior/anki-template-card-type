from ..generators import *
from .general import footer, header

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
symbolics = TableFields(["Name",
                         "French",
                         "Notation",
                         "Abbreviation",
                         {"field":"Equation",
                          "classes":"Definition"},
                         {"field":"Nth element",
                          "classes":"Nth"}],
                        greater=2,
                        name="Symbolic")
symbolic = TableFields(["Name",
                        "French",
                        "Notation",
                        "Abbreviation",
                        {"field":"Equation",
                         "classes":"Definition"},
                        {"field":"Nth element",
                         "classes":"Nth"}],
                       name="Symbolic")
symbolic2 = TableFields(["Name2",
                         "French2",
                        "Notation2",
                         "Abbreviation2",
                        {"field":"Equation2",
                         "classes":"Definition"},
                        {"field":"Nth element2",
                         "classes":"Nth"}],
                       name="Symbolic")

combinatorics = [header, numeric, bijection, symbolics, footer]
combinatoric_numeric = [header, numeric, footer]
combinatoric_symbolic = [header, symbolic, footer]
combinatoric_symbolic2 = [header, symbolic2, footer]
