from ..generators.imports import *
from .general import header, footer, typDic
name_ = [{"field":"Instruction",
          "classes":"Notation"},
         "Variable",
         {"field":"Shortcut",
          "classes":["Abbreviation","Shortcut"]},
         "Abbreviation",
         "Library",
         {"field":"Program",
          "classes":"Library"},
         "Where to use it"]
name = TableFields(name_,
                   isMandatory=False,
                   name="CS name",
                   suffix = hr)
complexity_ = ["Time complexity",
               "Space complexity",
               "AC complexity",
               "NC complexity",
               "Logical complexity"
               "Other complexity",
               "Potential or credit"]
complexity=TableFields(complexity_,
                       isMandatory=False,
                       name="Complexity",
                       suffix = hr)

values=PotentiallyNumberedFields("Value",
                                 7,
                                 suffix = hr)

problem_ = ["Input",
            "Returns",
            "Effect",
            "Meaning",
            typDic,
            "Subtype of",
            "Default",
            "Initialization",
            "Invariant",
            "Abstract data structure"]
problem = TableFields(problem_,
                      isMandatory=False,
                      name="Description",
                      suffix = hr
)

implementation= PotentiallyNumberedFields("Implementation",4,suffix=hr)
exceptions = PotentiallyNumberedFields("Exception",5,suffix=hr)
all_=TableFields(name_+
                 problem_+
                 complexity_,
                 isMandatory = False,
                 suffix = hr)
tout=[header,
      name,
      problem,
      values,
      implementation,
      complexity,
      exceptions,
      footer]
      

# CS_header= header+[problem,DecoratedField("Abstract data structures")]
# CS_footer=[implementation,complexity]+footer
algorithm = tout
noteType= tout
variable=tout
commandLine=tout
instruction=tout
dataStructure=tout
problem=tout
