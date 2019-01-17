from ...generators import *
from .short_head import short_header
from .foot import footer

_notations = Filled("Notation",
                    [('Notation',PotentiallyNumberedFields('Notation', 4, isMandatory = False)),
                     hr])
notations = ("Notation2",[short_header,_notations,footer])
