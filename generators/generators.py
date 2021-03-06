import sys

import bs4

from ..debug import (ExceptionInverse, assertType, debug, debugFun,
                     debugOnlyThisMethod, doMemoize)
from ..utils import identity, standardContainer
from .constants import *
from .ensureGen import addTypeToGenerator, ensureGen


def thisClassIsClonable(cl):
    cl.classToClone = cl
    return cl


def memoize(computeKey=(lambda: None)):
    """Decorator:

    It adds a dictionnary "versions" to self.
    versions[function_name][computeKey(*args,**kwargs)] memoize the outputs of function_name on (*args,**kwargs).
    If computeKey returns the same value for many input, the function is computted a single time.
    """
    CURRENTLY_COMPUTED = ("CURRENTLY COMPUTED",)

    def actualArobase(fun):
        if not doMemoize:
            return fun
        fname = fun.__name__
        # @debugFun

        def fun_(self, *args, **kwargs):
            if not hasattr(self, "versions"):
                self.versions = dict()
            if fname not in self.versions:
                self.versions[fname] = dict()
            key = computeKey(*args, **kwargs)
            debug(f"Key is {key}")
            if key not in self.versions:
                debug("Computation is done explicitly")
                self.versions[fname][key] = CURRENTLY_COMPUTED
                self.versions[fname][key] = fun(self, *args, **kwargs)
            else:
                if self.versions[fname][key] == CURRENTLY_COMPUTED:
                    debug("Infinite loop for {fun.__qualname__}({key})")
                    assert False
                else:
                    debug("Computation is retrieved from memoization")
            return self.versions[fname][key]
        fun_.__name__ = f"Memoized_{fun.__name__}"
        fun_.__qualname__ = f"Memoized_{fun.__qualname__}"
        return fun_
    return actualArobase


def modelToFields(model):
    """The set of fields of the model given in argument"""
    return frozenset({fld["name"] for fld in model["flds"]})


def modelToHash(model):
    """Given the model, return the hash of its set of fields."""
    return (model["name"], model["mod"])


def ensureGenAndSetState(state):
    def actualArobase(f):
        # @debugFun
        def aux_ensureGenAndSetState(self, *args, **kwargs):
            self.ensureSingleStep(state)
            ret = f(self, *args, **kwargs)
            ret = self._ensureGen(ret)
            if not ret:
                return self._ensureGen(None)
            else:
                ret.setState(state)
                return ret
        return aux_ensureGenAndSetState
        aux_ensureGenAndSetState.__name__ = f"SetState({State})__{f.__name__}"
        aux_ensureGenAndSetState.__qualname__ = f"SetState({State})__{f.__qualname__}"
    return actualArobase


