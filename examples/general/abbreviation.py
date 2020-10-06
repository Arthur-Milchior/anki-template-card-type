from ..util import *

_toAbbreviation = question(
    "Name", "'s ", "abbreviation", " is ", "Abbreviation")
toAbbreviation = _toAbbreviation()
toAbbreviation2 = _toAbbreviation("2")

_abbreviation = question(
    "Abbreviation", "", " means ", "", "Name")
abbreviation = _abbreviation()
abbreviation2 = _abbreviation("2")
abbreviation3 = _abbreviation("3")

