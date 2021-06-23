from ..generators import *
from .util import *
from .style import *

def translationToEnglish(language):
    l = [CLASS("quote", Field(language)),
         f" (in {language}) means ",
         QuestionnedField(field="English",
                          child=CLASS("quote", Field("English")))]
    return ensureGen(l).assumeAsked("English")


def translationFromEnglish(language):
    l = [QuestionnedField(field=language, child=CLASS("quote", Field(language))),
         f" {language} is ",
         CLASS("quote", Field("English"))
    ]
    return ensureGen(l).assumeAsked(language)
