from ..generators.imports import *
firstName = QuestionnedField("First name")
lastName = QuestionnedField("Last name")
fullName = Cascade("Full name",[firstName,lastName,br],["First name","Last name"])
knownFor = DecoratedField("Known for",suffix=br)
nameExample=[fullName,knownFor,QuestionnedField("Picture")]
