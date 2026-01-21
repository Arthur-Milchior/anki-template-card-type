from .category import bareField
from ...generators import *
from ..general import footer, header, namesNotationsDenotedBy
from ..util import *

source_object1 = bareFieldOrDefault("Source object (mathjax)", "a")
source_object2 = bareFieldOrDefault("Source object2 (mathjax)", "b")
target_object1 = bareFieldOrDefault("Target object (mathjax)", "F(a)")
target_object2 = bareFieldOrDefault("Target object2 (mathjax)", "F(b)")
morphism1 = bareFieldOrDefault("Source arrow (mathjax)", "f")
domain = bareFieldOrDefault("Domain (mathjax)", "\mathcal A")
codomain = bareFieldOrDefault("Codomain (mathjax)", "\mathcal A'")

images = [
        {
            "field":"Object",
            "label":[
                "Sends \\(",
                source_object1,
                "\\) to "
                ],
                "hideInSomeQuestion": {
                    "Domain", "Codomain", "Arrow",
                },
         },
        {
            "field":"Arrow",
            "label":[
                "Sends \\(",
                morphism1,
                "\in ", domain, "(", source_object1, ", ", source_object2,
                ")\\) to \\(",
                codomain, "(", target_object1, ", ", target_object2,
                ")\\)'s ",],
                "hideInSomeQuestion": {
                    "Domain", "Codomain"
                },
         },]

definition_bar = TableFields(
    name="Definition",
    fields=[
        "Domain",
        "Codomain",
        *images
         ]
)
functor_base = addBoilerplate(
    [H5("Functor"), hr,
     namesNotationsDenotedBy,
     definition_bar])

properties = TableFields([*images,
                          ["Left adjoint to",
                           "Right adjoint to"],
                          ["Create limits",
                           "Preserve limits"],
                          ["Preserve product",
                           "Preserve coproduct"],
                          ["Full",
                           "Faithfull"],
                           "Representable",
                          "Projective"])

functor = addBoilerplate(
    [H5(["Functor in \\([", domain, ", ", codomain, "]\\)"]), hr,
     namesNotationsDenotedBy,
     properties])
