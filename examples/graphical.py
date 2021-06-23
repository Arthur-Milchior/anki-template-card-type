from ..generators import *
from .general import footer, header
from .util import *
from .general import namesNotationsDenotedBy

properties = TableFields([
    {"field":   "Location",
     "classes": "Definition"},
    {"field":   "Description",
     "classes": "Definition2"},
])

graphical = addBoilerplate([namesNotationsDenotedBy, properties])
