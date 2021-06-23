from ..generators import *
from .general import footer, header
from .util import *

number = [QuestionnedField("Significative digit", classes="Definition"),
          Filled("Exponant",
                 [Filled("Significative digit", "."),
                  FilledOrEmpty("Basis", QuestionnedField(
                      "Basis", classes="Definition2"), "10"),
                  SUP(QuestionnedField("Exponant", classes="Definition3"))
                  ]
                 )]

typedNumber = [number, QuestionnedField("Typ"), hr]
typedNumber = Cascade("Typs", typedNumber, {"Typ"})
types = Filled("Typ",
               PotentiallyNumberedFields("Typ",
                                         5,
                                         label="Type",
                                         suffix=hr)
               )
typeOrNumber = AtLeastOneField(typedNumber,
                               fields=["Significative digit",
                                       "Exponant",
                                       "Basis"],
                               otherwise=types)


definition = TableFields(
    ["Name",
     "Abbreviation",
     "Etymology",
     "French",
     "DenotedBy",
     {"field": "Represents",
      "classes": "Intuition"}],
    greater=2,
    name="Definition",
    suffix=hr
)
sis = Answer(
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
            name="si details"
        ),
        hr])
constant = addBoilerplate([definition, typeOrNumber, sis])

# find to deal with both represents


def _represented(i=1):
    questionField = f"Represents{empty1(i)}"
    answer = f"Name{empty1(i)}"
    return FromAndTo(questionField, ' ', 'is represented by', ' ', answer, classes="Name")

represented = _represented()
represented2 = _represented(2)
