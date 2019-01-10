from ..generators.imports import *
from .general import header, footer


automata = [
    header,
    TableFields(
        name = "Automata",
        fields = ["States",
                  "Locations",
                  "Alphabet",
                  "Initial",
                  "Final",
                  "q.a",
                  "Typ",
                  "Labels",
                  "Clock number"],
    ),
    footer
]
