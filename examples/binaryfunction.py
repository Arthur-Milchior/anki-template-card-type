from ..generators import *
from .definition.definition import _definitions
from .general.namesNotationsDenotedBy import namesNotationsDenotedBy
from .general import footer, header
from .util import *

properties = TableFields(
    [
        "Domain",
        "Codomain",
        "Idempotent",
        "Metric",
        "Linearity",
        "Associative",
        "Commutative",
        "Zero",
        "Unit",
    ],
    name="Properties"
)

binaryfunction = addBoilerplate([namesNotationsDenotedBy, _definitions, properties])
