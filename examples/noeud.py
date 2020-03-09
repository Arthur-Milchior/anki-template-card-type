from ..generators import *
from .general import footer, header


def localFun(i):
    nb = TD(str(i or 1))
    fig = TD(QuestionnedField(field=f"Step{i}", child={
             f"Figure{i}"}, classes="Definition"))
    step = TD(QuestionnedField(field=f"Step{i}", classes="Definition"))
    return {"child": TR([nb, step, fig]),
            "questions": {f"Step{i}"},
            "filledFields": [f"Step{i}", f"Figure{i}"]}


def globalFun(l):
    result = "No figure at all"
    for i in ["Figure", "Figure2", "Figure3", "Figure4", "Figure5", "Result"]:
        result = FilledOrEmpty(i,
                               {i},
                               result)
    description = TH(QuestionnedField(
        field=f"Description", classes="Notation"))
    result = TH(QuestionnedField(field=f"Description",
                                 child=result, classes="Notation"))
    return Table([TR([description, result])]+l)


def steps(i):
    return NumberedFields(fieldPrefix="Step",
                          greater=i,
                          localFun=localFun,
                          globalFun=globalFun)


properties = TableFields(
    ["Interest", "Types", "Fiable", "Réglable", "Décoratif", "Défaisable"])


def noeudContruction(i):
    return [header, steps(i), footer]


noeud = noeudContruction(5)
