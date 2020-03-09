from ...generators import *
from .foot import footer
from .short_head import short_header

_notations = Filled("Notation",
                    [('Notation', PotentiallyNumberedFields('Notation', 4, isMandatory=False)),
                     hr])
notations = ("Notation2", [short_header, _notations, footer])
