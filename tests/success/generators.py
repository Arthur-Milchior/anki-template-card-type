# List of templates which must be equals

from ..imports import *
from ..data import *

# Leaf

## Empty
assert assertEqual("none", "emptyGen")
assert assertEqual("none", "none.getNormalForm()")
assert assertEqual("none", "none.getWithoutRedundance()")
assert none.isEmpty()
assert not none.toKeep
assert not none
assert assertEqual("emptyGen", "Empty(createOther = True)")
assert none == ensureGen(None)

## Literal
assert assertEqual("literalTest" , """Literal("test")""")
assert assertEqual("literalTest", "literalTest.getNormalForm()")
assert assertEqual("literalTest", "literalTest.getWithoutRedundance()")
assert not literalTest.isEmpty()
assert literalTest
assert literalTest !=  emptyGen
assert emptyGen !=  literalTest
assert assertEqual("literalTest.restrictToModel(model)", "literalTest")
assert literalTest != literalFoo
stringFoo = ensureGen("foo")
assert assertEqual("stringFoo", "literalFoo")

## Field 
assert assertEqual("fieldFoo_", "fieldFoo")
assert fieldFoo  !=  Literal("test")
assert fieldFoo !=  Literal("{{foo}}")
assert assertEqual("fieldFoo", "Field('foo')")
assert assertEqual("fieldFoo", "fieldFoo.getNormalForm()")
assert assertEqual("fieldFoo", "fieldFoo.getWithoutRedundance()")
assert not fieldFoo.isEmpty()
assert fieldFoo.toKeep
assert fieldFoo
assert assertEqual("fieldFoo.restrictToModel(model)", "emptyGen")
assert assertEqual("fieldQuestion.restrictToModel(model)", "fieldQuestion")

# singleChild
assert assertEqual("contradictionRequirement.getNormalForm()", "emptyGen")



foofoo_ = ensureGen(["foo",emptyGen,fieldFoo])
assert foofoo
assert foofoo.toKeep is not False
assert not foofoo.isEmpty()
assert assertEqual("foofoo.force()", "foofoo_.force()")
foofooNormal = foofoo.getNormalForm()
foofooWR = foofoo.getWithoutRedundance()
assert assertEqual("foofoo.force()", "foofooNormal.force()")
assert assertEqual("foofoo.force()", "foofooWR.force()")
assert assertEqual("foofoo.restrictToModel(model)", "literalFoo")
assert assertEqual("fooQuestion.restrictToModel(model)", "fooQuestion")
assert fooList


test = testObjects["test"]
assert assertEqual("test", "literalTest")
assert assertEqual("test", "test.getNormalForm()")
assert assertEqual("test", "test.getWithoutRedundance()")

assert assertEqual("branch", "questionnedField")

