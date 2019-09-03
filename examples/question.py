from ..generators import *
from .general import footer, header

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
