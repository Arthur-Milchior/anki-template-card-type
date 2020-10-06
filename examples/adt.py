from ..generators import *
from .general.footer import footer
from .general.header import header
from .general.typ import typDic

definition_adt = TableFields(
    name="Adt_",
    fields=[typDic,
            {"field": "Extends",
             "classes": "Definition2"},
            {"field": "Invariant",
             "classes": "Definition3"},
            {"field": "Initialization",
             "classes": "Definition4"}
            ]
)

definition = Cascade("Adt",
                     [definition_adt,
                      PotentiallyNumberedFields(
                          "Function", 5, classes="Definition"),
                      PotentiallyNumberedFields(
                          "Axiom", 4, classes="Definition3"),
                      ],
                     {"Adt_", "Functions"})
adt = [header, definition, footer]
