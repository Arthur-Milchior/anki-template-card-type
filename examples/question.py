from .general import header, footer
from ..generators.imports import *

answers = PotentiallyNumberedFields("Answer",
                                    7,
                                    label = Field("Question"),
                                    infix = None,
                                    suffix = hr)
                                    
question = [Filled("Question",
                   [header, answers, DecoratedField("Construction", suffix=hr), footer]),
            hr]
