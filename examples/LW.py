from ..generators import *
firstName = QuestionnedField("First name")
lastName = QuestionnedField("Last name", classes= "Notation")
fullName = Cascade("Full name",[firstName,lastName,br],["First name","Last name"])
talkOf = DecoratedField("Talk of",suffix=br, classes= "Definition")
workshop = DecoratedField("Workshop",suffix=br, classes= "Definition2")
lw=[fullName,workshop,talkOf,QuestionnedField("Picture")]
