from ...generators import *


def _example(i=""):
    appliedTo = f"Applied to{i}"
    example = f"Example{i}"
    return FilledOrEmpty(appliedTo,
                         DecoratedField(prefix="On ",
                                        label={appliedTo},
                                        field=example,
                                        suffix=""),
                         QuestionnedField(example, classes="Example"))


def localFun(i):
    example = f"Example{i}"
    child = LI(_example(i))
    return {"child": child,
            "questions": {example},
            "filledFields": [example]}


_examples = ('Example',
             PotentiallyNumberedFields('Example',
                                       4,
                                       suffix=hr,
                                       localFunMultiple=localFun,
                                       singleCase=DecoratedField(label="Example",
                                                                 field="Example",
                                                                 child=_example(
                                                                     ""),
                                                                 suffix=hr),
                                       isMandatory=False))
_counterexamples = ('Counterexample', PotentiallyNumberedFields(
    'Counterexample', 4, isMandatory=False, suffix=hr))


def showOnAnswerOrQuestion(child, Name):
    return QuestionOrAnswer(AtLeastOneField(child,
                                            [f"{Name}{i}" for i in [
                                                "s", "", "2", "3", "4"]],
                                            asked=True),
                            child)


examples = showOnAnswerOrQuestion(_examples, "Example")
counterexamples = showOnAnswerOrQuestion(_counterexamples, "Counterexample")
