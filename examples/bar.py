from ..generators import *
from .general import footer, header
from ..util import *

definition_bar = TableFields(
    name="Bar",
    fields=[]
)
properties = TableFields([])

bar = addBoilerplate([definition_bar, properties])
