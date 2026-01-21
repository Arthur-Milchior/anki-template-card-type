from ..generators import *
from .general import footer, header
from .util import *
from .style import *
from .general import namesNotationsDenotedBy
from .general.examples import examples

answers = PotentiallyNumberedFields("Answer",
                                    16,
                                    label=QuestionnedField("Question"),
                                    infix=br,
                                    numbered_field=numbered_field,
                                    classes="Definition")

questionGen = addBoilerplate(
    [
        namesNotationsDenotedBy,
        answers,
        hr,
        ShowIfAskedOrAnswer("Construction",
                            DecoratedField("Construction", suffix=hr, classes="DenotedBy")),
        examples(prefix=hr),
    ]
)
