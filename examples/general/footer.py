from ...generators import *
from ..style import *

origin = [
    DecoratedField("Chapter", infix=" ", suffix=", ", isMandatory=True),
    DecoratedField("Section", infix=" ", suffix=", ", isMandatory=True),
    FilledOrEmpty("Kind",
                  [Field("Kind", isMandatory=True),
                   Filled("Index", [" ", {"Index"}], isMandatory=True),
                   ", "],
                  DecoratedField("Index", infix=" ", suffix=", ", isMandatory=True)),
    DecoratedField("Page", infix=" ", suffix=", ")
]

"""Show all informations that gives card context. Only the assumption are sometime asked, there are no other questions."""
footer = FOOTER(
    [
        P(Field("Variables")),
        DecoratedField("Assuming", emphasizing=decorateQuestion),
        Empty("Context", P(deck)),
        Answer(
            [P(Field("Extra")),
             origin])]
)

