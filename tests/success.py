print("Testing")
from .imports import *

literalTest = Literal("test")
assert assertEqual("literalTest" , """Literal("test")""")
assert assertEqual("literalTest", "literalTest.getNormalForm()")
assert assertEqual("literalTest", "literalTest.getWithoutRedundance()")
assert not literalTest.getIsEmpty()
assert literalTest
assert literalTest !=  emptyGen
assert emptyGen !=  literalTest
assert assertEqual("literalTest.restrictToModel(model)", "literalTest")


literalFoo = Literal("foo")
assert literalTest != literalFoo
stringFoo = ensureGen("foo")
assert assertEqual("stringFoo", "literalFoo")


fieldFoo = Field("foo")
fieldFront = Field("FrontField")
fieldFoo_ = ensureGen(Field('foo'))
assert assertEqual("fieldFoo_", "fieldFoo")
assert fieldFoo  !=  Literal("test")
assert fieldFoo !=  Literal("{{foo}}")
assert assertEqual("fieldFoo", "Field('foo')")
assert assertEqual("fieldFoo", "fieldFoo.getNormalForm()")
assert assertEqual("fieldFoo", "fieldFoo.getWithoutRedundance()")
assert not fieldFoo.getIsEmpty()
assert fieldFoo.getToKeep()
assert fieldFoo
assert assertEqual("fieldFoo.restrictToModel(model)", "emptyGen")
assert assertEqual("fieldFront.restrictToModel(model)", "fieldFront")


none = ensureGen(None)
assert assertEqual("none", "emptyGen")
assert assertEqual("none", "none.getNormalForm()")
assert assertEqual("none", "none.getWithoutRedundance()")
assert none.getIsEmpty()
assert not none.getToKeep()
assert not none
assert assertEqual("emptyGen", "Empty()")


foofoo = ListElement([literalFoo,emptyGen,fieldFoo])
foofront = ListElement([literalFoo,emptyGen,fieldFront])
foofoo_ = ensureGen(["foo",emptyGen,fieldFoo])
assert foofoo
assert foofoo.getToKeep()
assert not foofoo.getIsEmpty()
assert assertEqual("foofoo", "foofoo_")
foofooNormal = foofoo.getNormalForm()
foofooNormal = foofoo.getWithoutRedundance()
assert assertEqual("foofoo", "foofooNormal")
assert assertEqual("foofoo.restrictToModel(model)", "literalFoo")
assert assertEqual("foofront.restrictToModel(model)", "foofront")

fooList = ensureGen([Field('foo')])
assert fooList


testObjects = dict()
userOption = json.loads(jsonTest)
instructions = userOption.get("instructions", [])
for instruction in instructions:
    if isinstance(instruction,list):
        (name,value) = instruction
        #debug(f"""Evaluating "{name}" as "{value}" of type {type(value)}.""")
        testObjects[name] =  ensureGen(eval(value,globals(), testObjects))
    elif isinstance(instruction,str):
        exec(instruction,globals(), testObjects)
    else:
        assert False
test = testObjects["test"]
assert assertEqual("test", "literalTest")
assert assertEqual("test", "test.getNormalForm()")
assert assertEqual("test", "test.getWithoutRedundance()")


#########HTML
noHtml = "foo1"
assert assertEqual("templateFromSoup(soupFromTemplate(noHtml))","noHtml")

noTemplate = """<p>
 foo2
</p>"""
soupNo = soupFromTemplate(noTemplate)
assert assertEqual("""templateFromSoup(soupNo,prettify = True)""","""noTemplate""")
assert assertEqual("tagsToEdit(soupNo)","[]")
compile_(soupNo, soup = soupNo, isQuestion = True, model = model, objects = testObjects)
assert assertEqual("""templateFromSoup(soupNo,prettify = True)""","""noTemplate""")