def ensureReturnGen(f):
    def aux_ensureReturnGen(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        return self._ensureGen(ret)
    aux_ensureReturnGen.__name__ = f"ensureReturnGen_of_{f.__name__}"
    aux_ensureReturnGen.__qualname__ = f"ensureReturnGen_of_{f.__qualname__}"
    return aux_ensureReturnGen

# def emptyToEmpty(f):
#     #@debugFun
#     def f_(self, *args, **kwargs):
#         if self.isEmpty():
#             return None
#         else:
#             return f(self, *args, **kwargs)
#     f_.__name__=f"EmptyToEmpty_{f.__name__}"
#     f_.__qualname__=f"EmptyToEmpty_{f.__qualname__}"
#     return f_

# refer to README.md to understand what this class is about


class Gen:
    """
    Super class for all objects allowing to generate content in templates.
    Should never be instancied directly.

    Each instance has a state, defined in constant. This state allow
    to know what was already processed in the compilation. Ensuring no
    steps are omitted. States can be accessed and edited using some method
    defined below in "finding status". Those methods should not be overided.

    An instance may be «toKeep» or not, according to the variable. A
    list of instances may be discarded if each of its elements are not
    to keep. This is for example the case if the list represents a set
    of fields, and separators between those fields. If there are no
    fields and only separator, there is no reason to keep the list.
    #TODO: check whether "to keep" is still useful.

    There are a lot of method which transform the content of the
    field. Methods not starting with _ call the method of the same
    name, starting with _. They may or may not memoize the result of
    the computation (this is mostly done for steps which are done for
    the compilation, and not for intermediary steps). The method
    without _ must always return a Gen.

    By default, the method _foo, (i.e. starting with _) create a copy
    of self, with each child replaced by child.foo(). This method
    should be reimplemented in subclasses where this method should
    actually have an action.

    To implement inheriting class, see INTERNALS.md, «new core» section
    """
    # @debugFun

    def __init__(self,
                 *,
                 localMandatories=frozenset(),
                 toKeep=None,
                 state=BASIC,
                 locals_=None,
                 ):
        assert assertType(localMandatories, [set, frozenset])
        self.locals_ = locals_
        self.toKeep = toKeep
        self.state = state
        self.localMandatories = localMandatories
        for m in localMandatories:
            assert assertType(m, str)

    def getLocalMandatories(self):
        return self.localMandatories

    def getGlobalMandatories(self):
        m = self.getLocalMandatories()
        for c in self.getChildren():
            m |= c.getGlobalMandatories()
        return m

    indentation = 0
    # @debugFun

    def _ensureGen(self, element):
        """Ensure that a generator is returned, with the state of self"""
        gen = ensureGen(element, self.locals_)
        gen.setState(self.getState())
        return gen

    @debugFun
    def clone(self, children):
        assert False

    #######################
    # Method used for debugging

    @memoize()
    def __repr__(self):
        return self.repr()

    def repr(self, indentDone=False):
        space = "  "*Gen.indentation
        Gen.indentation += 1
        if not indentDone:
            t = space
        else:
            t = ""
        t += self._repr()
        Gen.indentation -= 1
        return t

    def _repr(self):
        return f"""{self.__class__.__name__}(without repr,{self.params()})"""

    def params(self, show=False):
        """The list of params as string. So that it can be printed."""
        if not hasattr(self, "toKeep"):
            self.toKeep = None
        if not hasattr(self, "state"):
            self.state = None
        if not show:
            return ""
        space = "  "*Gen.indentation
        return f"""
{space}toKeep = {self.toKeep},
{space}state = {self.getState()}"""

    def _outerEq(self, other):
        return isinstance(other, Gen) and self.getLocalMandatories() == other.getLocalMandatories()

    def __eq__(self, other):
        return self._outerEq(other) and self._innerEq(other)
    #######################
    # Finding status

    @debugFun
    def setState(self, state):
        """State that the state is at least state. If the state is already higher, then it is not changed.
        Return the actual state."""
        if not hasattr(self, "state"):
            self.state = state
        else:
            self.state = self.state.union(state)
        return self.getState()

    # @debugFun
    def getState(self):
        return self.state

    # @debugFun
    def isAtLeast(self, state):
        return state <= self.getState()

    # @debugFun
    def isEmpty(self):
        return self.isAtLeast(EMPTY)

    # #@debugFun
    # def isNormal(self):
    #     return self.isAtLeast(NORMAL)

    # #@debugFun
    # def isWithoutRedundancy(self):
    #     return self.isAtLeast(WITHOUT_REDUNDANCY)

    # @debugFun
    # def isModelApplied(self):
    #     return self.isAtLeast(MODEL_APPLIED)

    # @debugFun
    # def isTemplateApplied(self):
    #     return self.isAtLeast(TEMPLATE_APPLIED)

    # @debugFun

    def __bool__(self):
        ret = not self.isEmpty()
        return ret

    # @debugFun
    def dontKeep(self):
        self.toKeep = False

        # @debugFun
    def doKeep(self):
        self.toKeep = True

    """The list of children, as generators."""
    @memoize()
    @debugFun
    def getChildren(self):
        return self._getChildren()

    def getToKeep(self):
        if self.toKeep is not None:
            return self.toKeep
        else:
            for child in self.getChildren():
                if child.getToKeep():
                    return True
            return None

    ##########################################
    ## Transform the gen                  #
    #########################################
    #############
    # Meta changing gen

    def ensureSingleStep(self, goal):
        if self.getState() < goal.previousStep():
            raise ExceptionInverse(
                f"Can't compute {goal} from state {self.getState()} of {self}")

    @debugFun
    @ensureReturnGen
    def callOnChildren(self, method, *args, force=True, **kwargs):
        # memoize.__name__ = f"memoize_of_{method}"
        # memoize.__qualname__ = f"memoize_of_{method}"
        # fun_ = fun if force else memoize
        ret = self._callOnChildren(method, *args, **kwargs)
        return ret

    @debugFun
    def _callOnChildren(self, method, *args, force=True, **kwargs):
        elements = []
        someChange = False
        for element in self.getChildren():
            debug("Considering {element}")
            newElement = (getattr(element, method))(*args, **kwargs)
            debug("it becomes {newElement}")
            if newElement != element:
                debug("thus changed")
                someChange = True
            elements.append(newElement)
        if someChange:
            debug("Some change did occurs, thus we clone")
            ret = self.clone(elements=elements)
            return ret
            # if ret == self:
            #     debug("However the clone is identic")
            #     ret = self
            # else:
            #     debug("and the clone is different")
        else:
            debug("No change found, so we keep the old element")
            return self

    ###########################
    # Changing step
    @memoize()
    @debugFun
    @ensureGenAndSetState(NORMAL)
    # @emptyToEmpty
    def getNormalForm(self):
        """A copy of self, where only used classes are «normal»
        classes. In particular, only Gens , and no othe type, are
        returned."""
        return self._getNormalForm()

    @debugFun
    def _getNormalForm(self):
        return self.callOnChildren(method="getNormalForm")

    @memoize()
    @ensureGenAndSetState(WITHOUT_REDUNDANCY)
    @debugFun
    @debugOnlyThisMethod
    def getWithoutRedundance(self):
        """Remove redundant, like {{#foo}}{{#foo}}, {{#foo}}{{^foo}}.
        Similarly, Question/Answer inside Question/Answer. And
        Asked(foo) inside Asked(Foo)

        """
        return self._getWithoutRedundance()

    @debugFun
    def _getWithoutRedundance(self):
        return self.callOnChildren(method="getWithoutRedundance")

    @memoize((lambda isQuestion: isQuestion))
    @ensureGenAndSetState(QUESTION_ANSWER)
    # @emptyToEmpty
    @debugFun
    def questionOrAnswer(self, isQuestion):
        """Assert that this is the question side if isQuestion is
        True. Otherwise answer side.

        Thus remove the Answer(), and replace Question() by its content
        """

        return self._questionOrAnswer(isQuestion=isQuestion)

    @debugFun
    def _questionOrAnswer(self, isQuestion):
        if isQuestion:
            return self.assumeQuestion(changeStep=True)
        else:
            return self.assumeAnswer(changeStep=True)

    @memoize((lambda fields: fields))
    @ensureGenAndSetState(MODEL_APPLIED)
    # @emptyToEmpty
    @debugFun
    def restrictToModel(self, fields):
        """Given the model, restrict the generator according the fields
        existing. It follows that the returned answer contains no
        requireInModel/requireAbsentOfModel requirement. It contains
        no Field(foo), or Filled(foo), if foo does not belong to the model.
        """
        if isinstance(fields, str):
            fields = {fields}
        missing = self.getLocalMandatories() - fields
        if missing:
            print(
                f"""Beware: the generator {self} request the field(s) {missing} which is/are absent from your model.""", file=sys.stderr)
        return self._restrictToModel(fields=fields)

    @debugFun
    def _restrictToModel(self, fields):
        return self.callOnChildren(method="restrictToModel", fields=fields)

    @memoize(lambda fields: fields)
    @ensureGenAndSetState(MANDATORY)
    @ensureReturnGen
    @debugFun
    def mandatory(self, fields):
        """Self, where the display only occurs if each fields of mandatory are be filled"""
        if isinstance(fields, str):
            fields = {fields}
        current = self.assumeFieldFilled(fields, setMandatoryState=True)
        for field in fields:
            # EnsureGen of a tuple create a FilledObject.
            current = self._ensureGen((field, current))
            current.setState(MANDATORY)
        return current

    @memoize(lambda fields: fields)
    @ensureGenAndSetState(FORBIDDEN)
    @ensureReturnGen
    @debugFun
    def forbidding(self, fields):
        """Self, where the display only occurs if each fields of mandatory are be filled"""
        current = self.assumeFieldEmpty(fields, setForbiddenState=True)
        for field in fields:
            # EnsureGen of a tuple create a FilledObject.
            current = self._ensureGen((field, None, current))
            current.setState(FORBIDDEN)
        return current

    @memoize()
    @ensureReturnGen
    @debugFun
    def force(self):
        """Ensure that ensureGen is called on each element recursively."""
        self.callOnChildren(method="force")

    @memoize()
    @ensureGenAndSetState(ASKED)
    @ensureReturnGen
    @debugFun
    def noMoreAsk(self):
        """Remove all Asked(foo), and replace NotAsked(foo) with foo"""
        return self._noMoreAsk()

    @debugFun
    def _noMoreAsk(self):
        return self.callOnChildren(method="noMoreAsk")

    # @emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeFieldFilled(self, fields, setMandatoryState=False):
        """Remove Empty(field,foo) and Absent(field,foo), replace Filled(field,foo) by foo, for each field in fields"""
        if isinstance(fields, str):
            fields = {fields}
        ret = self._assumeFieldFilled(fields, setMandatoryState)
        if setMandatoryState:
            ret = self._ensureGen(ret)
            ret.setState(MANDATORY)
        return ret

    @debugFun
    def _assumeFieldFilled(self, fields, setMandatoryState):
        return self.callOnChildren("assumeFieldFilled", fields=fields, setMandatoryState=setMandatoryState)

    # @emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeFieldEmpty(self, fields, setForbiddenState=False):
        """Remove Filled(field,foo), replace Empty(field,foo) by foo"""
        if isinstance(fields, str):
            fields = {fields}
        ret = self._assumeFieldEmpty(fields, setForbiddenState)
        if setForbiddenState:
            ret = self._ensureGen(ret)
            ret.setState(FORBIDDEN)
        return ret

    @debugFun
    def _assumeFieldEmpty(self, fields, setForbiddenState):
        return self.callOnChildren("assumeFieldEmpty", fields, setForbiddenState)

    # @emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeFieldPresent(self, field):
        """Remove Absent(field,foo), replace Present(field,foo) by foo"""
        return self._assumeFieldPresent(field)

    @debugFun
    def _assumeFieldPresent(self, field):
        return self.callOnChildren("assumeFieldPresent", field=field)

    # @emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeFieldAbsent(self, field):
        """Remove Present(field,foo) and Filled(field,foo), replace Absent(field,foo) by foo"""
        return self._assumeFieldAbsent(field)

    @debugFun
    def _assumeFieldAbsent(self, field):
        return self.callOnChildren("assumeFieldAbsent", field=field)

    # @emptyToEmpty
    @memoize((lambda changeStep=False: None))
    @ensureReturnGen
    @debugFun
    def assumeQuestion(self, changeStep=False):
        """Assume this is question side. Replace Question(foo) by
    foo. Remove Answer(foo)"""
        assert assertType(changeStep, bool)
        ret = self._assumeQuestion(changeStep=changeStep)
        ret = self._ensureGen(ret)
        if changeStep:
            ret.setState(QUESTION_ANSWER)
        return ret

    @debugFun
    def _assumeQuestion(self, changeStep):
        return self.callOnChildren("assumeQuestion", changeStep=changeStep)

    # @emptyToEmpty
    @memoize((lambda changeStep=False: None))
    @ensureReturnGen
    @debugFun
    def assumeAnswer(self, changeStep=False):
        """Assume this is answer side. Replace Answer(foo) by
        foo. Remove Question(foo)"""
        ret = self._assumeAnswer(changeStep=changeStep)
        ret = self._ensureGen(ret)
        if changeStep:
            ret.setState(QUESTION_ANSWER)
        return ret

    @debugFun
    def _assumeAnswer(self, changeStep=False):
        return self.callOnChildren("assumeAnswer", changeStep=changeStep)

    # @emptyToEmpty
    @memoize((lambda fields, modelName=None, changeState=False: fields))
    @ensureReturnGen
    @debugFun
    def assumeAsked(self, fields, modelName=None, changeState=False):
        """
        Assume that name is asked. Thus remove notAsked(name,foo). Replace
        Asked(name,foo) by foo. Recall that this name was asked in
        this model. Change the state to ASKED if changeState is True.
        """
        if isinstance(fields, str):
            fields = frozenset({fields})
        ret = self._assumeAsked(fields, modelName, changeState)
        ret = self._ensureGen(ret)
        if changeState:
            ret.setState(ASKED)
        return ret

    @debugFun
    def _assumeAsked(self, fields, modelName, changeState):
        return self.callOnChildren("assumeAsked", fields, modelName, changeState)

    # @emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeNotAsked(self, name):
        """Assume that name is not asked. Thus remove
        Asked(name,foo). Replace NotAsked(name,foo) by foo."""
        return self._assumeNotAsked(name)

    @debugFun
    def _assumeNotAsked(self, name):
        return self.callOnChildren("assumeNotAsked", name)

    # @emptyToEmpty
    @memoize((lambda fields, changeState=False: fields))
    @ensureReturnGen
    @debugFun
    def removeName(self, fields, changeState=False):
        """remove each instance of Asked(name,foo) and NotAsked(name,Foo)"""
        if isinstance(fields, str):
            fields = {fields}
        ret = self._removeName(fields, changeState)
        ret = self._ensureGen(ret)
        if changeState:
            ret.setState(HIDE)
        return ret

    @debugFun
    def _removeName(self, fields, changeState):
        return self.callOnChildren("removeName", fields, changeState)

    #################
    # Consider the end of compilation

    @memoize((lambda soup: None))
    @debugFun
    def createHtml(self, soup):
        """A list of BeautifulSoup object representing this
        generator.
        """
        self.ensureSingleStep(TAG)
        assert soup is not None
        new_tag = self._createHtml(soup)
        if new_tag is None:
            ret = []
        elif isinstance(new_tag, list):
            ret = new_tag
        elif isinstance(new_tag, bs4.element.NavigableString) or isinstance(new_tag, bs4.element.Tag):
            ret = [new_tag]
        else:
            assert False
        assert assertType(ret, list)
        return ret

    @debugFun
    def getQuestions(self):
        return self._getQuestions()

    @debugFun
    def _getQuestions(self):
        s = []
        for child in self.getChildren():
            s += child.getQuestions()
        return s

    @debugFun
    def getName(self):
        return self._getName()

    @debugFun
    def _getName(self):
        for child in self.getChildren():
            n = child.getName()
            if n is not None:
                return n
        return None

    @debugFun
    def getQuestionToAsk(self, model):
        return self._getQuestionToAsk(model)

    @debugFun
    def _getQuestionToAsk(self, model):
        for child in self.getChildren():
            q = child.getQuestionToAsk(model)
            if q is not None:
                return q
        return None

    @debugFun
    def _createHtml(self, soup):
        """A (list of) BeautifulSoup object representing this
        generator. Or None
        """
        raise ExceptionInverse(f"""_createHtml in gen for: "{self}".""")

    @memoize((lambda
              soup=None,
              goal=None,
              fields=None,
              isQuestion=None,
              asked=None,
              mandatory=None,
              hide=None,
              hideQuestions=None,
              toPrint=False,
              modelName=None,
              template=None:
              (goal, fields, isQuestion, asked, mandatory, hide, hideQuestions)))
    @debugFun
    def compile(self,
                soup=None,
                goal=None,
                fields=None,
                isQuestion=None,
                asked=None,
                forbidden=None,
                mandatory=None,
                hide=None,
                hideQuestions=None,
                toPrint=False,
                modelName=None,
                template=None
                ):
        """Compile as much as possible given the informations. Or up to goal."""
        if goal is None:
            if isQuestion is None:
                goal = WITHOUT_REDUNDANCY
            elif fields is None:
                goal = QUESTION_ANSWER
            elif asked is not None or hide is not None or mandatory is not None:
                goal = MODEL_APPLIED
            elif hide is None:
                goal = HIDE
            elif asked is None:
                goal = ASKED
            elif mandatory is None:
                goal = MANDATORY
            else:
                goal = TAG

        if toPrint:
            print(f"""\nTesting each step of "{self}".""")
        if goal == BASIC:
            return self

        nf = self.getNormalForm()
        if toPrint:
            print(f"""\nNormal form is "{nf}".""")
        if goal == NORMAL:
            return nf

        wr = nf.getWithoutRedundance()
        if toPrint:
            print(f"""\nWithout redundance is "{wr}".""")
        if goal == WITHOUT_REDUNDANCY:
            return wr

        assert isQuestion is not None
        questionRestriction = wr.questionOrAnswer(isQuestion=isQuestion)
        assert QUESTION_ANSWER <= questionRestriction.getState()
        if toPrint:
            print(f"""\nWith question restricted, "{questionRestriction}".""")
        if goal == QUESTION_ANSWER:
            return questionRestriction

        if isQuestion and hideQuestions:
            for hideQuestion in hideQuestions:
                questionRestriction = questionRestriction.removeName(
                    hideQuestion)

        assert fields is not None
        modelRestriction = questionRestriction.restrictToModel(fields)
        if toPrint:
            print(f"""\nWith model({fields}) applied, "{modelRestriction}".""")
        if goal == MODEL_APPLIED:
            return modelRestriction

        if hide is None:
            hide = frozenset()
        assert standardContainer(hide)
        hidden = modelRestriction.removeName(hide, True)
        if toPrint:
            print(f"""\nWith removeName({hide}) applied, "{hidden}".""")
        if goal == HIDE:
            return hidden

        if asked is None:
            asked = frozenset()
        assert standardContainer(asked)
        askedGen = hidden.assumeAsked(asked, modelName, True).noMoreAsk()
        if toPrint:
            print(f"""\nWith assumeAsked({asked}) applied, "{askedGen}".""")
        if goal == ASKED:
            return askedGen

        if mandatory is None:
            mandatory = frozenset()
        missingFields = mandatory-fields
        if missingFields:
            raise Exception(
                f"{missingFields} are mandatory but not in the model.")
        mandatoried = askedGen.mandatory(mandatory)
        if toPrint:
            print(
                f"""\nWith mandatory({mandatory}) applied, "{mandatoried}".""")
        if goal == MANDATORY:
            return mandatoried

        if forbidden is None:
            forbidden = frozenset()
        forbidded = mandatoried.forbidding(forbidden)
        if toPrint:
            print(
                f"""\nWith forbidding({forbidden}) applied, "{forbidded}".""")
        if goal == FORBIDDEN:
            return forbidded

        if template:
            name = forbidded.getName()
            template["name"] = name

        assert soup is not None
        try:
            resultTags = forbidded.createHtml(soup=soup)
        except Exception:
            print(f"mandatoried is {mandatoried}")
            raise
        str(resultTags)
        if goal == TAG:
            return resultTags

        assert False

    def firstDifference(self, other):
        """A pair of generators, in the same position in the tree of self/other, which are distinct"""
        if not self._outerEq(other):
            return (self, other)
        else:
            return self._firstDifference(other)

# class Normal(Gen):
#     def __init__(self, *args, **kwargs):
#         super().__init__(self, *args, **kwargs)
#         if not hasattr(hasNormalType)
#     pass


addTypeToGenerator(Gen, identity)

# @debugFun


def shouldBeKept(gen):
    """
    True if Gen which must be kept.
    False if Gen which can be discarded
    None if it can't yet been known."""
    if isinstance(gen, Gen):
        return gen.getToKeep()
    else:
        return None


def genRepr(g, label=None):
    t = "  "*Gen.indentation
    if label is not None:
        t += f"{label} = "
    if isinstance(g, Gen):
        t += g.repr(indentDone=True)
    else:
        t += repr(g)
    return t


class MultipleChildren(Gen):
    # @debugFun
    def __init__(self, toKeep=None,  **kwargs):
        super().__init__(**kwargs)

        # if toKeep is None:
        #     allFalse = True
        #     for element in self.getChildren():
        #         shouldIt = shouldBeKept(element)
        #         if shouldIt is True:
        #             toKeep = True
        #             allFalse = False
        #             break
        #         if shouldIt is None:
        #             allFalse = None
        #     if allFalse:
        #         toKeep = False
        # if toKeep is True:
        #     self.doKeep()
        # elif toKeep is False:
        #     self.dontKeep()


class NotNormal(Gen):
    def _getWithoutRedundance(self):
        raise ExceptionInverse(f"_getWithoutRedundance from not normal")
    # def getWithoutRedundance(self):
    #     raise ExceptionInverse(f"getWithoutRedundance from not normal")
    # def assumeFieldInSet(self, *args, **kwargs):
    #     raise ExceptionInverse(f"assumeFieldInSet from not normal")

    def _assumeFieldFilled(self, field, setMandatoryState):
        raise ExceptionInverse(f"_assumeFieldFilled from not normal:{self}")

    def _assumeFieldEmpty(self, fields, setForbiddenState=False):
        raise ExceptionInverse(f"_assumeFieldEmpty from not normal:{self}")

    def _assumeFieldPresent(self, field):
        raise ExceptionInverse(f"_assumeFieldPresent from not normal:{self}")

    def _assumeAnswer(self, changeStep=False):
        raise ExceptionInverse(f"_assumeAnswer from not normal:{self}")

    def _assumeFieldAbsent(self, field):
        raise ExceptionInverse(f"_assumeFieldAbsent from not normal:{self}")

    def _getQuestions(self):
        raise ExceptionInverse(f"_getQuestions from not normal:{self}")

    def _getName(self):
        raise ExceptionInverse(f"_getQuestions from not normal:{self}")
    # def _assumeFieldInSet(self, *args, **kwargs):
    #     raise ExceptionInverse(f"_assumeFieldInSet from not normal")

    def _assumeQuestion(self, *args, **kwargs):
        raise ExceptionInverse(f"_assumeQuestion from not normal:{self}")

    def _createHtml(self, *args, **kwargs):
        raise ExceptionInverse(f"_createHtml from not normal:{self}")

    def _restrictToModel(self, *args, **kwargs):
        raise ExceptionInverse(f"_restrictToModel from not normal:{self}")

    def _questionOrAnswer(self, *args, **kwargs):
        raise ExceptionInverse(f"_questionOrAnswer from not normal:{self}")


class SingleChild(MultipleChildren):
    def __init__(self, child=None, toKeep=None, **kwargs):
        self.child = child
        super().__init__(toKeep=toKeep, **kwargs)

    @debugFun
    def clone(self, elements):
        assert len(elements) == 1
        child = elements[0]
        return self.cloneSingle(child)

    @debugFun
    def cloneSingle(self, child):
        if not child:
            return None
        if child == self.getChild():
            return self
        return self._cloneSingle(child)

    @debugFun
    def _cloneSingle(self, child):
        """Assuming child is distinct from self.child and is not truthy"""
        return self.classToClone(child=child)

    @debugFun
    def getChild(self):
        self.child = self._ensureGen(self.child)
        return self.child

    # @ensureReturnGen
    # #@debugFun
    # @memoize()
    # def getChild(self):
    #     return self.child

    @debugFun
    def _getChildren(self):
        return [self.getChild()]

    def __hash__(self):
        return hash((self.__class__, self.child))

    def _repr(self):
        space = "  "*Gen.indentation
        if hasattr(self, "classToClone"):
            toClone = self.classToClone
            if toClone == self.__class__:
                className = self.__class__.__name__
            else:
                className = f"{self.__class__.__name__}/{toClone}"
        else:
            className = self.__class__.__name__
        t = f"""{className}(
{genRepr(self.child, label="child")},{self.params()})"""
        return t

    def _innerEq(self, other):
        """It may require to actually compute the child"""
        return self.getChild() == other.getChild()

    def _outerEq(self, other):
        return isinstance(other, SingleChild) and super()._outerEq(other)

    def _firstDifference(self, other):
        return self.getChild().firstDifference(other.getChild())
