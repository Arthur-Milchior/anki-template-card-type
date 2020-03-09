from ..generators import *
from .general import footer, header

automata = [
    header,
    ("Typ", [{"Typ"}, ":"]),
    TableFields(
        name="Automata",
        fields=[
            {"field": "States",
             "classes": "Definition"},
            {"field": "Locations",
             "classes": "Definition2"},
            {"field": "Alphabet",
             "classes": "Definition3"},
            {"field": "Initial",
             "classes": "Definition4"},
            {"field": "Final",
             "classes": "Definition5"},
            {"field": "Transitions",
             "classes": "Definition6"},
            {"field": "Labels",
             "classes": "Definition8"},
            {"field": "Actions",
             "classes": "Definition6"},
            {"field": "Edges",
             "classes": "Definition6"},
            {"field": "Labeling function",
             "classes": "Definition8"},
            {"field": "Clock number",
             "classes": "Definition9"}]),
    footer
]
