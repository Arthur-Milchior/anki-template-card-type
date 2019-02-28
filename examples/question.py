from .general import header, footer
from ..generators import *

answers = PotentiallyNumberedFields("Answer",
                                    7,
                                    label = QuestionnedField("Question"),
                                    infix = None,
                                    suffix = hr,
                                    classes = "Definition")

questionGen = [header,
               answers,
               ShowIfAskedOrAnswer("Construction",
                                   DecoratedField("Construction", suffix=hr, classes = "DenotedBy")),
               footer,
               hr]
