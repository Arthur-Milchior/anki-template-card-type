from ..generators import *
from .general import footer, header

definition = TableFields(
    fields=[
        "Definition",
        "Definition2",
        "Definition3",
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
    "Cardinal",
    ["Stable on left",
     "Stable on right"]
])

binaryrelation = [header, definition, properties, footer]
