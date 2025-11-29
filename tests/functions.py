import bs4

from ..debug import assertEqual, debugOnlyThisMethod
from ..generators.constants import *
from ..generators.ensureGen import ensureGen
from ..generators.generators import modelToFields
from ..templates.soupAndHtml import soupFromTemplate, templateFromSoup
from ..templates.templates import compile_
from .data.models import *


class TestHTML:
    def __init__(self, source, compiled, *, numberOfTagToEdit=None, model=model, **kwargs):
        self.source = source
        self.model = model
        self.compiled = compiled
        self.kwargs = kwargs
        self.numberOfTagToEdit = numberOfTagToEdit
    #     self.test()

    # def test(self):
        soup = soupFromTemplate(self.source)
        #debug("""TestHTML: kwargs is {self.kwargs}""")
        compile_(soup, soup=soup, model=model, recompile=True, **self.kwargs)
        assert assertEqual(templateFromSoup(
            soup, prettify=True), self.compiled)


def testEachStep(gen,
                 goal=None,
                 modelName=None,
                 isQuestion=True,
                 asked=frozenset({"Definition"}),
                 hide=frozenset(),
                 mandatory=frozenset(),
                 toPrint=False,
                 fields=None,
                 html=""):
    """Main interest is changing the default value for ones useful for the test"""
    if fields is None:
        fields = modelToFields(model)
    soup = soupFromTemplate(html)
    gen = ensureGen(gen)
    return gen.compile(
        soup=soup,
        goal=goal,
        fields=fields,
        isQuestion=isQuestion,
        asked=asked,
        mandatory=mandatory,
        hide=hide,
        toPrint=toPrint,
        modelName=modelName
    )


def prettifyGen(*args, **kwargs):
    soup = genToSoup(*args, **kwargs)
    return templateFromSoup(soup)


def compileGen(*args, goal=LAST_GEN_STEP, **kwargs):
    return testEachStep(*args, goal=goal, **kwargs)


def genToTags(*args, **kwargs):
    return genToSoup(goal=TAG, *args, **kwargs)


def genToSoup(*args, **kwargs):
    bs = bs4.BeautifulSoup("", "html.parser")
    bs.clear()
    new_tags = testEachStep(goal=TAG, *args, **kwargs)
    for tag in new_tags:
        bs.append(tag)
    return bs
