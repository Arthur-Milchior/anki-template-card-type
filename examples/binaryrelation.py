from ..generators import *
from .general import footer, header, namesNotationsDenotedBy
from .util import addBoilerplate
from .general.examples import examples
from .general.counterexamples import counterexamples

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
_binaryrelation = [namesNotationsDenotedBy, definition, properties, examples(), counterexamples]
binaryrelation = addBoilerplate(_binaryrelation)

