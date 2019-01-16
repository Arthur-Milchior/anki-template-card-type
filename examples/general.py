from ..generators.imports import *

contextOrDeck = [FilledOrEmpty('Context',
                               DecoratedField('Context', isMandatory = True),
                               ["Deck: ",deck]), hr]


def _name_extra(i=""):
    field = f"Name{i}"
    relatedInformation = ListFields(fields = [f"Abbreviation", f"French", f"Etymology"],
                                    localFun = (lambda f: {"child":Parenthesis(DecoratedField(field=f"{f}{i}",
                                                                                              label=f,
                                                                                              suffix="",
                                                                                              classes = f)),
                                                           "filledFields":[f"{f}{i}"]}))
    return relatedInformation

_names = ["Names: ",
          ListFields(fields = ["","2","3","4"],
                     localFun = (lambda i: {"child":LI([QuestionnedField(f"Name{i}",classes=["Name"]),
                                                        NotAsked(f"Name{i}",_name_extra(i))]),
                                            "questions":f"Name{i}",
                                            "filledFields":[f"Name{i}"]}),
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
                    [('Notation',PotentiallyNumberedFields('Notation', 4, isMandatory = False)),
                     hr])
_examples = ('Example',
             NumberedFields('Example',
                            4,
                            suffix=hr,
                            localFun= (lambda i:{"child":LI(FilledOrEmpty(f"Applied to{i}",
                                                                  DecoratedField(prefix="On ",
                                                                                 label = {f"Applied to{i}"},
                                                                                 field=f"Example{i}",
                                                                                 suffix=""),
                                                                  QuestionnedField(f"Example{i}",classes="Example"))),
                                                 "questions":{f"Example{i}"},
                                                 "filledFields":[f"Example{i}"]}),
                            isMandatory = False))
_counterexamples = ('Counterexample',PotentiallyNumberedFields('Counterexample', 4, isMandatory = False))

_namesNotationsDenotedBy = Cascade(child=[name_s,
                                          _notations,
                                          DecoratedField('Representation',suffix=hr),
                                          DecoratedField('Denoted by',suffix=hr)],
                                   cascade = ["Names","Notations","Representation","Denotedy by"],
                                   field="NamesNotationsDenotedBy")
short_header =CLASS("head",[contextOrDeck,('Variables', [DecoratedField('Variables'), hr] ),('Assuming',[DecoratedField('Assuming'),br])])
header = [short_header, _namesNotationsDenotedBy]

origin= [
    DecoratedField("Chapter", infix=" ", suffix=", ", isMandatory = True),
    DecoratedField("Section", infix=" ", suffix=", ", isMandatory = True),
    FilledOrEmpty("Kind",
                  [Field("Kind", isMandatory = True),
                   Filled("Index", [" ",("Index")],isMandatory = True),
                   ", "],
                  DecoratedField("Index", infix=" ", suffix=", ", isMandatory = True)),
    DecoratedField("Page", infix=" ", suffix=", ")
]
answerFooter= CLASS("footer",Answer([DecoratedField('Extra', suffix=hr),origin]))
footer = [_examples,_counterexamples, answerFooter]
namesNotationsDenotedBy = header+footer
names = ("Name2",[short_header,_names, footer])
notations = ("Notation2",[short_header,_notations,footer])
typDic = {"field":"Typ",
          "label":"Type",
          "filledFields":["Typ"],
          "questions":"Typ"}
