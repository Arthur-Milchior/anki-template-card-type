from .general import header, footer
from ..generators.imports import *

definition_adt = TableFields(
    name = "Adt_",
    fields = [("Typ","Type"),
              "Extends",
              "Invariant",
              "Initialization"
    ]
)

definition=Cascade("Adt",
                   [definition_adt, PotentiallyNumberedFields("Function",5)],
                   ["Adt","Functions"])
adt = [header, definition, footer]
