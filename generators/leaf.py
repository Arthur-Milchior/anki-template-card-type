import copy
import sys
import types

from bs4 import NavigableString

from ..debug import ExceptionInverse, assertType, debug, debugFun, debugInit
from .constants import *
from .ensureGen import addTypeToGenerator
from .generators import Gen, genRepr, thisClassIsClonable
from .html.html import CLASS


class Leaf(Gen):
    """
    The class of generators with no child.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @debugFun
    def _getChildren(self):
        return frozenset()

    @debugFun
    def clone(self, elements=[]):
        assert elements == []
        return self

    def _firstDifference(self, other):
        return None

    def _innerEq(self, other):
        return True


emptyGen = None
@thisClassIsClonable
class NoContent(Leaf):
    """A generator without any content"""
    instance = None

    def __hash__(self):
        return 0

    def __init__(self,
                 *args,  # required, because EnsureGen may give an argument
                 toKeep=False,
                 state=EMPTY,
                 createOther=False,
                 init=None,
                 **kwargs):
        if createOther:
            pass
        elif NoContent.instance is None and init:
            NoContent.instance = self
        else:
            raise ExceptionInverse("Calling NoContent")
        super().__init__(state=state,
                         toKeep=toKeep,
                         **kwargs)

    def _repr(self):
        if self == emptyGen:
            return "emptyGen"
        else:
            return f"""NoContent(createOther = True,{self.params()})"""

    def _createHtml(self, soup):
        return None

    def _outerEq(self, other):
        #debug("{self!r} == {other!r}",1)
        l = isinstance(other, NoContent)
        # if l:
        #debug("other is NoContent")
        # else:
        #debug("other is not NoContent but {type(other)}")
        # debug("",-1)
        return l


noContentGen = NoContent(init=True)


def constNoContent(x):
    return noContentGen


addTypeToGenerator(type(None), constNoContent)


@thisClassIsClonable
class Literal(Leaf):
    """A text to be printed, as-is, unconditionally."""

    def __init__(self,
                 text=None,
                 state=LAST_GEN_STEP,
                 **kwargs):
        assert assertType(text, str)
        if text is None:
            text = ""
        self.text = text
        if not self.text:
            state == EMPTY
        super().__init__(state=state,
                         **kwargs)

    def __hash__(self):
        return hash(self.text)

    def _repr(self):
        return f"""Literal(text = "{self.text}",{self.params()})"""

    def _outerEq(self, other):
        if not isinstance(other, Literal):
            return False
        return self.text == other.text

    def _createHtml(self, soup):
        return NavigableString(self.text)


addTypeToGenerator(str, Literal)


@thisClassIsClonable
class Field(Leaf):
    """Representation of a field.

    keywords parameter:
    field -- The name of the field
    typ -- Whether "type:" should be prefixed. It has some special signification in anki
    cloze -- Whether "cloze:" should be prefixed. It has some special signification in anki
    isMandatory -- Show an error message if this field is used in a model where this field is not present. By default its false
    useClasses -- Whether some class should be applied to the field
