from ...generators import *
from ..general import footer, header

firstName = QuestionnedField("First name", classes="Notation")
lastName = QuestionnedField("Last name", classes="Name")
fullName = Cascade("Full name",[firstName,lastName,br],{"First name","Last name"})
knownFor = DecoratedField("Known for",suffix=br)
_face=[fullName,knownFor,QuestionnedField("Picture")]
face=header+_face+footer
