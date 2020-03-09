from ...generators import *
from .examples import counterexamples, examples

origin = [
    DecoratedField("Chapter", infix=" ", suffix=", ", isMandatory=True),
    DecoratedField("Section", infix=" ", suffix=", ", isMandatory=True),
    FilledOrEmpty("Kind",
                  [Field("Kind", isMandatory=True),
                   Filled("Index", [" ", ("Index")], isMandatory=True),
                   ", "],
                  DecoratedField("Index", infix=" ", suffix=", ", isMandatory=True)),
    DecoratedField("Page", infix=" ", suffix=", ")
]
answerFooter = CLASS("footer", Answer(
    [DecoratedField('Extra', suffix=hr), origin]))
footer = [examples, counterexamples, answerFooter]
