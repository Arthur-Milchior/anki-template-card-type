from ..generators import *
from .definition.definition import definitions
from .general import footer, header

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
    name="Properties"
)

binaryfunction = [header, definitions, properties, footer]
