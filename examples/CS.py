from ..generators.imports import *
from .general import header, footer
all_=TableFields(["Instruction",
     "Shortcut",
     "Library",
     "Program",
     "Where to us it",
    "Input",
     "Returns",
     "Effect",
     "Meaning",
     ("Typ","Type"),
     "Subtype of",
     "Default",
     "Initialization",
     "Invariant",
     "Abstract data structure",
     "Time complexity",
     "Space complexity",
     "AC complexity",
     "NC complexity",
     "Logical complexity"
     "Other complexity",
     "Potential or credit"],
                 suffix=hr)
name=TableFields(["Instruction",
                  "Shortcut",
                  "Library",
                  "Program",
                  "Where to us it"],
                 name="CS name")

complexity=TableFields(["Time complexity",
                        "Space complexity",
                        "AC complexity",
                        "NC complexity",
                        "Logical complexity"
                        "Other complexity",
                        "Potential or credit"],
                       name="Complexity")

values=PotentiallyNumberedFields("Value",7)

problem=TableFields(["Input",
                     "Returns",
                     "Effect",
                     "Meaning",
                     ("Typ","Type"),
                     "Subtype of",
                     "Default",
                     "Initialization",
                     "Invariant",
                     "Abstract data structure"],
                    name="Description"
)

implementation= PotentiallyNumberedFields("Implementation",4)
exceptions = PotentiallyNumberedFields("Exception",5)
tout=[header,
      all_,
      # problem,
      values,
      # implementation,
      # complexity,
      exceptions,
      footer]
      

# CS_header= header+[problem,DecoratedField("Abstract data structures")]
# CS_footer=[implementation,complexity]+footer
algorithm = tout
typ= tout
variable=tout
commandLine=tout
instruction=tout
dataStructure=tout
problem=tout
