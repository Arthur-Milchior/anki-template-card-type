from ..generators import *
from .general.foot import footer
from .general.head import header
from .general.typ import typDic

def toField(n):
    if n==1:
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
    elif nbQuestions == 2:
        questions = frozenset({toField(nb), toField(nb-1)})
    else:
        assert nbQuestions % 10 ==0
        nbParts = nbQuestions // 10
        if nbParts == 1:
            questions = frozenset({toPart(nb//10)})
        elif nbParts == 2:
            questions = frozenset({toPart(nb//10), toPart(nb//10-1)})
        elif nbParts == 20:
            questions = frozenset({toPart(nb) for nb in range(1,21)})
        else:
            assert False
    lyrics = lyrics.getNormalForm().assumeAsked(questions)
    return [prefix, lyrics]
