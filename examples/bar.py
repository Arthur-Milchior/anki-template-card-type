from ..generators import *
from .general import footer, header

definition_bar = TableFields(
    name="Bar",
    fields=[]
)
properties = TableFields([])

bar = [header, definition_bar, properties, footer]
