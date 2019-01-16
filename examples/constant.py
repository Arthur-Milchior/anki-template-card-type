from .general import short_header, footer
from ..generators.imports import *

number=[QuestionnedField("Significative digit"),
        Filled("Exponant",
               [Filled("Significative digit","."),
                FilledOrEmpty("Basis",QuestionnedField("Basis"),"10"),
                SUP(QuestionnedField("Exponant"))
               ]
        )]

typedNumber= [number, QuestionnedField("Typ"),hr]
types=Filled("Typ",
             PotentiallyNumberedFields("Typ",
                                       5,
                                       label="Type",
                                       suffix=hr)
             )
typeOrNumber = AtLeastOneField(typedNumber,
                               fields = ["Significative digit",
                                         "Exponant",
                                         "Basis"],
                               otherwise = types)


definition = TableFields(
    ["Name",
     "Abbreviation",
     "Etymology",
     "French",
     "DenotedBy",
     "Represents"],
    greater = 2,
    name = "Definition",
    suffix=hr
)
sis=Answer(
    [
        TableFields(
            [
                "kg",
                "m",
                "s",
                "A",
                "lm",
                "bit",
                "Kelvin",
                "mol",
                "rad",
                "cd",
                "sr",
            ],
            name = "si details"
        ),
        hr])
constant = [short_header, definition, typeOrNumber, sis, footer]

#find to deal with both represents
