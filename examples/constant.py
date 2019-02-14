from .general import short_header, footer
from ..generators import *

number=[QuestionnedField("Significative digit", classes= "Definition"),
        Filled("Exponant",
               [Filled("Significative digit","."),
                FilledOrEmpty("Basis",QuestionnedField("Basis", classes= "Definition2"),"10"),
                SUP(QuestionnedField("Exponant", classes= "Definition3"))
               ]
        )]

typedNumber= [number, QuestionnedField("Typ"),hr]
typedNumber  = Cascade("Typs",typedNumber,{"Typ"})
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
     {"field":"Represents",
      "classes":"Intuition"}],
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
