from ..generators.imports import *

def _name(i):
    name = QuestionnedField(f"Name{i}",classes=["Answer", "Answer_Name"])
    return ListFields(fields = [f"Abbreviation", f"French", f"Etymology"],
                      localFun = (lambda f: Parenthesis(DecoratedField((f"f{i}","f"),suffix=""))),
                      globalSep = (lambda f: ", "),
                      globalFun = (lambda l: (f"Name{i}",[name,l])))

_names= ListFields(fields = ["","2","3","4"],
                  localFun = (lambda f: (f"Name{i}",LI(_name(f)))),
                  globalFun = (lambda l: UL(l)))

names= FilledOrEmpty("Name2",
                     _names,
                     _name(""))

namesNotationsDenotedBy = [names,
                           ('Notation',PotentiallyNumberedFields('Notation',4)),
                           DecoratedField('Representation'),
                           DecoratedField('Denoted by'),
]

contextOrDeck = [FilledOrEmpty('Context', DecoratedField('Context'),["Deck: ",deck]), hr]
header = HEADER([contextOrDeck,('Variables', [DecoratedField('Variables'), hr] )])
extendedHead = [header, ('Assuming',[{'Assuming'},br]), namesNotationsDenotedBy]

footer = FOOTER(Filled('Extra', [hr,Field('Extra')]))

