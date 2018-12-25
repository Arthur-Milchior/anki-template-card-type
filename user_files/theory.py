from general import header, footer

extends = PotentiallyNumberedFields(fieldPrefix = "Extends", greater = 2)
axioms = PotentiallyNumberedFields(fieldPrefix = "Axiom", greater = 10)
properties = TableFields(["Complete",
                          "Categorical",
                          "Closed"])
models = PotentiallyNumberedFields(fieldPrefix = "model", greater = 4)


definition_theory = NamedList("Definition",
                               [DecoratedField("Vocabulary"),
                                extends,
                                axioms],
                               "Definition ???"
)
theory = [header, definition_theory, models, properties, footer]
