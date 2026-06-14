from typing import Optional

from .util import numbered_field
from ..generators import *
from .general.footer import footer
from .general.header import header
from .general.typ import typDic
from ..generators.html.atom import *


def toPart(n):
    """The name of the i-th part. For cascading purpose."""
    return f"Part{int(n)}"


def grouping(subgroup, nb=0,numberOfGroup: Optional[None]= None,size=10):
    """The generator for the `nb`-th group."""
    partName = toPart(nb+1)
    verses = [numbered_field("vers", i) for i in range(size*nb+1, size*(nb+1)+1)]
    is_last_group = nb == numberOfGroup-1
    separator = hr_answer if is_last_group else hr 
    prefix = Filled(verses[0], separator)
    verses = {*verses}
    subgroup = Cascade(partName, subgroup, verses)
    return [prefix, subgroup]


one_line_warning = Filled("one-line", Empty("two-lines", "One-line is filled, please filled two-lines"))
two_line_warning = Filled("two-line", Empty("one paragraph", "two-lines is filled, please filled one paragraph"))

prefix = TableFields(['Titre', 'Interprète', 'Auteur'])


class MandatoryFieldTree:
    def encapsulateGenerator(self, gen_true, gen_false=emptyGen):
        raise NotImplementedError()

class MandatoryFieldLeaf(MandatoryFieldTree):
    def __init__(self, field):
        self.field = field

    def encapsulateGenerator(self, gen_true, gen_false=emptyGen):
        return FilledOrEmpty(self.field, gen_true, gen_false)

class MandatoryFieldOr(MandatoryFieldTree):
    def __init__(self, *children):
        self.children = children

    def encapsulateGenerator(self, gen_true, gen_false=emptyGen):
        gen = gen_false
        for child in self.children:
            gen = child.encapsulateGenerator(gen_true, gen)
        return gen

class MandatoryFieldAnd(MandatoryFieldTree):
    def __init__(self, *children):
        self.children = children

    def encapsulateGenerator(self, gen_true, gen_false=emptyGen):
        gen = gen_true
        for child in self.children:
            gen = child.encapsulateGenerator(gen, gen_false)
        return gen
    
class MandatoryFieldTrue(MandatoryFieldTree):
    def encapsulateGenerator(self, gen_true, gen_false=emptyGen):
        return gen_true

def missing_previous(line):
    """If line is present but not the previous expected line, warn."""
    if line == 1:
        return emptyGen
    
    if line % 10 == 1:
        expectedLine = line - 10
    else:
        expectedLine = line - 1
    return Filled(numbered_field("vers", line), Empty(numbered_field("vers", expectedLine), f"Line {line} is filled, please fill line {expectedLine}"))
            


