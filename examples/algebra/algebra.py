from ...generators import *
from ..general.namesNotationsDenotedBy import *
from ..general.typ import typDic
from .name import algebra_name_formatted
from ..util import *
from ..style import *

v1 = bareFieldOrDefault("value (mathjax)", "a")
pv1 = parenthese(v1)
v2 = bareFieldOrDefault("value2 (mathjax)", "b")
pv2 = parenthese(v2)
base = bareFieldOrDefault("base element (mathjax)", "r")


inner_function = TableFields(
    [
        {"field": "Ring-base",
         "label": "Base",
         "classes": "Definition6"},
        {"field": "Field-base",
         "label": "Base",
         "classes": "Definition6"},
        {"field": "+",
         "classes": "Definition",
         "label": mathjax_equal(pv1, " + ", pv2)
        },
        {"field":    "0",
         "classes": "Definition2"},
        {"field":    "-",
         "classes": "Definition3",
         "label": mathjax_equal("-", pv1),
        },
        {"field":    "*",
         "classes": "Definition4",
         "label": mathjax_equal(pv1, " * ", pv2),
        },
        {"field":    "1",
         "classes": "Definition5"},
        {"field":    "÷",
         "classes": "Definition6",
         "label": mathjax_equal("1 / ", pv1),
         },
        {"field":    "\\",
         "classes": "Definition",
         "label": mathjax_equal(pv1, " \\ ", pv2),
         },
        {"field":    "×",
         "classes": "Definition7",
         "label":   mathjax_equal(base," \\times ", pv1),
         },
        {"field":    "⋀",
         "classes": "Definition8",
         "label":   mathjax_equal(pv1, " \\wedge ", pv2),
         },
        {"field":    "⋁",
         "classes": "Definition9",
         "label": mathjax_equal(pv1, " \\vee ", pv2)
            },
        {"field":    "→",
         "classes": "Definition",
         "label": mathjax_equal(pv1, " \\to ", pv2,)
         },
        {"field":    "¬",
         "classes": "Definition4",
         "label": mathjax_equal("¬", pv1),
         },
        {"field":    "◁",
         "classes": "Definition5",
         "label": mathjax_equal(pv1, " \\triangleleft ", pv2,),
        },
    ],
    emphasizing=decorateQuestion,
    name="Inner functions",
    suffix=hr
)

presentation = ("Relation",
                PotentiallyNumberedFields(label=Cascade("Relations",
                                                        QuestionnedField(
                                                            "Generating family"),
                                                        {"Generating family"}),
                                          greater=5,
                                          numbered_field=numbered_field,
                                          fieldPrefix="Relation",
                                          suffix=hr))
outer_function = TableFields(
    ["Graduation",
     {"field":"Norm",
      "label": mathjax_equal("\\left|", pv1, "\\right|",)},
     "Euclidean function",
     "Quadratic form",
     ],
    name="Outer functions"
)
definition = Cascade("Definitions",
                     [DecoratedField("Set", suffix=hr),
                      presentation,
                      inner_function,
                      outer_function],
                     {"Inner functions", "Outer functions", "Relations", "Set"})

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
     "Dimension",
     typDic,
     "Free family",
     "Generating family",
     "Inner product",
     "Cover",
     "Faithful",
     "Minimals",
     "Maximals",
     "Well-founded",
     "Units",
     "Zero divisors",
     ],
    name="Properties"
)

algebra = addBoilerplate([
    namesNotationsDenotedBy,
    algebra_name_formatted,
    definition,
    properties,
])
