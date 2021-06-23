from ..generators import *
from .general.typ import typDic
from .general.examples import examples
from .general.namesNotationsDenotedBy import namesNotationsDenotedBy
from .util import addBoilerplate, empty1

typDicLanguage = {"field": "Typ",
                  "label": "Type",
                  "filledFields": ["Typ"],
                  "questions": {"Typ"},
                  "function": lambda i: code("Language")({f"Typ"}),
}

def code(languageField):
    """A function which add tag ensuring that the child is interpreted as code in language `language` or given in the field
    `languageField`."""
    def aux(child, **kwargs):
        return FilledOrEmpty(languageField,
                      PRE(
                          child=CODE(
                              child=child,
                              attrs={"class": "{{" + languageField + "}}"},
                              **kwargs
                          ),
                          **kwargs
                      ),
                      child)
    return aux
    
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
     "function": lambda i: code("Language")({f"Instruction{empty1(i)}"}),
    },
    {"field": "Long flag",
     "classes": "Notation",
     "function": codeLanguageFixed("sh", "Long flag"),
    },
    {"field": "Variable",
     "classes": "Notation",
     "function": lambda i: code("Language")({f"Variable"}),
    },
    {"field": "Shortcut",
     "classes": ["Abbreviation", "Shortcut"]},
    {"field": "Abbreviation",
     "classes": ["Abbreviation", "Shortcut"]},
    {"field": "Short flag",
     "classes": ["Abbreviation", "Shortcut"],
     "function": codeLanguageFixed("sh", "Short flag"),
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
                                   7,
                                   suffix=hr)

problem_ = ["Input",
            "Returns",
            "Print",
            "Effect",
            "Meaning",
            typDicLanguage,
            "Subtype of",
            "Default",
            "Initialization",
            "Invariant",
            "Abstract data structure"]
problem = TableFields(problem_,
                      isMandatory=False,
                      name="Description",
                      suffix=hr
                      )
def impl_code(field: str):
    return {
        "field": field,
        "child": code("Language")({field})
        }

implementation = PotentiallyNumberedFields(
    "Implementation", 4,
    suffix=hr,
    localFunMultiple=impl_code,
    singleCase=DecoratedField(
        "Implementation",
        child=
        QuestionnedField(
            "Implementation",
            child=code("Language")(P({"Implementation"})))))

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
    name,
    problem,
    values,
    implementation,
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
