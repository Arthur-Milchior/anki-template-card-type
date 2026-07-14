from ..generators import *
from .util import *

def mathjax_field(field_name):
    return Field(field_name, useClasses=False)

def mt_table_entry(field_name):
    return {
        "field": field_name,
        "label": field_name,
        "function": lambda _: mathjax_field(field_name)}

definition = TableFields(
    fields=[
        mt_table_entry("Formula"),
        mt_table_entry("Formula2"),
        "Definition",
        mt_table_entry("Taylor series"),
        "Domain",
        "Codomain",
        "Radius",
    ],
    name="Definitions"
)
properties = TableFields([
    "Parity",
    "Continuous",
    "Measurable",
    "Monotonic",
    "Measure",
    "Period",
    ["Zero",
     "Unit"],
    [mt_table_entry("Derivative"),
     mt_table_entry("Nth derivative"),
     mt_table_entry("Integral")],
    "Inverse",
    "Partial fractions",
    "Differential equation",
    "Infinite product expansion",
    "Continued fraction",
    "Fixed points",
    "Roots",
    "Poles",
])

analysis = addBoilerplate([H1(mathjax_field("Notation")), definition, properties])
