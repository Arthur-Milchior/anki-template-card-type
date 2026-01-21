from ...generators import *
from ..definition.definition import definitions
from ..general.footer import footer
from ..general.header import header
from ..util import *
from ..style import *

fullname =  [{"Name"}, Filled("Receuil", [", ", {"Receuil"}])]
header = [header, fullname, " ", {
    "Composer"}, br, {"Speed"}, ", ", {"Rythm"}]
music = [Asked("Subpart", {"Music"}),  Asked("Part", {"Music"})]


def grouping(subgroup, nb=0, size=4, part="Part", prefix="Subpart"):
    """If none of prefix{i} for i in the nb-th segment of size size is
    asked, and if part{nb+1} is present, then show part{nb+1}. Else show
    subgroup

    """
    partName = f"{part}{nb+1}" if nb else part
    definitions = [numbered_field(prefix, i) for i in range(
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
    part = Cascade(partName, part, set(definitions))
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
                                        numbered_field=numbered_field,
                                        label=labelDef,
                                        infix="",
                                        applyToGroup=grouping,
                                        groupSize=4)
learn_sheet = addBoilerplate([header, music, definitions, hr], "Learn")

title = H1(Filled("Name", [{"Name"}, Filled( "Receuil", [",", {"Receuil"}]), Filled( "Composer", [",", {"Composer"}])]))

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
            l = {numbered_field("Part", parts[0])}
        else:
            s = "Play parts " + ", ".join(parts[:-1]) + " and " + parts[-1]
            l = [[{numbered_field("Part", i)}, br] for i in parts]
    content = [ H2(s + " "+precision), title, l]
    return addBoilerplate(content, asked=[numbered_field("Part", i) for i in parts])

def subpractices(subpart: int):
    """Coentent to practice subpart and the last present subpart. Assuming this is at most 4 before before subpart."""
    all_content = emptyGen
    current_subpart_field = numbered_field("Subpart", subpart)
    for i in range(4):
        first_subpart = subpart -4 + i
        first_subpart_field = numbered_field("Subpart", first_subpart)
        this_content=  [H2(f"Practice part {first_subpart} to {subpart}"), title, br, {first_subpart_field}, {current_subpart_field}]
        all_content = FilledOrEmpty(first_subpart_field, this_content, all_content)
    return addBoilerplate(Filled(current_subpart_field, all_content))

def subpractice(subpart: int):
    header_text = f"Play subpart {subpart}"
    sp = numbered_field("Subpart", subpart)
    return addBoilerplate(Filled("Practice subpart", Filled(sp, [H2(header_text), title, {sp}, hr, footer()])))
