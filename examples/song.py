from ..generators import *
from .general.footer import footer
from .general.header import header
from .general.typ import typDic


def toField(n):
    if n == 1:
        return "vers"
    else:
        return f"vers{n}"


def toPart(n):
    return f"Part{int(n)}"


def grouping(subgroup, nb=0, size=10):
    partName = toPart(nb+1)
    verses = [toField(i) for i in range(size*nb+1, size*(nb+1)+1)]
    prefix = AtLeastOneField(child=hr, fields=verses)
    verses = {*verses}
    subgroup = Cascade(partName, subgroup, verses)
    return [prefix, subgroup]


prefix = TableFields(['Titre', 'Interprète', 'Auteur'])


def song(nb, nbQuestions):
    lyrics = NumberedFields(fieldPrefix="vers",
                            label="",
                            greater=nb,
                            applyToGroup=grouping,
                            groupSize=10,
                            globalFun=identity)
    if nbQuestions == 1:
        questions = frozenset({toField(nb)})
        mandatories = frozenset({toField(nb if nb % 10 != 1 else nb+1)} | {"one-line"})
        # if this part has a single line, don't generate this card since it's also the current part.
    elif nbQuestions == 2:
        assert nb >= 2
        questions = frozenset({toField(nb), toField(nb-1)})
        mandatories = frozenset({toField(nb+1 if nb % 10 != 2 else nb+1)} | {"two-lines"})
    # if this part has at most two lines, don't generate this card since it's also the current part.
    else:
        assert nbQuestions % 10 == 0
        nbParts = nbQuestions // 10
        if nbParts == 1:
            assert nb >= 10
            questions = frozenset({toPart(nb//10)})
            mandatories = frozenset({toField(nb-9 if nb != 10 else 11)})
            # if the song has a single part, don't generate this card since it's also the whole song
        elif nbParts == 2:
            assert nb >= 20
            questions = frozenset({toPart(nb//10), toPart(nb//10-1)})
            mandatories = frozenset({toField(nb-9 if nb != 20 else 21)})
            # if the song has at most two parts, don't generate this card since it's also the whole song
        elif nbParts == 20:
            assert nb >= 200
            questions = frozenset({toField(nb) for nb in range(1, 201)})
            mandatories = frozenset()
        else:
            assert False
    lyrics = lyrics.getNormalForm().assumeAsked(questions)
    r = [prefix, lyrics]
    for filled_field in mandatories:
        r = Filled(filled_field, r)
    return r
