from .general import header, footer
from ..generators import *

def localFun(i):
    fig = TD(QuestionnedField(field=f"Step{i}", child={f"Figure{i}"},classes="Definition"))
    step = TD(QuestionnedField(field=f"Step{i}",classes="Definition"))
    return {"child":TR([step,fig]),
            "questions":{f"Step{i}"},
            "filledFields":[f"Step{i}",f"Figure{i}"]}


def globalFun(l):
    result = "No figure at all"
    for i in  ["Figure","Figure2","Figure3","Figure4","Figure5","Result"]:
        result = FilledOrEmpty(i,
                               {i},
                               result)
    description = TH(QuestionnedField(field=f"Description",classes="Notation"))
    result = TH(QuestionnedField(field=f"Description", child=result,classes="Notation"))
    return Table([TR([description, result])]+l)

steps = NumberedFields(fieldPrefix="Step",
                       greater=5,
                       localFun=localFun,
                       globalFun=globalFun)

properties = TableFields(["Interest","Types","Fiable","Réglable", "Décoratif", "Défaisable"])

noeud = [header, steps, properties, footer]
