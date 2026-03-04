from ...generators import *
from ..general import footer, header, namesNotationsDenotedBy
from ..util import *

domain_field = "Domain (mathjax)"
codomain_field = "Codomain (mathjax)"

notation_mj = bareFieldOrDefault("Notation (mathjax)", "F")
source_object1_mj = bareFieldOrDefault("Source object (mathjax)", "a")
source_object2_mj = bareFieldOrDefault("Source object2 (mathjax)", "b")
target_object1_mj = bareFieldOrDefault("Target object (mathjax)", [notation_mj, parenthese(source_object1_mj)])
target_object2_mj = bareFieldOrDefault("Target object2 (mathjax)", [notation_mj, parenthese(source_object2_mj)])
morphism1_mj = bareFieldOrDefault("Source arrow (mathjax)", "f")
domain_mj = bareFieldOrDefault(domain_field, "\mathcal A")
codomain_mj = bareFieldOrDefault(codomain_field, "\mathcal A'")

images = [
        {
            "field":"Object",
            "label":[
                "Sends ", mathjax(
                source_object1_mj, "\\in ", domain_mj
                ), " to "
                ],
                "hideInSomeQuestions": {
                    "Domain (mathjax)", "Codomain (mathjax)", 
                    "Domain", "Codomain",
                },
         },
        {
            "field":"Arrow",
            "label":[
                "Sends ",mathjax(
                morphism1_mj,
                "\in ", domain_mj, "(", source_object1_mj, ", ", source_object2_mj,
                ")"), " to ", mathjax(
                codomain_mj, "(", target_object1_mj, ", ", target_object2_mj,
                ")"), "'s ",],
                "hideInSomeQuestions": {
                    "Domain (mathjax)", "Codomain (mathjax)",
                    "Domain", "Codomain", "Object",
                },
         },]

definition_bar = TableFields(
    name="Definition",
    fields=[
        {
            "field": domain_field,
            "label": "Domain",
            "function": lambda _: mathjax(bareField(domain_field))
        },
        {
            "field": codomain_field,
            "label": "Codomain",
            "function": lambda _: mathjax(bareField(codomain_field))
        },
        *images
         ]
)
functor_base = addBoilerplate(
    [H5("Functor"), hr,
     namesNotationsDenotedBy,
     definition_bar])

properties = TableFields([*images,
                          ["Its right adjoint",
                           "Its left adjoint"],
                          ["Create limits",
                           "Preserve limits",
                           "Create colimits",
                           "Preserve colimits"],
                           ["Preserve reflections",
                            "Preserve coreflections"],
                          ["Preserve products",
                           "Preserve coproducts"],
                          ["Full",
                           "Faithfull"],
                          {
                             "field": "Functor representation",
                             "label":"Representation"},
                          "Projective",
                          ["Elements", "Universal element"],
                          ])

functor = addBoilerplate(
    [H5(["Functor in ", mathjax("[", domain_mj, ", ", codomain_mj, "]")]), hr,
     namesNotationsDenotedBy,
     properties])