from ...debug import assertEqual
from ..data import *
from ..functions import prettifyGen

assert assertEqual(prettifyGen(image), imageHtml)
assert assertEqual(prettifyGen(emptyGen), emptyHtml)
assert assertEqual(prettifyGen(literalFoo), literalHtml)
assert assertEqual(prettifyGen(fieldQuestion), fieldHtml)
assert assertEqual(prettifyGen(requireQuestion), requirementHtml)
assert assertEqual(prettifyGen(requirements3), requirement2Html)
# assert assertEqual(prettifyGen(contradictionRequirement),emptyHtml)
assert assertEqual(prettifyGen(requiringInexistant), emptyHtml)
assert assertEqual(prettifyGen(listEmptyExistingField), listHtml)
