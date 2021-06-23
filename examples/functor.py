from ..generators import *
from .general import footer, header, namesNotationsDenotedBy
from .util import *

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

functor = addBoilerplate(
    [H5("Functor"), hr,
     namesNotationsDenotedBy,
     definition_bar,
     properties])
