from .general import header, footer
from ..generators import *

answers = PotentiallyNumberedFields("Answer",
                                    7,
                                    label = QuestionnedField("Question"),
                                    infix = None,
                                    suffix = hr,
                                    classes = "Notation")
                                    
questionGen = [Filled("Question",
                      [header, answers, DecoratedField("Construction", suffix=hr, classes = "DenotedBy"), footer]),
            hr]
