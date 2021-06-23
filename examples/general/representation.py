from ..util import *
from ..style import *

representation = addBoilerplate(FromAndTo("Name", " is ", "represented by", " ", "Representation"), {"Representation", "Name"})
represents = addBoilerplate(FromAndTo("Representation", " ", "represents", " ", "Name"), {"Representation", "Name"})
