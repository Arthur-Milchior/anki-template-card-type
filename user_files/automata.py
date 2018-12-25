from general import header, footer

automata = [
    header,
    TableFields(
        listName = "automata",
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
