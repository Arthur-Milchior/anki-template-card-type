from .generators.leaf import Literal, emptyGen, Field, Empty
from .config import getObject
import aqt
import json

from .generators.children import ListElement
from .generators.generators import ensureGen
from .debug import debug

from .generators.sugar.conditionals import *
from .generators.sugar.fields import *
from .generators.sugar.html import *
from .generators.child import *
from .generators.children import *
from .generators.leaf import *
from .generators.generators import ensureGen

def assertEqual(left, right):
    leftEval = eval(left)
    rightEval = eval(right)
    if leftEval == rightEval:
        return
    debug(f"{left} evaluates as {leftEval}.\n{right} evaluates as {rightEval}. They are distinct.")
    raise Exception

jsonTest = """{
    "instructions":[
        ["test", "'test'"],
        ["foo","[\\"foo\\",None, Field(\\"foo\\")]"]
    ]
}"""

model = {'sortf': 0, 'did': 1, 'latexPre': '\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n', 'latexPost': '\\end{document}', 'mod': 1544145481, 'usn': -1, 'vers': [], 'type': 0, 'css': '.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n', 'name': 'Basic', 'flds': [{'name': 'Front', 'ord': 0, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}, {'name': 'Back', 'ord': 1, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}], 'tmpls': [{'name': 'Card 1', 'ord': 0, 'qfmt': '\n <span object="test" templateversion="1">\n </span>\n', 'afmt': '\n', 'did': None, 'bqfmt': '\n', 'bafmt': '\n'}], 'tags': [], 'id': '1542656718186', 'req': [[0, 'none', []]]}

literalTest = Literal("test")
assertEqual("literalTest" , """Literal("test")""")
assertEqual("literalTest", "literalTest.getNormalForm()")
assertEqual("literalTest", "literalTest.getWithoutRedundance()")
assert not literalTest.getIsEmpty()
assert literalTest
assert literalTest !=  emptyGen
assert emptyGen !=  literalTest
assertEqual("literalTest.restrictToModel(model)", "literalTest")


literalFoo = Literal("foo")
assert literalTest != literalFoo
stringFoo = ensureGen("foo")
assertEqual("stringFoo", "literalFoo")


fieldFoo = Field("foo")
fieldFront = Field("Front")
fieldFoo_ = ensureGen(Field('foo'))
assertEqual("fieldFoo_", "fieldFoo")
assert fieldFoo  !=  Literal("test")
assert fieldFoo !=  Literal("{{foo}}")
assertEqual("fieldFoo", "Field('foo')")
assertEqual("fieldFoo", "fieldFoo.getNormalForm()")
assertEqual("fieldFoo", "fieldFoo.getWithoutRedundance()")
assert not fieldFoo.getIsEmpty()
assert fieldFoo.getToKeep()
assert fieldFoo
assertEqual("fieldFoo.restrictToModel(model)", "emptyGen")
assertEqual("fieldFront.restrictToModel(model)", "fieldFront")


none = ensureGen(None)
assertEqual("none", "emptyGen")
assertEqual("none", "none.getNormalForm()")
assertEqual("none", "none.getWithoutRedundance()")
assert none.getIsEmpty()
assert not none.getToKeep()
assert not none
assertEqual("emptyGen", "Empty()")


foofoo = ListElement([literalFoo,emptyGen,fieldFoo])
foofront = ListElement([literalFoo,emptyGen,fieldFront])
foofoo_ = ensureGen(["foo",emptyGen,fieldFoo])
assert foofoo
assert foofoo.getToKeep()
assert not foofoo.getIsEmpty()
assertEqual("foofoo", "foofoo_")
foofooNormal = foofoo.getNormalForm()
foofooNormal = foofoo.getWithoutRedundance()
assertEqual("foofoo", "foofooNormal")
assertEqual("foofoo.restrictToModel(model)", "literalFoo")
assertEqual("foofront.restrictToModel(model)", "foofront")

# fooList = ensureGen([Field('foo')])
# print(f"ensureGen([Field('foo')]) is {fooList!r}")
# assert fooList ,  ListElement([Field("foo")]))


objects = dict()
userOption = json.loads(jsonTest)
instructions = userOption.get("instructions", [])
for instruction in instructions:
    if isinstance(instruction,list):
        (name,value) = instruction
        #debug(f"""Evaluating "{name}" as "{value}" of type {type(value)}.""")
        objects[name] =  ensureGen(eval(value,globals(), objects))
    elif isinstance(instruction,str):
        exec(instruction,globals(), objects)
    else:
        assert False
test = objects["test"]
assert test == literalTest
assert test == test.getNormalForm()
assert test == test.getWithoutRedundance()

# test = getObject("test")
# assert test == Literal("test")
# assert test == test.getNormalForm()
# assert test == test.getWithoutRedundance()

# config._set("bar",emptyGen)
# assert config.objects["bar"] == emptyGen
# evaluate("t= 4")
# assert t==4
# define ("bar","'foo'")
# assert config.get("bar")== Literal("foo")
# define ("bar","['foo','foo']")
# assert config.get("bar")== ListElement([Literal("foo"),Literal("foo")])

