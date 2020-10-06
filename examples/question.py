from ..generators import *
from .general import footer, header
from .util import *
from .general.names import names
from .general.examples import examples

answers = PotentiallyNumberedFields("Answer",
                                    7,
                                    label=QuestionnedField("Question"),
                                    infix=br,
                                    classes="Definition")

questionGen = addBoilerplate(
    [
        names(suffix=hr),
        answers,
        hr,
        ShowIfAskedOrAnswer("Construction",
                            DecoratedField("Construction", suffix=hr, classes="DenotedBy")),
        examples(prefix=hr),
    ]
)
