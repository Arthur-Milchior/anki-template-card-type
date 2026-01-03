from ...generators import *
from ..util import *
from .names import names
from .namesNotationsDenotedBy import namesNotationsDenotedBy
from ..style import *

def _appliedTo(i):
    """On {{applied to}}: {{Example}}"""
    appliedTo = numbered_field("Applied to", i)
    example = numbered_field("Example", i)
    return DecoratedField(prefix="On ",
                   label={appliedTo},
                   field=example,
                   suffix="")

def exampleLine(i):
    """Either
    On {{applied to}}: {{Example}}
    or
    {{Example}} """
    appliedTo = numbered_field("Applied to", i)
    exampleField = numbered_field("Example", i)
    return Filled(exampleField,
                  LI(FilledOrEmpty(appliedTo,
                                   _appliedTo(i),
                                   DecoratedField(exampleField, classes="Example", emphasizing=decorateQuestion))))

def _exampleAsked(i):
    """
    Line of Example 3
    Line of Example 4
    Line of Example 1
    Ask example 2
    """
    l = []
    for j in range(i + 1, i + 4):
        if j > 4:
            j -= 4
        l.append(exampleLine(j))
    l.append(AskedField(numbered_field("Example", i), question="Or ?"))
    return addBoilerplate(UL(l, addLi=False))
    

def exampleAsked(i):
    """All necessary text to ask i-th example"""
    appliedToField = f"""Applied to{empty1(i)}"""
    exampleField = numbered_field("Example", i)
    example = FilledOrEmpty(appliedToField,
                            _appliedTo(i),
                            _exampleAsked(i)
    )
    example = example.assumeAsked(exampleField)
    example = addBoilerplate([namesNotationsDenotedBy, example], exampleField)
    if i == 1:
        # ask example 1 separately only if there are multiple examples
        example = Filled("Example2", example)
    return example

"""Show all examples"""
def examples(prefix=None):
    return Cascade("Examples",
                   Filled("Example",
                          [prefix,
                           FilledOrEmpty("Example2",
                                         UL([exampleLine(i) for i in range (1,5)], addLi=False),
                                         exampleLine(1)
                           )]
                   ),
                   {numbered_field("Example", i) for i in range(1, 5)}
                   )

"""Ask all examples"""
def examplesAskedParam(content=namesNotationsDenotedBy):
    return addBoilerplate(
        QuestionnedField("Examples", child=[content, examples(prefix=hr)]),
        "Example"
    ).assumeAsked(["Example", "Example2", "Example3", "Example4"])

examplesAsked = examplesAskedParam()


# def localFun(i):
#     example = f"Example{i}"
#     child = LI(_example(i))
#     return {"child": child,
#             "questions": {example},
#             "filledFields": [example]}


# _examples = ('Example',
#              PotentiallyNumberedFields('Example',
#                                        4,
#                                        suffix=hr,
#                                        localFunMultiple=localFun,
#                                        singleCase=DecoratedField(label="Example",
#                                                                  field="Example",
#                                                                  child=_example(
#                                                                      ""),
#                                                                  suffix=hr),
#                                        isMandatory=False))
# _counterexamples = ('Counterexample', PotentiallyNumberedFields(
#     'Counterexample', 4, isMandatory=False, suffix=hr))


# def showOnAnswerOrQuestion(child, Name):
#     return QuestionOrAnswer(AtLeastOneField(child,
#                                             [f"{Name}{i}" for i in [
#                                                 "s", "", "2", "3", "4"]],
#                                             asked=True),
#                             child)


# examples = showOnAnswerOrQuestion(_examples, "Example")
# counterexamples = showOnAnswerOrQuestion(_counterexamples, "Counterexample")
