from ..generators.imports import *

name = CLASS(["Name","Chord name"],
             [QuestionnedField("Base", mandatory=True),
              QuestionnedField("Quality", mandatory=True),
              QuestionnedField("Inverval", mandatory=True),
              Filled("Over",["/",QuestionnedField("Over", mandatory=True)]
              )])

def color(name):
    def aux(i):
        return QuestionOrAnswer(QuestionnedField(f"{name}{i}", mandatory=True),
                                FilledOrEmpty(f"{name} color{i}",
                                              QuestionnedField(f"{name} color{i}", mandatory=True),
                                              QuestionnedField(f"{name}{i}", mandatory=True)))
    return aux
diagram = color("Diagram")
partition = color("Partition")

table = TableFields(
    [
        {"function":diagram,
         "field": "Diagram",
         "filledFields":"Diagram"},
        {"function":partition,
         "field": "Partition",
         "filledFields":"Partition"},
        ["Unison",
          "3rd",
          "5th",
          "Nth"],
    ],
    greater=5,
    isMandatory=True)

guitarChord = [name,table]
