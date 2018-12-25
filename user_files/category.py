from general import header, footer

definition_ordinal = TableFields(
    listName = "ordinal",
    fields = ["Objects", "Arrows", "Composition"]
)
properties = TableFields(["Abelian",
              "Additive",
              "Bimorphism",
              "Biproduct",
              "Ccc",
              "Classifier",
              "Cocomplete",
              "Coconstant",
              "Coequalizer",
              "Cokernel",
              "Complete",
              "Connected",
              "Conormal",
              "Constant",
              "Coproduct",
              "Epi",
              "Equalizer",
              "Exponential",
              "Extremal epi",
              "Free",
              "Generator",
              "Groups",
              "Identity morphism",
              "Initial",
              "Arrow from initial",
              "Arrow to initial",
              "Injective object",
              "Iso",
              "Kernel",
              "Mono",
              "Monoid",
              "Monoidal operations",
              "Normal",
              "Opposite",
              "Power",
              "Preadditive",
              "Product",
              "Projective",
              "Pullback",
              "Pushout",
              "Regular",
              "Regular epi",
              "Split epi",
              "Split mono",
              "Subcategory",
              "Subobjects",
              "Symmetric monoidal category",
              "Terminal",
              "Arrow to terminal",
              "Arrow from terminal",
              "Topos",
              "Zero morphism",
              "Has zero morphisms",
              "Zero object",
])

category = [header, definition_ordinal, properties, footer]