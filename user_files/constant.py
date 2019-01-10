from .general import header, footer
from ..generators.imports import *

number=[QuestionnedField("Significative digit"),
        Filled("Exponant",
               [Filled("Significative digit","."),
                FilledOrEmpty("Basis",QuestionnedField("Basis"),"10"),
                SUP(QuestionnedField("Exponant"))
               ]
        )]

typedNumber= [number, QuestionnedField("Typ")]

types=PotentiallyNumberedFields("Typ",
                                5,
                                label="Type")

constant = [header, typedNumber, types, footer]

#find to deal with both represents
