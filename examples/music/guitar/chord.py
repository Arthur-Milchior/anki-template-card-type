from ...util import numbered_field
from ....generators import *

name = CLASS(["Name", "Chord name"],
             [QuestionnedField("Base", isMandatory=True, classes="Definition"),
              QuestionnedField("Quality", isMandatory=True,
                               classes="Definition2"),
              QuestionnedField("Inverval", isMandatory=True,
                               classes="Definition4"),
              Filled("Over", ["/", QuestionnedField("Over", isMandatory=True)]
                     )])


def color(name):
    def aux(i):
        return QuestionOrAnswer(QuestionnedField(f"{name}{i}", isMandatory=True),
                                FilledOrEmpty(f"{name} color{i}",
                                              QuestionnedField(
                                                  f"{name} color{i}", isMandatory=True),
                                              QuestionnedField(f"{name}{i}", isMandatory=True)))
    return aux


diagram = color("Diagram")
partition = color("Partition")

table = TableFields(
    [
        {"function": diagram,
         "field": "Diagram",
         "filledFields": "Diagram"},
        {"function": partition,
         "field": "Partition",
         "filledFields": "Partition"},
        [
            {"field": "Unison",
             "classes": ["Definition", "Guitar chord"]},
            {"field": "3rd",
             "classes": ["Definition2", "Guitar chord"]},
            {"field": "5th",
             "classes": ["Definition3", "Guitar chord"]},
            {"field": "Nth",
             "classes": ["Definition4", "Guitar chord"]},
        ]],
    numbered_field=numbered_field,
    greater=5,
    isMandatory=True)

guitarChord = [name, table]
