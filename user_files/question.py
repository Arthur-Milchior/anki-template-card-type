from .general import header, footer
from ..generators.imports import *

answers = PotentiallyNumberedFields("Answer",
                                    7,
                                    prefix=DecoratedField("Question",suffix=[":",br]),
                                    infix=None,
                                    label="",
                                    suffix=hr)
                                    
question = Filled("Question",
                  [header, answers, DecoratedField("Construction", suffix=hr), footer])
