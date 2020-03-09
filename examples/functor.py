from ..generators import *
from .general import footer, header

definition_bar = TableFields(
    name="Definition",
    fields=["Object",
            "Arrow",
            "Domain",
            "Codomain"]
)
properties = TableFields([["Left adjoint to",
                           "Right adjoint to"],
                          ["Create limits",
                           "Preserve limits"],
                          ["Preserve product",
                           "Preserve coproduct"],
                          ["Full",
                           "Faithfull"],
                          "Projective"])

functor = [header, definition_bar, properties, footer]
