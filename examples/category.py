from ..generators.imports import *
from .general import header, footer

definition_ordinal = TableFields(
    name = "Definition",
    fields = ["Objects", "Arrows", "Compositions"]
)
def relatedFields(fields):
    assert assertType(relatedFields, list)
    return [{"field" : field,
               "hideInSomeQuestion": s - {field}} for field in fields]
properties = TableFields(
    [
        ["Arrow from initial", "Arrow to initial", "Arrow from terminal", "Arrow to terminal"],
        ["Mono", "Epi", "Iso", "Bimorphism","Split epi",
        "Split mono"],
        ["Initial", "Terminal", "Zero object"],
        ["Biproduct","Product", "Coproduct"],
        ["Pullback","Pushout"],
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
])

category = [header, definition_ordinal, properties, footer]
