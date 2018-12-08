from .generators.leaf import Literal, emptyGen, Field, Empty
from .config import getObject
import aqt
import json
from copy import copy

from .editTemplate import soupFromTemplate, templateFromSoup, tagsToEdit, _templateTagAddText

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
    debug(f"""{left} evaluates as \n"{leftEval}".\n"{rightEval}"\n is the value of {right}, they are distinct.""")
    raise Exception

jsonTest = """{
    "instructions":[
        ["test", "'test'"],
        ["foo","[\\"foo\\",None, Field(\\"Front\\")]"]
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

fooList = ensureGen([Field('foo')])
assert fooList


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
assertEqual("test", "literalTest")
assertEqual("test", "test.getNormalForm()")
assertEqual("test", "test.getWithoutRedundance()")


#########HTML
noHtml = "foo1"
assertEqual("templateFromSoup(soupFromTemplate(noHtml))","noHtml")

noTemplate = """<p>foo2</p>"""
soupNo = soupFromTemplate(noTemplate)
assertEqual("""templateFromSoup(soupNo,prettify = False)""","""noTemplate""")
assertEqual("len(tagsToEdit(soupNo))","0")
_templateTagAddText(soupNo.p, soupNo, True, model, objects, recompile = True)

htmlTest = """<span object="test" templateversion="1">foo4</span>"""
soupTest = soupFromTemplate(htmlTest)
assertEqual("""templateFromSoup(soupTest,prettify = False)""","""htmlTest""")
assertEqual("len(tagsToEdit(soupTest))","1")
_templateTagAddText(soupTest.span, soupTest, True, model, objects, recompile = True)
htmlTestCompiled = """<span object="test" templateversion="1">test</span>"""
assertEqual("""templateFromSoup(soupTest,prettify = False)""","""htmlTestCompiled""")

htmlBar = """<span object="bar" templateversion="1">foo5</span>"""
soupBar = soupFromTemplate(htmlBar)
assertEqual("""templateFromSoup(soupBar,prettify = False)""","""htmlBar""")
assertEqual("len(tagsToEdit(soupBar))","1")
_templateTagAddText(soupBar.span, soupBar, True, model, objects, recompile = True)
htmlBarCompiled = """<span object="bar" objectabsent="bar" templateversion="1"></span>"""
assertEqual("""templateFromSoup(soupBar,prettify = False)""","""htmlBarCompiled""")

htmlFoo = """<span object="foo" templateversion="1"></span>"""
soupHtml = soupFromTemplate(htmlFoo)
assertEqual("""templateFromSoup(soupHtml,prettify = False)""","""htmlFoo""")
assertEqual("len(tagsToEdit(soupHtml))","1")
_templateTagAddText(soupHtml.span, soupHtml, True, model, objects, recompile = True)
htmlFooCompiled = """<span object="foo" templateversion="1">foo{{Front}}</span>"""
assertEqual("""templateFromSoup(soupHtml,prettify = False)""","""htmlFooCompiled""")



# test = getObject("test")
# assertEqual(" test ", "Literal("test")")
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

