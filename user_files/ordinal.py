from general import header, footer

definition_foo = TableFields(
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

ordinal = [header, definition_foo, properties, footer]
