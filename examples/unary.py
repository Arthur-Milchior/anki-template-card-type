from ..generators import *
from .general import header, footer

definition = TableFields(
    fields = [
        "Definition",
        "Definition2",
        "Taylor series",
        "Domain",
        "Codomain",
        "Radius",
    ],
    name="Definitions"
)
properties = TableFields([
    "Parity",
    "Degree",
    "Continuous",
    "Measurable",
    "Linear",
    "Involutary",
    "Idempotent",
    "Monotonic",
    "Measure",
    "Norm",
    "Morphism",
    ["Derivative",
    "Nth derivative",
     "Integral"],
    "Jective",
    ["Left inverse",
     "Right inverse",
     "Inverse"],

])

unary = [header, definition, properties, footer]
