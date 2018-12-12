from ..imports import *

literalTest = Literal("test")
literalFoo = Literal("foo")
fieldFoo = Field("foo")
fieldFront = Field("Question")
fieldFoo_ = ensureGen(Field('foo'))
none = ensureGen(None)
foofoo = ListElement([literalFoo,emptyGen,fieldFoo])
foofront = ListElement([literalFoo,emptyGen,fieldFront])
fooList = ensureGen([Field('foo')])
