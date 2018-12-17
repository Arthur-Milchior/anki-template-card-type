from .data.models import *
from ..generators.constants import *
from ..generators.generators import modelToFields
from ..templates.soupAndHtml import soupFromTemplate, templateFromSoup

class TestHTML:
    def  __init__(self,source, compiled, *, numberOfTagToEdit = None, model = model, **kwargs):
        self.source = source
        self.model = model
        self.compiled = compiled
        self.kwargs = kwargs
        self.numberOfTagToEdit = numberOfTagToEdit
    #     self.test()

    # def test(self):
        soup = soupFromTemplate(self.source)
        if self.numberOfTagToEdit is not None:
            assert self.numberOfTagToEdit == len(tagsToEdit(soup))
        #debug(f"""TestHTML: kwargs is {self.kwargs}""")
        compile_(soup, soup = soup, model = model, **self.kwargs)
        assert assertEqual(self.compiled, templateFromSoup(soup, prettify = True))

def testEachStep(gen,
                 goal = None,
                 model = model,
                 isQuestion = True,
                 asked = frozenset({"Definition"}),
                 hide = frozenset(),
                 toPrint = False,
                 html = ""):
    fields = modelToFields(model)
    """Apply each step to gen. Print each intermediate step. returne the
    template at the end of the process, and the soup."""
    assert goal is not None
    if toPrint: print(f"""\ntesting each step of "{gen}".""")
    if goal == BASIC:
        return gen
    nf = gen.getNormalForm()
    if toPrint: print(f"""\nnormal form is "{nf}".""")
    if goal == NORMAL:
        return nf
    wr = nf.getWithoutRedundance()
    if toPrint: print(f"""\nwithout redundance is "{wr}".""")
    if goal == WITHOUT_REDUNDANCY:
        return wr
    questionRestriction = wr.questionOrAnswer(isQuestion = isQuestion)
    assert QUESTION_ANSWER<= questionRestriction.getState()
    if toPrint: print(f"""\nWith question restricted, "{questionRestriction}".""")
    if goal == QUESTION_ANSWER:
        return questionRestriction
    modelRestriction = questionRestriction.restrictToModel(fields)
    if toPrint: print(f"""\nWith model applied, "{modelRestriction}".""")
    if goal == MODEL_APPLIED:
        return modelRestriction
    templateRestriction = modelRestriction.template(asked = asked,
                                                    hide = hide)
    if toPrint: print(f"""\nWith template applied, "{templateRestriction}".""")
    if goal == TEMPLATE_APPLIED:
        return templateRestriction
    soup = soupFromTemplate(html)
    templateRestriction.applyTag(tag = soup.enclose, soup = soup)
    prettified = templateFromSoup(soup)
    if toPrint: print(prettified)
    if goal == SOUP:
        return soup
    assert False

def prettifyGen(*args, **kwargs):
    soup = genToSoup(*args, **kwargs)
    return soup.prettify()
 
def compileGen(*args, goal = TEMPLATE_APPLIED, **kwargs):
    return testEachStep(*args, goal = goal, **kwargs)
 
def genToSoup(*args, **kwargs):
    return testEachStep(goal = SOUP_PRETTIFIED, *args, **kwargs)

 
