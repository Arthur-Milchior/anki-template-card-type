from ..generators import *
from .general import header, footer
from .definition.definition import definitions

properties = TableFields(
    [
        "Domain",
        "Codomain",
        "Idempotent",
        "Metric",
        "Linearity",
        "Associative",
        "Commutative",
    ],
    name = "Properties"
)

binaryfunction = [header, definitions, properties, footer]
