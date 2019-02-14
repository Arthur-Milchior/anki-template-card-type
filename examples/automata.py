from ..generators import *
from .general import header, footer


automata = [
    header,
    TableFields(
        name = "Automata",
        fields = [
            {"field": "States",
             "classes":"Definition"},
            {"field": "Locations",
             "classes":"Definition2"},
            {"field": "Alphabet",
             "classes":"Definition3"},
            {"field": "Initial",
             "classes":"Definition4"},
            {"field": "Final",
             "classes":"Definition5"},
            {"field": "Transitions",
             "classes":"Definition6"},
            {"field": "Typ",
             "classes":"Definition7"},
            {"field": "Labels",
             "classes":"Definition8"},
            {"field": "Actions",
             "classes":"Definition6"},
            {"field": "Edges",
             "classes":"Definition6"},
            {"field": "Labeling function",
             "classes":"Definition8"},
            {"field": "Clock number",
             "classes":"Definition9"}]),
    footer
    ]
