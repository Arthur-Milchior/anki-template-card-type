from ..generators import *
from .general.footer import footer
from .general.header import header
from .general.typ import typDic
from .general.namesNotationsDenotedBy import namesNotationsDenotedBy
from .util import *
from .style import *

definition_adt = TableFields(
    name="Adt_",
    fields=[typDic,
            {"field": "Extends",
             "classes": "Definition2"},
            {"field": "Invariant",
             "classes": "Definition3"},
            {"field": "Initialization",
             "classes": "Definition4"}
            ], 
            numbered_field=numbered_field,
    emphasizing=decorateQuestion
)

definition = Cascade("Adt",
                     [definition_adt,   
                      PotentiallyNumberedFields(
                          "Function", 5, classes="Definition", numbered_field=numbered_field),
                      PotentiallyNumberedFields(
                          "Axiom", 4, classes="Definition3", numbered_field=numbered_field),
                      PotentiallyNumberedFields(
                          "Meaning", 4, classes="Definition5", numbered_field=numbered_field),
                      ],
                     {"Adt_", "Functions"})
adt = addBoilerplate([namesNotationsDenotedBy, hr, definition])
