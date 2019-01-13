from ..generators.imports import *
firstName = QuestionnedField("First name")
lastName = QuestionnedField("Last name")
fullName = Cascade("Full name",[firstName,lastName,br],["First name","Last name"])
talkOf = DecoratedField("Talk of",suffix=br)
workshop = DecoratedField("Workshop",suffix=br)
lw=[fullName,workshop,talkOf,QuestionnedField("Picture")]
