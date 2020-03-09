from ..generators import *
from .general import footer, header

definition_ordinal = TableFields(
    name="Definition",
    fields=[
        {"field": "Objects",
         "classes": "Definition"},
        {"field": "Arrows",
         "classes": "Definition2"},
        {"field": "Compositions",
         "classes": "Definition3",
         "emptyCase": AskedOrNot("Composition",
                                 markOfQuestion,
                                 "Standard composition")},
    ]
)


def relatedFields(fields):
    assert assertType(relatedFields, list)
    return [{"field": field,
             "hideInSomeQuestion": s - {field}} for field in fields]


properties_ = TableFields(
    [
        ["Arrow from initial", "Arrow to initial",
            "Arrow from terminal", "Arrow to terminal"],
        ["Mono", "Epi", "Iso", "Bimorphism", "Split epi",
         "Split mono"],
        ["Initial", "Terminal", "Zero object"],
        ["Biproduct", "Product", "Coproduct"],
        ["Pullback", "Pushout"],
        ["Coequalizer",
         "Equalizer"],
        ["Kernel",
         "Cokernel"],
        ["Conormal",
         "Normal"],
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
category = [header, definition_ordinal, properties, footer]
