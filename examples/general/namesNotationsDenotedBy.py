from ...generators import *
from .foot import footer
from .names import singleOrMultipleNames
from .notations import _notations
from .short_head import short_header

_namesNotationsDenotedBy = Cascade(child=[singleOrMultipleNames,
                                          _notations,
                                          DecoratedField('Representation',suffix=hr),
                                          DecoratedField('Denoted by',suffix=hr)],
                                   cascade = {"Names","Notations","Representation","Denoted by"},
                                   field="NamesNotationsDenotedBy")
namesNotationsDenotedBy = [short_header,_namesNotationsDenotedBy,footer]
