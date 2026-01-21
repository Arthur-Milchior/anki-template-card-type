from ...generators import *
from ..general import footer, header, namesNotationsDenotedBy
from ..util import *


object1 = bareFieldOrDefault("Object1 (mathjax)",  "a")
object2 = bareFieldOrDefault("Object2 (mathjax)",  "b")
object3 = bareFieldOrDefault("Object3 (mathjax)", "c")
morphism1 = bareFieldOrDefault("Morphism1 (mathjax)", "f")
morphism2 = bareFieldOrDefault("Morphism2 (mathjax)", "g")
morphism3 = bareFieldOrDefault("Morphism3 (mathjax)", "h")


definition_ordinal = TableFields(
    name="Definition",
    fields=[
        {"field": "Definition",
         "classes": "Definition"},
        {"field": "Objects",
         "classes": "Definition"},
        {"field": "Arrows",
         "classes": "Definition2",
         "label":["Arrows \\(", 
                  object1,
                  " \\to ",
                  object2,
                  "\\) :",
                 ],
         },
        {"field": "2-morphism",
         "classes": "Definition4"},
        {"field": "n-morphism",
         "classes": "Definition5"},
        {"field": "Compositions",
         "classes": "Definition3",
         "label":["Arrows \\(", 
                  morphism1,
                  " \\circ ",
                  morphism2,
                  "\\) :",
                 ],
         "emptyCase": AskedOrNot("Composition",
                                 markOfQuestion,
                                 "Standard composition")},
    ]
)


def relatedFields(fields):
    assert assertType(relatedFields, list)
    return [{"field": field,
             "hideInSomeQuestions": fields - {field}} for field in fields]


properties_ = TableFields(
    [
        ["Arrow from initial", "Arrow to initial",
            "Arrow from terminal", "Arrow to terminal"],
        ["Mono", "Epi", "Iso", "Bimorphism", "Split epi",
         "Split mono"],
        ["Initial", "Terminal", "Zero object"],
        ["Biproduct", "Product", "Coproduct"],
        [
            {
                "field":"Pullback",
                "label":[
                    "Pullback of \\(", 
                    morphism1,
                    ": ",
                    object1,
                    " \\to ",
                    object3,
                    "\\) and \\(",
                    morphism2,
                    ": ",
                    object2,
                    " \\to ",
                    object3,
                    "\\)"
                 ],
            }, 
            {
                "field":"Pushout",
                "label":[
                    "Pushout of \\(", 
                    morphism1,
                    ": ",
                    object1,
                    " \\to ",
                    object2,
                    "\\) and \\(",
                    morphism2,
                    ": ",
                    object1,
                    " \\to ",
                    object3,
                    "\\)"
                 ],
            },
        ],
        [
            {
                "field":"Coequalizer",
                "label":[
                    "Coequalizer of \\(", 
                    morphism1,
                    ", ",
                    morphism2,
                    ": ",
                    object1,
                    " \\to ",
                    object2,
                    "\\)",
                 ],
            },
          {
                "field":"Equalizer",
                "label":[
                    "Equalizer of \\(", 
                    morphism1,
                    ", ",
                    morphism2,
                    ": ",
                    object1,
                    " \\to ",
                    object2,
                    "\\)",
                 ],
            }],
        ["Kernel",
         "Cokernel"],
        ["Conormal",
         "Normal"],
         ["Limit", "Colimit"],
        "Abelian",
        "Additive",
        "Ccc",
        "Classifier",
        "Cocomplete",
        "Coconstant",
        "Complete",
        "Connected",
        "Constant",
        "Exponential",
        "Extremal epi",
        "Free",
        "Generator",
        "Group",
        "Identity morphism",
        "Injective object",
        "Monoid",
        "Monoidal operations",
        "Opposite",
        "Power",
        "Preadditive",
        "Projective",
        "Regular",
        "Regular epi",
        "Subcategory",
        "Subobjects",
        "Symmetric monoidal category",
        "Topos",
        "Zero morphism",
        "Has zero morphisms",
    ],
    defaultClasses="Property")

properties = HideInSomeQuestions(
    ["Arrows", "Objects", "Compositions", "Definition"], properties_,)
category = addBoilerplate([namesNotationsDenotedBy, hr, definition_ordinal, hr, properties])
