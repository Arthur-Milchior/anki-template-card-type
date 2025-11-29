from ..style import *
from ..util import question

def _language(word, answer, language):
    return question(word, " in ", language, " is ", answer)

def langage(word, answer, language):
    return question(word, " en ", language, " est ", answer)

_french = _language("Name", "French", "French")
_english = _language("French", "Name", "English")

deJaponais = langage("Japonais", "French", "Français")()
versJaponais = langage("French", "Japonais", "Japonais")()

french = _french()
french2 = _french("2")
english = _english()
english2 = _english("2")
