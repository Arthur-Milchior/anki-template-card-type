from .general import header, footer
from ..generators.imports import *

definition_foo = TableFields(
    name = "foo",
    fields = []
)
properties = TableFields([])

foo = [header, definition_foo, properties, footer]
