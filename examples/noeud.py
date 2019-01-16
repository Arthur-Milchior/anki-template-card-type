from .general import header, footer
from ..generators.imports import *

def localFun(i):
    fig = TD(QuestionnedField(field=f"Step{i}", child={f"Figure{i}"}))
    step = TD(QuestionnedField(field=f"Step{i}"))
    return {"child":[fig,step],
            "questions":{f"Step{i}"},
            "filledFields":[f"Step{i}",f"Figure{i}"]}

def globalFun(l):
    description = QuestionnedField(field=f"Description")
    result = QuestionnedField(field=f"Description", child={"Result"})
    return Table([[description, result]]+l)
steps = NumberedFields(fieldPrefix="Step",
                       greater=5,
                       localFun=localFun,
                       globalFun=globalFun)

properties = TableFields(["Interest","Types","Fiable","Réglable", "Décoratif", "Défaisable"])

noeud = [header, steps, properties, footer]
