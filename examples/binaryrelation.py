from ..generators import *
from .general import header, footer

definition = TableFields(
    fields = [
        "Definition",
        "Definition2",
        "Set"
    ],
    name="Definitions"
)
properties = TableFields([
    "Symmetry",
    "Transitive",
    "Reflexive",
    "Equivalence",
    "Order",
    ["Stable on left",
     "Stable on right"]
])

binaryrelation = [header, definition, properties, footer]
