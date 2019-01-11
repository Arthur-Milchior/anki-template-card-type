from ..generators.imports import *
contextOrDeck = [FilledOrEmpty('Context', DecoratedField('Context'),["Deck: ",deck]), hr]


def _name_extra(i=""):
    field = f"Name{i}"
    relatedInformation = ListFields(fields = [f"Abbreviation", f"French", f"Etymology"],
                                    localFun = (lambda f: (Parenthesis(DecoratedField(field=f"{f}{i}",label=f,suffix="")),{f"{f}{i}"})))
    return relatedInformation

_names = ["Names: ",
          ListFields(fields = ["","2","3","4"],
                     localFun = (lambda i: (LI([QuestionnedField(f"Name{i}",classes=["Name"]),
                                                NotAsked(f"Name{i}",_name_extra(i))]),
                                            {f"Name{i}"},
                                            {f"Name{i}"})),
                     globalFun = (lambda l: UL(l,addLi=False)))]

name_s= Filled("Name",
               child=[
                   Cascade(child=FilledOrEmpty("Name2",
                                               _names,
                                               DecoratedField("Name",suffix=[_name_extra(),br])),
                           field="Names",
                           cascade=["Name","Name2","Name3","Name4"]),
                   hr])

_notations = Filled("Notation",
                    [('Notation',PotentiallyNumberedFields('Notation',4)),
                     hr])
_examples = ('Example',
             NumberedFields('Example',
                            4,
                            suffix=hr,
                            localFun= (lambda i:(LI(FilledOrEmpty(f"Applied to{i}",
                                                                  DecoratedField(prefix="On ",
                                                                                 label = {f"Applied to{i}"},
                                                                                 field=f"Example{i}",
                                                                                 suffix=""),
                                                                  QuestionnedField(f"Example{i}",classes="Example"))),
                                                 {f"Example{i}"},{f"Example{i}"}))))
_counterexamples = ('Counterexample',PotentiallyNumberedFields('Counterexample',4))

_namesNotationsDenotedBy = Cascade(child=[name_s,
                                          _notations,
                                          DecoratedField('Representation',suffix=hr),
                                          DecoratedField('Denoted by',suffix=hr)],
                                   cascade = ["Names","Notations","Representation","Denotedy by"],
                                   field="NamesNotationsDenotedBy")
short_header =[contextOrDeck,('Variables', [DecoratedField('Variables'), hr] ),('Assuming',[DecoratedField('Assuming'),br])] 
header = short_header + [_namesNotationsDenotedBy]
namesNotationsDenotedBy = header
names = ("Name2",[short_header,_names])
notations = ("Notation2",[short_header,_notations])

origin= [
    DecoratedField("Chapter", infix=" ", suffix=", "),
    DecoratedField("Section", infix=" ", suffix=", "),
    FilledOrEmpty("Kind",
                  [{"Kind"},
                   Filled("Index", [" ",{"Index"}]),
                   ", "],
                  DecoratedField("Index", infix=" ", suffix=", ")),
    DecoratedField("Page", infix=" ", suffix=", ")
]
answerFooter= Answer([DecoratedField('Extra', prefix=hr, suffix=""),origin])
footer = [_examples,_counterexamples, answerFooter]
