from ...generators import *
from ..general.head import header
from ..general.foot import footer
from ..general.typ import typDic
from .name import algebra_name_formatted


inner_function = TableFields(
    [
        {"field":"Ring-base",
         "label": "Base",
         "classes": "Definition6"},
        {"field":"Field-base",
         "label": "Base",
         "classes": "Definition6"},
        {"field":"+",
         "classes":"Definition"},
        {"field":    "0",
         "classes":"Definition2"},
        {"field":    "-",
         "classes":"Definition3"},
        {"field":    "*",
         "classes":"Definition4"},
        {"field":    "1",
         "classes":"Definition5"},
        {"field":    "/",
         "classes":"Definition6"},
        {"field":    "\\",
         "classes":"Definition"},
        {"field":    "×",
         "classes":"Definition7"},
        {"field":    "⋀",
         "classes":"Definition8"},
        {"field":    "⋁",
         "classes":"Definition9"},
        {"field":    "→",
         "classes":"Definition"},
        {"field":    "¬",
         "classes":"Definition4"},
        {"field":    "◁",
         "classes":"Definition5"},
    ],
    name = "Inner functions",
    suffix = hr
)

presentation = ("Relation",
                PotentiallyNumberedFields(label = Cascade("Relations",
                                                          QuestionnedField("Generating family"),
                                                          {"Generating family"}),
                                          greater = 5,
                                          fieldPrefix = "Relation",
                                          suffix = hr))
outer_function = TableFields(
    ["Graduation",
     "Norm",
     "Euclidean function",
     "Quadratic form",
    ],
    name = "Outer functions"
)
definition = Cascade("Definitions",
                     [DecoratedField("Set", suffix = hr),
                      presentation,
                      inner_function,
                      outer_function],
                     {"Inner functions", "Outer functions","Relations", "Set"})

properties = TableFields(
    ["Principal ideal",
     "Integral",
     "Unique factorization",
     "Closed",
     "Commutative",
     "Not associative",
     "Right-distributive",
     "Complete",
     "Idempotent",
     "Base",
     "Base2",
     "Base3",
     "Dimension",
     typDic,
     "Free family",
     "Generating family",
     "Inner product",
     "Cover",
     "Minimals",
     "Maximals",
     "Well-founded"
    ],
    name = "Properties"
)

algebra = [header,
           algebra_name_formatted,
           definition,
           properties,
           footer]
