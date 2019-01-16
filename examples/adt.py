from .general import header, footer, typDic
from ..generators.imports import *

definition_adt = TableFields(
    name = "Adt_",
    fields = [typDic,
              "Extends",
              "Invariant",
              "Initialization"
    ]
)

definition=Cascade("Adt",
                   [definition_adt, PotentiallyNumberedFields("Function",5)],
                   ["Adt","Functions"])
adt = [header, definition, footer]