def song(indexOfTheLastAskedLine, numberOfAskedLines):
    """
    `numberOfShownLines` - the number of lines shown in the answer.
    `numberOfAskedLines`: the number of lines to hide in question with ???
    """
    assert indexOfTheLastAskedLine >= numberOfAskedLines
    indexOfTheFirstAskedLine = indexOfTheLastAskedLine-numberOfAskedLines+1
    

    lyrics = NumberedFields(fieldPrefix="vers",
                            label="",
                            greater=indexOfTheLastAskedLine,
                            numbered_field=numbered_field,
                            applyToGroup=grouping,
                            groupSize=10,
                            globalFun=identity)
    # We are setting `questions` and `mandatories`
    if numberOfAskedLines == 1:
        questions = frozenset({numbered_field("vers", indexOfTheLastAskedLine)})
        if indexOfTheLastAskedLine % 10 == 1:
            # The question is the first line of the paragraph.
            # We should check the paragraph is not a single line long. That is, the second line is filled. It should imply current line is also filled.
            mandatoryLineIndex = indexOfTheLastAskedLine+1
            mandatoryRestriction = "two-lines"
        else:
            # Just check this line exists.
            mandatoryLineIndex = indexOfTheLastAskedLine
            mandatoryRestriction = "one-line"
        mandatories = MandatoryFieldAnd(
            MandatoryFieldLeaf(numbered_field("vers",  mandatoryLineIndex )) , 
             MandatoryFieldOr(MandatoryFieldLeaf(mandatoryRestriction), 
                               MandatoryFieldLeaf(f"Focus {indexOfTheLastAskedLine}")))
        # if this part has a single line, don't generate this card since it's also the current part.
    elif numberOfAskedLines == 2:
        assert indexOfTheLastAskedLine >= 2
        if indexOfTheLastAskedLine % 10 == 1:
            #the question is the first line of the paragraph. Hard to ask the last filled line, so let's go with last paragraph.
            partOfLastShownLines = indexOfTheLastAskedLine // 10 # eg. last shown lines is 21, part is 2.
            questions = frozenset({numbered_field("vers", indexOfTheLastAskedLine), toPart(partOfLastShownLines - 1)})
            # also, let's check the paragraph has another element in in.
            mandatoryLineIndex = indexOfTheLastAskedLine+1
        else:
            if indexOfTheLastAskedLine % 10 == 2:
                # The question is the second line of the paragraph.
                # We should check the paragraph is at least three lines long. That is, the third line is filled. It should imply two first lines are also filled.
                mandatoryLineIndex = indexOfTheLastAskedLine+1
            else:
                # Just check this line exists.
                mandatoryLineIndex = indexOfTheLastAskedLine
            questions = frozenset({numbered_field("vers", indexOfTheLastAskedLine), numbered_field("vers", indexOfTheLastAskedLine-1)})
        mandatories = MandatoryFieldAnd(MandatoryFieldLeaf(numbered_field("vers", mandatoryLineIndex)),
                                        MandatoryFieldOr(MandatoryFieldLeaf("two-lines"), 
                                                         MandatoryFieldLeaf(f"Focus {indexOfTheLastAskedLine}")))
    else:
        assert numberOfAskedLines % 10 == 0
        assert indexOfTheLastAskedLine % 10 == 0
        numberOfAskedParagraphs = numberOfAskedLines // 10
        numberOfShownParagraphs = indexOfTheLastAskedLine // 10
        if numberOfAskedParagraphs == 1:
            questions = frozenset({toPart(indexOfTheLastAskedLine//10)})
            if numberOfShownParagraphs == 1:
                # If we ask to show the first paragraph, request the existence of paragraph two, to ensure this card is not the same as total
                mandatoryLineIndex = 11
                mandatoryRestriction = MandatoryFieldTrue()
            else:
                mandatoryLineIndex = indexOfTheLastAskedLine - 9 # Eg, if we show 30 lines, we request line 21
                mandatoryRestriction = MandatoryFieldLeaf("one paragraph")
            mandatories = MandatoryFieldAnd(MandatoryFieldLeaf(numbered_field("vers", mandatoryLineIndex)),
                                             mandatoryRestriction)
            # if the song has a single part, don't generate this card since it's also the whole song
        elif numberOfAskedParagraphs == 2:
            assert indexOfTheLastAskedLine >= 20
            questions = frozenset({toPart(indexOfTheLastAskedLine//10), toPart(indexOfTheLastAskedLine//10-1)})
            if numberOfShownParagraphs == 1:
                # If we ask to show the first two paragraphes, request the existence of paragraph three, to ensure this card is not the same as total
                mandatoryLineIndex = 21
            else:
                mandatoryLineIndex = indexOfTheLastAskedLine - 9 # Eg, if we show 30 lines, we request line 21
            mandatories = MandatoryFieldLeaf(numbered_field("vers", mandatoryLineIndex))
            # if the song has at most two parts, don't generate this card since it's also the whole song
        elif numberOfAskedParagraphs == 20:
            # We show the entire song
            assert indexOfTheLastAskedLine >= 200
            questions = frozenset({numbered_field("vers", numberOfShownLines) for numberOfShownLines in range(1, 201)})
            mandatories = MandatoryFieldTrue()
        else:
            assert False
    lyrics = lyrics.getNormalForm().assumeAsked(questions)
    r = [prefix, lyrics]
    r = mandatories.encapsulateGenerator(r)
    return [missing_previous(indexOfTheFirstAskedLine), one_line_warning, two_line_warning, r]