htmlTest = """<span object="test" template="object">
 foo4
</span>"""
soupTest = soupFromTemplate(htmlTest)
assert assertEqual("""templateFromSoup(soupTest,prettify = True)""","""htmlTest""")
assert assertEqual("len(tagsToEdit(soupTest))","1")
compile_(soupTest.span, soup = soupTest, isQuestion = True, model = model, objects = testObjects, recompile = True)
htmlTestCompiled = """<span object="test" template="object">
 test
</span>"""
assert assertEqual("""templateFromSoup(soupTest,prettify = True)""","""htmlTestCompiled""")
soupTest = soupFromTemplate(htmlTest)
compile_(soupTest, soup = soupTest, isQuestion = True, model = model, objects = testObjects)
assert assertEqual("""templateFromSoup(soupTest,prettify = True)""","""htmlTestCompiled""")

htmlBar = """<span object="bar" template="object">
 foo5
</span>"""
soupBar = soupFromTemplate(htmlBar)
assert assertEqual("""templateFromSoup(soupBar,prettify = True)""","""htmlBar""")
assert assertEqual("len(tagsToEdit(soupBar))","1")
compile_(soupBar.span, soup = soupBar, isQuestion = True, model = model, objects = testObjects, recompile = True)
htmlBarCompiled = """<span object="bar" objectabsent="bar" template="object">
</span>"""
assert assertEqual("""templateFromSoup(soupBar,prettify = True)""","""htmlBarCompiled""")
soupBar = soupFromTemplate(htmlBar)
compile_(soupBar, soup = soupBar, isQuestion = True, model = model, objects = testObjects)
assert assertEqual("""templateFromSoup(soupBar,prettify = True)""","""htmlBarCompiled""")


htmlFoo = """<span object="foo" template="object">
</span>"""
soupFoo = soupFromTemplate(htmlFoo)
assert assertEqual("""templateFromSoup(soupFoo,prettify = True)""","""htmlFoo""")
assert assertEqual("len(tagsToEdit(soupFoo))","1")
compile_(soupFoo.span, soup = soupFoo, isQuestion = True, model = model, objects = testObjects, recompile = True)
htmlFooCompiled = """<span object="foo" template="object">
 foo
 {{FrontField}}
</span>"""
assert assertEqual("""templateFromSoup(soupFoo,prettify = True)""","""htmlFooCompiled""")
soupFoo = soupFromTemplate(htmlFoo)
compile_(soupFoo, soup = soupFoo, isQuestion = True, model = model, objects =testObjects)
assert assertEqual("""templateFromSoup(soupFoo,prettify = True)""","""htmlFooCompiled""")

htmlFront = """<span template="Front Side">
</span>"""
soupFront = soupFromTemplate(htmlFront)
assert assertEqual("""templateFromSoup(soupFront,prettify = True)""","""htmlFront""")
assert assertEqual("len(tagsToEdit(soupFoo))","1")
compile_(soupFront.span, soup = soupFront, isQuestion = True, model = model, objects = testObjects, FrontSoup = soupTest, recompile = True)
htmlFrontCompiled = """<span template="Front Side">
</span>"""


###
modelCompiled = compileModel(model, objects = testObjects, prettify = True)
print(modelCompiled)
assert assertEqual("modelCompiled['tmpls'][0]['qfmt']","htmlTestCompiled")
htmlAnswerTestCompiled = """<span template="Front Side">
 <span object="test" template="object">
  test
 </span>
</span>"""
assert assertEqual("modelCompiled['tmpls'][0]['afmt']","htmlAnswerTestCompiled")
htmlFrontFieldCompiledBack = """<span template="Front Side">
 <span object="FrontField" template="object">
  {{FrontField}}
 </span>
</span>"""
htmlFrontFieldCompiledFront = """<span object="FrontField" template="object">
 ???
</span>"""
assert assertEqual("modelCompiled['tmpls'][1]['qfmt']","htmlFrontFieldCompiledFront")
#assert assertEqual("modelCompiled['tmpls'][1]['afmt']","htmlAnswerTestCompiled")


####################
# config

readIfRequired()
# print(objects)


# test = getObject("test")
# assert assertEqual(" test ", "Literal("test")")
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

