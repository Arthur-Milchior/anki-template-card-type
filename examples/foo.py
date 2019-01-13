from .general import header, footer
from ..generators.imports import *

definition_bar = TableFields(
    name = "Bar",
    fields = []
)
properties = TableFields([])

bar = [header, definition_bar, properties, footer]
