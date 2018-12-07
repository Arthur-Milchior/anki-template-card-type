from .generators.leaf import Literal, emptyGen, Field
from .config import objects, _set, get
from .generators.children import ListElement

assert  Literal("test") ==  Literal("test")
assert  Literal("test") !=  Literal("foo")
assert  Literal("test") !=  emptyGen
assert  Field("test") !=  Literal("test")

t = get("test")
assert t == Literal("test")
_set("bar",emptyGen)
assert objects["bar"] == emptyGen
evaluate("t= 4")
assert t==4
define ("bar","'foo'")
assert get("bar")== Literal("foo")
define ("bar","['foo','foo']")
assert get("bar")== ListElement([Literal("foo"),Literal("foo")])
