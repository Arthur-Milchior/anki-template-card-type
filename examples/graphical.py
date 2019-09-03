from ..generators import *
from .general import footer, header

properties = TableFields([
    {"field":   "Location",
     "classes":"Definition"},
    {"field":   "Description",
     "classes":"Definition2"},
])

graphical = [header, properties, footer]
