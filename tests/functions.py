from .imports import *

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
        assert assertEqual("self.compiled", "templateFromSoup(soup, prettify = True)")

def testEachStep(gen,
                 model = model,
                 isQuestion = True,
                 asked = frozenset({"Definition"}),
                 hide = frozenset(),
                 toPrint = False,
                 html = ""):
    """Apply each step to gen. Print each intermediate step. returne the
    template at the end of the process, and the soup."""
    if toPrint: print(f"""\ntesting each step of "{gen}".""")
    nf = gen.getNormalForm()
    if toPrint: print(f"""\nnormal form is "{nf}".""")
    wr = nf.getWithoutRedundance()
    if toPrint: print(f"""\nwithout redundance is "{wr}".""")
    questionRestriction = wr.questionOrAnswer(isQuestion = isQuestion)
    if toPrint: print(f"""\nWith question restricted, "{questionRestriction}".""")
    modelRestriction = questionRestriction.restrictToModel(model)
    if toPrint: print(f"""\nWith model applied, "{modelRestriction}".""")
    templateRestriction = modelRestriction.template(asked = asked,
                                                    hide = hide)
    if toPrint: print(f"""\nWith template applied, "{templateRestriction}".""")
    soup = soupFromTemplate(html)
    templateRestriction.applyTag(tag = soup.enclose, soup = soup)
    prettified = templateFromSoup(soup)
    if toPrint: print(prettified)
    return templateRestriction, soup, prettified


def prettifyGen(*args, **kwargs):
    templateRestriction, soup, prettified = testEachStep(*args, **kwargs)
    return prettified
 
def compileGen(*args, **kwargs):
    templateRestriction, soup, prettified = testEachStep(*args, **kwargs)
    return templateRestriction
 
def genToSoup(*args, **kwargs):
    templateRestriction, soup, prettified = testEachStep(*args, **kwargs)
    return soup
 
