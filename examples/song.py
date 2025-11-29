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


one_line_warning = Filled("one-line", Empty("two-lines", "One-line is filled, please filled two-lines"))
two_line_warning = Filled("two-line", Empty("one paragraph", "two-lines is filled, please filled one paragraph"))

warning = [one_line_warning, two_line_warning]
prefix = TableFields(['Titre', 'Interprète', 'Auteur'])

def song(numberOfShownLines, numberOfAskedLines):
    """
    `numberOfShownLines` - the number of verse shown in the answer.
    `numberOfAskedLines`: the number of lines to hide in question with ???
    """
    assert numberOfShownLines >= numberOfAskedLines
    lyrics = NumberedFields(fieldPrefix="vers",
                            label="",
                            greater=numberOfShownLines,
                            applyToGroup=grouping,
                            groupSize=10,
                            globalFun=identity)
    # We are setting `questions` and `mandatories`
    if numberOfAskedLines == 1:
        questions = frozenset({toField(numberOfShownLines)})
        if numberOfShownLines % 10 == 1:
            # The question is the first line of the paragraph.
            # We should check the paragraph is not a single line long. That is, the second line is filled. It should imply current line is also filled.
            mandatoryLineIndex = numberOfShownLines+1
            mandatoryRestriction = "two-lines"
        else:
            # Just check this line exists.
            mandatoryLineIndex = numberOfShownLines
            mandatoryRestriction = "one-line"
        mandatories = frozenset({toField( mandatoryLineIndex )} | {mandatoryRestriction})
        # if this part has a single line, don't generate this card since it's also the current part.
    elif numberOfAskedLines == 2:
        assert numberOfShownLines >= 2
        if numberOfShownLines % 10 == 1:
            #the question is the first line of the paragraph. Hard to ask the last filled line, so let's go with last paragraph.
            partOfLastShownLines = numberOfShownLines // 10 # eg. last shown lines is 21, part is 2.
            questions = frozenset({toField(numberOfShownLines), toPart(partOfLastShownLines - 1)})
            # also, let's check the paragraph has another element in in.
            mandatoryLineIndex = numberOfShownLines+1
        else:
            if numberOfShownLines % 10 == 2:
                # The question is the second line of the paragraph.
                # We should check the paragraph is at least three lines long. That is, the third line is filled. It should imply two first lines are also filled.
                mandatoryLineIndex = numberOfShownLines+1
            else:
                # Just check this line exists.
                mandatoryLineIndex = numberOfShownLines
            questions = frozenset({toField(numberOfShownLines), toField(numberOfShownLines-1)})
        mandatories = frozenset({toField(mandatoryLineIndex)} | {"two-lines"})
    else:
        assert numberOfAskedLines % 10 == 0
        assert numberOfShownLines % 10 == 0
        numberOfAskedParagraphs = numberOfAskedLines // 10
        numberOfShownParagraphs = numberOfShownLines // 10
        if numberOfAskedParagraphs == 1:
            questions = frozenset({toPart(numberOfShownLines//10)})
            if numberOfShownParagraphs == 1:
                # If we ask to show the first paragraph, request the existence of paragraph two, to ensure this card is not the same as total
                mandatoryLineIndex = 11
                mandatoryRestriction = frozenset()
            else:
                mandatoryLineIndex = numberOfShownLines - 9 # Eg, if we show 30 lines, we request line 21
                mandatoryRestriction = {"one paragraph"}
            mandatories = frozenset({toField(mandatoryLineIndex)}) | mandatoryRestriction
            # if the song has a single part, don't generate this card since it's also the whole song
        elif numberOfAskedParagraphs == 2:
            assert numberOfShownLines >= 20
            questions = frozenset({toPart(numberOfShownLines//10), toPart(numberOfShownLines//10-1)})
            if numberOfShownParagraphs == 1:
                # If we ask to show the first two paragraphes, request the existence of paragraph three, to ensure this card is not the same as total
                mandatoryLineIndex = 21
            else:
                mandatoryLineIndex = numberOfShownLines - 9 # Eg, if we show 30 lines, we request line 21
            mandatories = frozenset({toField(mandatoryLineIndex)})
            # if the song has at most two parts, don't generate this card since it's also the whole song
        elif numberOfAskedParagraphs == 20:
            # We show the entire song
            assert numberOfShownLines >= 200
            questions = frozenset({toField(numberOfShownLines) for numberOfShownLines in range(1, 201)})
            mandatories = frozenset()
        else:
            assert False
    lyrics = lyrics.getNormalForm().assumeAsked(questions)
    r = [prefix, lyrics]
    for filled_field in mandatories:
        r = Filled(filled_field, r)
    return [warning, r]
