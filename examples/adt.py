from .general.head import header
from .general.foot import footer
from .general.typ import typDic
from ..generators import *

definition_adt = TableFields(
    name = "Adt_",
    fields = [typDic,
              {"field":"Extends",
               "classes":"Definition2"},
              {"field":"Invariant",
               "classes":"Definition3"},
              {"field":"Initialization",
               "classes":"Definition4"}
    ]
)

definition=Cascade("Adt",
                   [definition_adt, PotentiallyNumberedFields("Function",5, classes="Definition")],
                   {"Adt","Functions"})
adt = [header, definition, footer]
