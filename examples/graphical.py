from .general import header, footer
from ..generators import *

properties = TableFields([
    {"field":   "Location",
     "classes":"Definition"},
    {"field":   "Description",
     "classes":"Definition2"},
])

graphical = [header, properties, footer]
