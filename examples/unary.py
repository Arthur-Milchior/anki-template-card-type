from ..generators import *
from .general import footer, header, namesNotationsDenotedBy
from .util import *

definition = TableFields(
    fields=[
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
    ["Zero",
     "Unit"],
    ["Derivative",
     "Nth derivative",
     "Integral"],
    "Jective",
    ["Left inverse",
     "Right inverse",
     "Inverse"],

])

unary = addBoilerplate([namesNotationsDenotedBy, definition, properties])
