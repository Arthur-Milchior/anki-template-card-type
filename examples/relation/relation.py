from ...generators import *
from ..util import *
from ..general import *
from ..general.examples import examplesAskedParam
from ..general.counterexamples import counterexamplesAskedParam


def suspend(when):
    return Filled(when, [CLASS("Warning", "Suspend this card"), hr])


"""{{Smaller to greater}} if field else "implies" """
impliesOrMorePrecise = FilledOrEmpty("Smaller to greater",
                                     {"Smaller to greater"},
                                     "implies")

questionnedImpliesOrMorePrecise = QuestionnedField(field="Smaller to greater",
                                                   child=impliesOrMorePrecise,
                                                   classes="Definition")

increaseRelation = Parenthesis(left=" ",
                               right=" ",
                               child=questionnedImpliesOrMorePrecise)

"""{{Greater to smaller}} if field else {{Smaller to greater}} if field else "Implied by" """
impliedByOrMore = FilledOrEmpty("Smaller to greater",
                                {"Smaller to greater"},
                                "implied by")
impliedByOrLotMore = FilledOrEmpty("Greater to smaller",
                                   {"Greater to smaller"},
                                   impliedByOrMore)
questionnedImpliedByOrMorePrecise = QuestionnedField(field="Greater to smaller",
                                                     child=impliedByOrLotMore,
                                                     classes="Definition")
decreaseRelation = Parenthesis(left=" ",
                               right=" ",
                               child=questionnedImpliedByOrMorePrecise)


def connexion(nb, side, default="and"):
    """{{Connect sidenb}} if field, else (default = "And").
    {{field side(nb+1)}}"""
    return Filled(f"{side}{nb+1}",
                  [Parenthesis(left=" ", right=" ",
                               child=FilledOrEmpty(f"Connect {side}{nb}",
                                                   {f"Connect {side}{nb}"},
                                                   default)),
                   QuestionnedField(f"{side}{nb+1}", classes="Definition2")])


def bigSide(side):
    """side0 connect0 side1 connect1 side2 connect2 side3"""
    l = [{f"Prefix {side}0"},
         QuestionnedField(f"{side}0", classes="Side"),
         connexion(0, side),
         connexion(1, side),
         connexion(2, side, default=FilledOrEmpty(f"Connect {side}0",
                                                  {f"Connect {side}0"},
                                                  "and")),
         {f"Suffix {side}"}, ]
    foe = FilledOrEmpty(f"{side}0",
                        l,
                        CLASS("Error", f"Error, {side}0 is empty"))
    return Cascade(field=f"{side}s",
                   cascade={f"{side}{i}" for i in range(4)},
                   child=foe)


greater = bigSide("Greater")
smaller = bigSide("Smaller")
listOfSideFieldNames = ["Smallest",
                        "Smaller0",
                        "Intermediate",
                        "Greater0",
                        "Greatest",
                        "Equivalent",
                        "Equivalent2",
                        "Equivalent3",
                        "Smaller1",
                        "Greater1",
                        "Smaller2",
                        "Greater2",
                        "Smaller3",
                        "Greater4",
                        ]


def df(fieldName, suffix=None, prefix=None):
    return DecoratedField(label="", infix=None, field=fieldName, suffix=suffix, prefix=prefix, classes="Side", emphasizing=decorateQuestion)


listOfSideFields = [df("Smallest"),
                    smaller,
                    df("Intermediate"),
                    greater,
                    df("Greatest"),
                    df("Equivalent"),
                    df("Equivalent2"),
                    df("Equivalent3")]

def increasing_(emphasize):
    if emphasize:
        increase = QuestionOrAnswer(
            decorateQuestion(increaseRelation),
            increaseRelation
        )
    else:
        increase = increaseRelation
    return [df("Smallest", suffix=increase),
            smaller,
            increase,
            df("Intermediate", suffix=increase),
            greater,
            df("Greatest", prefix=increase),
            df("Equivalent", prefix=increase),
            df("Equivalent2", prefix=increase),
        df("Equivalent3", prefix=increase)]

decreaseRelationEmphasized = QuestionOrAnswer(
    decorateQuestion(decreaseRelation),
    decreaseRelation,
)

decreasing_ = [
    df("Equivalent3", suffix=decreaseRelationEmphasized),
    df("Equivalent2", suffix=decreaseRelationEmphasized),
    df("Equivalent", suffix=decreaseRelationEmphasized),
    df("Greatest", suffix=decreaseRelationEmphasized),
    greater,
    df("Intermediate", prefix=decreaseRelationEmphasized),
    decreaseRelationEmphasized,
    smaller,
    df("Smallest", prefix=decreaseRelationEmphasized),
]


def construction(show_increasing:bool, in_increasing:bool):
    """The construction from smaller to greater if show_increasing else from greater to smaller.
    If in_increasing, this is displayed in a card where the statement starts with smaller and ends with greater."""
    field_name = f"Construction{"" if show_increasing else " back"}"
    field_label = FilledOrEmpty("Construction back", "Construction ⇒" if show_increasing==in_increasing else "Construction ⇐", "Construction")
    return [hr,
         ShowIfAskedOrAnswer(field_name,
                             DecoratedField(field_name,
                                            label=H2(field_label),
                                            classes="Construction",
                                            infix="",
                                            suffix=hr))]

def constructions(in_increasing:bool):
    return [construction(show_increasing=in_increasing, in_increasing=in_increasing), construction(show_increasing=not in_increasing, in_increasing=in_increasing)]

def longLine(line, construction):
    line = addBoilerplate(
        [namesNotationsDenotedBy,
         AskedOrNot("Definition",
                    QuestionOrAnswer(markOfQuestion,
                                     line),
                    line), construction],)
    return [AtLeastOneField(asked=True,
                           fields=listOfSideFieldNames,
                           child=[suspend("Hide sides"), line],
                           otherwise=line)]


increasing = Empty("Hide sides", longLine(increasing_(True), constructions( in_increasing=True)))
decreasing = Empty("Hide sides", longLine(decreasing_, constructions(in_increasing=False)))

inc_to_emphasize = increasing_(False)
increasing_meta_content = [
    namesNotationsDenotedBy,
    AskedOrNot("Definition",
                QuestionOrAnswer(markOfQuestion,
                                 inc_to_emphasize),
                inc_to_emphasize),
    constructions(in_increasing=True),
    ]
increasing_meta = addBoilerplate(increasing_meta_content)

def relation(left, right):
    if left < right:
        relation = increaseRelation
        asked = "Smaller to greater"
    elif right < left:
        relation = decreaseRelation
        asked = "Greater to smaller"
    else:
        assert False
    relation = relation.getNormalForm().assumeAsked(asked)
    leftField = listOfSideFields[left]
    rightField = listOfSideFields[right]
    leftFieldName = listOfSideFieldNames[left]
    rightFieldName = listOfSideFieldNames[right]
    in_increasing=left < right
    l = [header, leftField, relation, rightField, constructions(in_increasing=in_increasing), footer(),]
    filled = Filled(leftFieldName, Filled(rightFieldName, l))
    return Empty("Hide middle", filled)

relation_example = examplesAskedParam(increasing_meta_content)
relation_counter_example = counterexamplesAskedParam(increasing_meta_content)
