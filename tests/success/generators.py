from ..imports import *
from ..data import *

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
assert assertEqual("fieldFront.restrictToModel(model)", "fieldFront")



assert assertEqual("none", "emptyGen")
assert assertEqual("none", "none.getNormalForm()")
assert assertEqual("none", "none.getWithoutRedundance()")
assert none.isEmpty()
assert not none.toKeep
assert not none
assert assertEqual("emptyGen", "Empty(createOther = True)")


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
assert assertEqual("foofront.restrictToModel(model)", "foofront")
assert fooList


test = testObjects["test"]
assert assertEqual("test", "literalTest")
assert assertEqual("test", "test.getNormalForm()")
assert assertEqual("test", "test.getWithoutRedundance()")


# decoratedField = DecoratedField("FrontField")
# #debug(f"""decorated: {decoratedField}""")
# normal = decoratedField.getNormalForm()
# #debug(f"""normal: {normal}""")
# withoutRedundance = normal.getWithoutRedundance()
# #debug(f"""withoutRedundance: {withoutRedundance}""")
# #debug("Compute restriction")
# modelApplied = withoutRedundance.restrictToModel(model)
# #debug(f"""modelApplied: {modelApplied}""")
