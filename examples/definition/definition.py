from ...generators import *
from ..general.footer import footer
from ..general.header import header
from ..general.namesNotationsDenotedBy import namesNotationsDenotedBy
from ..general.names import names
from ..general.notations import notations
from ..general.typ import typDic
from ..util import *
from ..style import *

labelDef = [Filled("DefType",
                   [QuestionnedField("DefType",
                                     isMandatory=True),
                    Empty("Conjdef", " such that ")]),
            FilledOrEmpty("Conjdef",
                          QuestionnedField("Conjdef", ["Conjdef"]),
                          Filled("Definition2",
                                 FilledOrEmpty("Typ",
                                               "equivalently",
                                               "Equivalently")))
            ]
labelDef = Cascade("Definitions",
                   Cascade("Conjdef",
                           labelDef,
                           {"DefType"}),
                   {"Conjdef"})


def grouping(subgroup, nb=0, size=4, part="Part", prefix="Definition"):
    """If none of prefix{i} for i in the nb-th segment of size size is
    asked, and if part{nb+1} is present, then show part{nb+1}. Else show
    subgroup

    """
    partName = f"{part}{nb+1}" if nb else part
    definitions = [prefix if i == 1 else f"{prefix}{i}" for i in range(
        size*nb+1, size*(nb+1)+1)]
    part = LI({partName})
    part = FilledOrEmpty(
        partName,
        part,
        subgroup
    )
    for defName in definitions:
        part = AskedOrNot(defName,
                          subgroup,
                          part)
    return part


_definitions = ("Definition",
               [PotentiallyNumberedFields(fieldPrefix="Definition",
                                          greater=16,
                                          label=labelDef,
                                          infix="",
                                          applyToGroup=grouping,
                                          groupSize=4),
                hr])

# definitions = grouping(definitions, size=16, part="All")
# definitions = grouping(definitions, size=4, part="All", prefix="Part")
# definitions = grouping(definitions, size=1, part="All", prefix="Definitions")

# Ensure that if Parti is asked, then Definition4i+1, 4i+2, 4i+3 and 4i+4 is asked
for i in range(1, 5):
    name = "Part"+("" if i == 1 else str(i))
    content = set()
    for j in range(4):
        d = 4*(i-1)+j
        content.add("Definition"+("" if d == 1 else str(d)))
    _definitions = Cascade(name,
                          _definitions,
                          content)



other = TableFields([{"field": "Construction",
                      "showIfAskedOrAnswer": True},
                     {"field": "Property",
                      "showIfAskedOrAnswer": True},
                     {"field": "Cardinal",
                      "showIfAskedOrAnswer": True},
                     typDic])

definitions = addBoilerplate([
    namesNotationsDenotedBy,
    hr,
    _definitions,
    other,
])
definitions_names_end = addBoilerplate([
    _definitions,
    other,
    hr,
    namesNotationsDenotedBy,
])
