from ...generators.imports import *
from ..general import header, footer

firstName = QuestionnedField("First name")
lastName = QuestionnedField("Last name")
fullName = Cascade("Full name",[firstName,lastName,br],["First name","Last name"])
knownFor = DecoratedField("Known for",suffix=br)
_face=[fullName,knownFor,QuestionnedField("Picture")]
face=header+_face+footer
