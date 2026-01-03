from ..generators import *
from .general.typ import typDic
from .general.examples import examples
from .general.namesNotationsDenotedBy import namesNotationsDenotedBy
from .util import addBoilerplate, empty1
from aqt.qt import debug;

typDicLanguage = {"field": "Typ",
                  "label": "Type:",
                  "filledFields": ["Typ"],
                  "questions": {"Typ"},
                  "function": lambda i: code("Language")({f"Typ"}),
}

    
def codeLanguageFixed(language, field_name):
    assert language
    def aux(index, **kwargs):
        return PRE(
            child=CODE(
                child={field_name},
                attrs={"class": language},
                **kwargs
            )
        )
    return aux

cs_context_ = [
    {"field": "Code context",
     "classes": "context",
     "function": lambda i: code("Language")({"Code context"})
    },
    {"field": "Invariant context",
     "classes": "context"},
    {"field": "Library",
     "classes": "context"},
    {"field": "Program",
     "classes": "context"},
    {"field": "Where to use it",
     "classes": "context"},
    {"field": "Prefix",
     "classes": "context",
     "function": codeLanguageFixed("sh", "Prefix"),
    }
]
cs_context = TableFields(cs_context_,
                         isMandatory=False,
                         name="CS context",
                         suffix=hr)
name_ = [
    {"field": "Instruction",
     "classes": "Notation",
     "function": lambda i: code("Language")({numbered_field("Instruction", i)}),
    },
    {"field": "Syntactic sugar",
     "classes": "Notation",
     "function": lambda i: code("Language")({"Syntactic sugar"}),
    },
    {"field": "Variable",
     "classes": "Notation",
     "function": lambda i: code("Language")({f"Variable"}),
    },
    {"field": "Constant",
     "classes": "Notation",
     "function": lambda i: code("Language")({f"Constant"}),
    },
    {"field": "Shortcut",
     "classes": ["Abbreviation", "Shortcut"]},
    {"field": "Abbreviation",
     "classes": ["Abbreviation", "Shortcut"],
     "function": lambda i: code("Language")({f"Abbreviation"}),
     },
]
name = TableFields(name_,
                   isMandatory=False,
                   name="CS name",
                   suffix=hr)
complexity_ = ["Time complexity",
               "Space complexity",
               "AC complexity",
               "NC complexity",
               "Logical complexity"
               "Other complexity",
               "Potential or credit"]
complexity = TableFields(complexity_,
                         isMandatory=False,
                         name="Complexity",
                         suffix=hr)

values = PotentiallyNumberedFields("Value",
                                   21,
                                   suffix=hr, emphasizingField=code("Language"))

problem_ = ["Input",
            {"field": "Identifier",
             "classes": "Notation",
             "function": lambda i: code("Language")({f"Identifier"}),
            },
            "Returns",
            "Print",
            "Effect",
            {"field": "Similar to",
             "classes": "Notation",
             "function": lambda i: code("Language")({f"Similar to"}),
            },
            "Meaning",
            "TypMeaning",
            "Construction",
            "Mutable",
            "Storage",
            "Scope",
            typDicLanguage,
            "Subtype of",
            "Default",
            "Initialization",
            "Syntactical constraint",
            "Invariant",
            "Abstract data structure"]
problem = TableFields(problem_,
                      isMandatory=False,
                      name="Description",
                      suffix=hr,
                 header_decoration=H2,
                      )
def impl_code(field: str):
    return {
        "field": field,
        "child": code("Language")({field})
        }

# implementation = PotentiallyNumberedFields(
#     "Implementation", 4,
#     suffix=hr,
#     localFunMultiple=impl_code,
#     singleCase=DecoratedField(
#         "Implementation",
#         child=
#         QuestionnedField(
#             "Implementation",
#             child=code("Language")(P({"Implementation"})))))

def languageComment(*args, **kwargs):
    return [Comment("Language: "), code("Language")(*args, **kwargs)]

def implementation():
    return PotentiallyNumberedFields(
    "Implementation", 
    4, 
    emphasizingField=languageComment
    #infix=[br, Comment("azerty")]
    )

flag_ = (
    "Flag abbreviation",
    UL([
        CODE(QuestionnedField("Fla"), attrs={"class":"sh"}),
        CODE(QuestionnedField("Flag abbreviation"), attrs={"class":"sh"}),
    ]),
    P(CODE(QuestionnedField("Fla"), attrs={"class":"sh"})),
)

exceptions = PotentiallyNumberedFields("Exception", 5, suffix=hr)
all_ = TableFields(cs_context_ +
                   name_ +
                   problem_ +
                   complexity_,
                   isMandatory=False,
                   suffix=hr)
tout = addBoilerplate([
    CSS("_github.css"),
    SCRIPT("_highlight.pack.js"),
    SCRIPT("_highlight_automatic.js"),
    namesNotationsDenotedBy,
    cs_context,
    flag_,
    name,
    problem,
    values,
    implementation(),
    complexity,
    exceptions,
    examples()])


# CS_header= header+[problem,DecoratedField("Abstract data structures")]
# CS_footer=[implementation,complexity]+footer
algorithm = tout
noteType = tout
variable = tout
commandLine = tout
instruction = tout
dataStructure = tout
problem = tout
enum = tout #todo improve
constant = tout
