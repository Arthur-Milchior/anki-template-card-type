from ...generators import *

def localFun(i):
    appliedTo = f"Applied to{i}"
    example = f"Example{i}"
    child = LI(FilledOrEmpty(appliedTo,
                             DecoratedField(prefix="On ",
                                            label = {appliedTo},
                                            field= example,
                                            suffix=""),
                             QuestionnedField(example,classes="Example")))
    return {"child":child,
            "questions":{example},
            "filledFields":[example]}

_examples = ('Example',
             NumberedFields('Example',
                            4,
                            suffix=hr,
                            localFun= localFun,
                            isMandatory = False))
_counterexamples = ('Counterexample',PotentiallyNumberedFields('Counterexample', 4, isMandatory = False, suffix=hr))

def showOnAnswerOrQuestion(child, Name):
    return QuestionOrAnswer(AtLeastOneField(child,
                                            [f"{Name}{i}" for i in ["s","","2","3","4"]],
                                            asked=True),
                            child)
examples = showOnAnswerOrQuestion(_examples,"Example")
counterexamples = showOnAnswerOrQuestion(_counterexamples,"Counterexample")


