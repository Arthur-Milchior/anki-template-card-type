from ..generators import *
from .general.head import header
from .general.foot import footer
from .general.typ import typDic

cs_context_ = [
    {"field":"Library",
     "classes":"context"},
    {"field":"Program",
     "classes":"context"},
    {"field": "Where to use it",
     "classes":"context"}]
cs_context = TableFields(cs_context_,
                         isMandatory = False,
                         name = "CS context",
                         suffix = hr)
name_ = [
    {"field":"Instruction",
     "classes":"Notation"},
    {"field":"Variable",
     "classes":"Notation"},
    {"field":"Shortcut",
     "classes":["Abbreviation","Shortcut"]},
    "Abbreviation",
    ]
name = TableFields(name_,
                   isMandatory=False,
                   name="CS name",
                   suffix = hr)
complexity_ = ["Time complexity",
               "Space complexity",
               "AC complexity",
               "NC complexity",
               "Logical complexity",
               "Other complexity",
               "Potential or credit"]
complexity=TableFields(complexity_,
                       isMandatory=True,
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
all_=TableFields(cs_context_+
                 name_+
                 problem_+
                 complexity_,
                 isMandatory = False,
                 suffix = hr)
tout=[header,
      cs_context,
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