"""

    def __init__(self,
                 field,
                 typ=False,
                 cloze=False,
                 state=WITHOUT_REDUNDANCY,
                 special=False,
                 isMandatory=False,
                 useClasses=True,
                 toKeep=True,
                 classes=None,
                 **kwargs):
        if special and isMandatory:
            print(
                f"""Beware: you stated that a special field {field} is isMandatory, it makes no sens.""", file=sys.stderr)
        self.isMandatory = isMandatory
        self.useClasses = useClasses or (classes is not None)
        self.classes = classes if (classes is not None) else field
        self.special = special
        self.typ = typ
        self.cloze = cloze
        if isinstance(field, Field):
            self.field = field.field
        # required so that {{foo}} becomes Field(foo)
        elif isinstance(field, set):
            assert len(field) == 1
            self.field = field.pop()
            field.add(self.field)
        else:
            self.field = field
        assert assertType(self.field, str)
        self.dealWithClozeAndType()
        self.dealWithSpecial()
        super().__init__(state=state,
                         toKeep=toKeep,
                         localMandatories={
                             self.field} if isMandatory else frozenset(),
                         **kwargs)

    def dealWithClozeAndType(self):
        if self.field.startswith("type:"):
            print(f"""Beware: you used "type:" in prefix of your field name. Please use "typ= True" in the Field object creator instead. "type:" is removed from the name.""", file=sys.stderr)
            self.typ = True
            self.field = self.field[5:]
        if self.field.startswith("cloze:"):
            print(f"""Beware: you used "cloze:" in prefix of your field name. Please use "cloze= True" in the Field object creator instead. "cloze:" is removed from the name.""", file=sys.stderr)
            self.cloze = True
            self.field = self.field[6:]

    def dealWithSpecial(self):
        specialName = {"FrontSide": "frontside", "Tags": "tags",
                       "Type": "typ", "Deck": "deck", "Card": "card"}
        if self.field in specialName and not self.special:
            print(
                f"""Beware: you use field "{self.field}", which is a special field. If you want to use this special field, use the constant "{[self.field]}".""", file=sys.stderr)
        if not self.special and self.field in specialName:
            print(
                f"""Beware: you want to create a special field "{self.field}", which does not belong to {specialName}, thus is not a special name.""", file=sys.stderr)
        if self.special:
            if self.typ:
                print(
                    f"""Beware: you want to have "type:" before a special field {self.field}, this makes no sens.""", file=sys.stderr)
            if self.cloze:
                print(
                    f"""Beware: you want to have "cloze:" before a special field {self.field}, this makes no sens.""", file=sys.stderr)

    def _getNormalForm(self):
        if self.useClasses:
            return CLASS(self.classes,
                         Field(self.field,
                               typ=self.typ,
                               cloze=self.cloze,
                               special=self.special,
                               isMandatory=self.isMandatory,
                               useClasses=False))
        else:
            return self

    def __hash__(self):
        return hash(self.field)

    def _outerEq(self, other):
        return isinstance(other, Field) and self.field == other.field and self.useClasses == other.useClasses and super()._outerEq(other)

    def _repr(self):
        t = f"""Field(field = "{self.field}","""
        if self.typ is not False:
            t += "\n"+genRepr(self.typ, label="type")+","
        if self.cloze is not False:
            t += "\n"+genRepr(self.cloze, label="cloze")+","
        if self.special is not False:
            t += "\n"+genRepr(self.special, label="special")+","
        if self.isMandatory is not False:
            t += "\n"+genRepr(self.isMandatory, label="isMandatory")+","
        if self.useClasses is not True:
            t += "\n"+genRepr(self.useClasses, label="useClasses")+","
        t += self.params()+")"
        return t

    def _assumeFieldEmpty(self, fields, setForbiddenState):
        if self.field in fields:
            if self.special:
                print(
                    f"""Beware: you assert that special name {self.field} is empty, which makes no sens.""", file=sys.stderr)
            return emptyGen
        else:
            return self

    def _assumeFieldAbsent(field):
        if field == self.field:
            if self.special:
                print(
                    f"""Beware: you assert that special name {self.field} is absent, which makes no sens.""", file=sys.stderr)
            return emptyGen
        else:
            return self

    @debugFun
    def _restrictToModel(self, fields):
        if self.field in fields:
            if self.special:
                print(
                    f"""Beware: your model has a field {self.field} which is also the name of a special field.""", file=sys.stderr)
            return self
        else:
            if self.special:
                return self
            else:
                return emptyGen

    def _createHtml(self, *args, **kwargs):
        typ = "type:" if self.typ else ""
        cloze = "cloze:" if self.cloze else ""
        return NavigableString(f"""{{{{{typ}{cloze}{self.field}}}}}""")


addTypeToGenerator(set, Field)
frontside = Field("FrontSide", special=True)
tags = Field("Tags", special=True)
typ = Field("Type", special=True)
deck = Field("Deck", special=True)
card = Field("Card", special=True)
