from ..generators import *
from .definition.definition import definition
from .general.foot import footer
from .general.short_head import short_header

header = [short_header, {"Name"}, " ", {
    "Composer"}, br, {"Speed"}, ", ", {"Rythm"}]
music = [Asked("Subpart", {"Music"}),  Asked("Part", {"Music"})]


def grouping(subgroup, nb=0, size=4, part="Part", prefix="Subpart"):
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


labelDef = [Filled("DefType",
                   [QuestionnedField("DefType",
                                     isMandatory=True),
                    " such that "]),
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

definitions = PotentiallyNumberedFields(fieldPrefix="Subpart",
                                        greater=16,
                                        label=labelDef,
                                        infix="",
                                        applyToGroup=grouping,
                                        groupSize=4)
learn_sheet = Filled("Learn", [header, music, definitions, hr, footer])


def practice(*args):
    parts = [arg for arg in args if isinstance(arg, int)]
    other = [arg for arg in args if not isinstance(arg, int)]
    assert len(other) <= 1 and (not other or isinstance(other[0], str))
    precision = f" ({other[0]}) " if other else ""
    if not parts:
        s = "Play all"
        l = FilledOrEmpty(
            "All",
            {"All"},
            definitions)
    else:
        if len(parts) == 1:
            s = f"Play part {parts[0]}"
            l = {f"Part{parts[0] if parts[0]>1 else ''}"}
        else:
            s = "Play parts " + ", ".join(parts[:-1]) + " and " + parts[-1]
            l = [[{f"Part{i if i>1 else ''}"}, br] for i in parts]
    content = [header, H1(s + " "+precision), l, hr, footer]
    for part in parts:
        content = Filled(f"Part{part if part>1 else ''}", content)
    return content
