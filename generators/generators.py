from ..debug import debug, assertType, debugFun, ExceptionInverse, optimize, debugOnlyThisMethod
from ..utils import identity, standardContainer
from .ensureGen import ensureGen, addTypeToGenerator
from .constants import *
import bs4
import sys
#from ..templates.soupAndHtml import templateFromSoup


def thisClassIsClonable(cl):
    cl.classToClone = cl
    return cl

def memoize(computeKey = (lambda:None)):
    CURRENTLY_COMPUTED = ("CURRENTLY COMPUTED",)
    def actualArobase(fun):
        if not optimize:
            return fun
        fname = fun.__name__
        #@debugFun
        def fun_(self, *args, **kwargs):
            if not hasattr(self, "versions"):
                self.versions = dict()
            if fname not in self.versions:
                self.versions[fname] = dict()
            key = computeKey(*args, **kwargs)
            if key not in self.versions:
                debug("Computation is done explicitly")
                self.versions[fname][key] = ("CURRENTLY COMPUTED",)
                self.versions[fname][key] = fun(self, *args, **kwargs)
            else:
                if self.versions[fname][key] == CURRENTLY_COMPUTED:
                    debug("Infinite loop for {fun.__qualname__}({key})")
                    assert False
                else:
                    debug("Computation is retrieved from memoization")
            return self.versions[fname][key]
        fun_.__name__=f"Memoized_{fun.__name__}"
        fun_.__qualname__=f"Memoized_{fun.__qualname__}"
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
        #@debugFun
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
        aux_ensureGenAndSetState.__name__=f"SetState({State})__{f.__name__}"
        aux_ensureGenAndSetState.__qualname__=f"SetState({State})__{f.__qualname__}"
    return actualArobase

def ensureReturnGen(f):
    def aux_ensureReturnGen(self, *args, **kwargs):
        return self._ensureGen(f(self, *args, **kwargs))
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

#refer to README.md to understand what this class is about
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
    #@debugFun
    def __init__(self,
                 *,
                 localMandatories = frozenset(),
                 toKeep = None,
                 state = BASIC,
                 locals_ = None,
    ):
        assert isinstance(localMandatories,set) or assertType(localMandatories,frozenset) 
        self.locals_ = locals_
        self.toKeep = toKeep
        self.state = state
        self.localMandatories = localMandatories
        for m in localMandatories:
            assert assertType(m,str)

    def getLocalMandatories(self):
        return self.localMandatories

    def getGlobalMandatories(self):
        m = self.getLocalMandatories()
        for c in self.getChildren():
            m|= c.getGlobalMandatories()
        return m

    indentation = 0
    #@debugFun
    def _ensureGen(self, element):
        """Ensure that a generator is returned, with the state of self"""
        gen = ensureGen(element, self.locals_)
        gen.setState(self.getState())
        return gen


    @debugFun
    def clone(self,children):
        assert False

    #######################
    # Method used for debugging

    @memoize()
    def __repr__(self):
        return self.repr()

    def repr(self, indentDone = False):
        space = "  "*Gen.indentation
        Gen.indentation +=1
        if not indentDone:
            t= space
        else:
            t =""
        t+= self._repr()
        Gen.indentation -=1
        return t

    def _repr(self):
        return f"""{self.__class__.__name__}(without repr,{self.params()})"""
        
    def params(self, show = False):
        """The list of params as string. So that it can be printed."""
        if not hasattr(self,"toKeep"):
            self.toKeep = None
        if not hasattr(self,"state"):
            self.state = None
        if not show:
            return ""
        space = "  "*Gen.indentation
        return f"""
{space}toKeep = {self.toKeep},
{space}state = {self.getState()}"""

    def _outerEq(self, other):
        return self.getLocalMandatories() == other.getLocalMandatories()

    def __eq__(self,other):
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
    
    #@debugFun
    def getState(self):
        return self.state

    #@debugFun
    def isAtLeast(self,state):
        return state <= self.getState()
    
    #@debugFun
    def isEmpty(self):
        return self.isAtLeast(EMPTY)

    #@debugFun
    def isNormal(self):
        return self.isAtLeast(NORMAL)
    
    #@debugFun
    def isWithoutRedundancy(self):
        return self.isAtLeast(WITHOUT_REDUNDANCY)

    @debugFun
    def isModelApplied(self):
        return self.isAtLeast(MODEL_APPLIED)
    
    @debugFun
    def isTemplateApplied(self):
        return self.isAtLeast(TEMPLATE_APPLIED)

    
    #@debugFun
    def __bool__(self):
        ret = not self.isEmpty()
        return ret
    
    #@debugFun
    def dontKeep(self):
        self.toKeep = False

        #@debugFun
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

    def ensureSingleStep(self,goal):
        if self.getState() < goal.previousStep():
            raise ExceptionInverse(f"Can't compute {goal} from state {self.getState()} of {self}")

    @debugFun
    @ensureReturnGen
    def callOnChildren(self, method, *args, force = True, **kwargs):
        # memoize.__name__ = f"memoize_of_{method}"
        # memoize.__qualname__ = f"memoize_of_{method}"
        # fun_ = fun if force else memoize
        ret = self._callOnChildren(method, *args, **kwargs)
        return ret
    
    @debugFun
    def _callOnChildren(self, method, *args, force = True, **kwargs):
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
            ret = self.clone(elements = elements)
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
    #@emptyToEmpty
    def getNormalForm(self):
        """A copy of self, where only used classes are «normal»
        classes. In particular, only Gens , and no othe type, are
        returned."""  
        return self._getNormalForm()
    @debugFun
    def _getNormalForm(self):
        return self.callOnChildren(method = "getNormalForm")
    
    @memoize()
    @ensureGenAndSetState(WITHOUT_REDUNDANCY)
    #@emptyToEmpty
    @debugFun
    def getWithoutRedundance(self):
        """Remove redundant, like {{#foo}}{{#foo}}, {{#foo}}{{^foo}}.
        Similarly, Question/Answer inside Question/Answer. And
        Asked(foo) inside Asked(Foo)

        """        
        return self._getWithoutRedundance()
    
    @debugFun
    def _getWithoutRedundance(self):
        return self.callOnChildren(method = "getWithoutRedundance")
    
    @memoize((lambda isQuestion:isQuestion))
    @ensureGenAndSetState(QUESTION_ANSWER)
    #@emptyToEmpty
    @debugFun
    def questionOrAnswer(self, isQuestion):
        """Assert that this is the question side if isQuestion is
        True. Otherwise answer side.
        
        Thus remove the Answer(), and replace Question() by its content
        """
    
    
        return self._questionOrAnswer(isQuestion = isQuestion)
    
    @debugFun
    def _questionOrAnswer(self, isQuestion):
        if isQuestion:
            return self.assumeQuestion(changeStep = True)
        else:
            return self.assumeAnswer(changeStep = True)

    @memoize((lambda fields:fields))
    @ensureGenAndSetState(MODEL_APPLIED)
    #@emptyToEmpty
    @debugFun
    def restrictToModel(self,fields):
        """Given the model, restrict the generator according the fields
        existing. It follows that the returned answer contains no
        requireInModel/requireAbsentOfModel requirement. It contains
        no Field(foo), or Filled(foo), if foo does not belong to the model.
        """
        missing = self.getLocalMandatories() - fields
        if missing:
            print(f"""Beware: the generator {self} request the field(s) {missing} which is/are absent from your model.""", file=sys.stderr)                    
        return self._restrictToModel(fields = fields)
    @debugFun
    def _restrictToModel(self,fields):
        return self.callOnChildren(method = "restrictToModel", fields = fields)

    @memoize((lambda asked, hide:(asked,hide)))
    #@ensureGenAndSetState(TEMPLATE_APPLIED) done in NoMoreAsk
    #@emptyToEmpty
    @debugFun
    def template(self, asked = frozenset(), hide = frozenset(), mandatory = frozenset(),modelName=None):
        """A copy of self where every Asked(foo) or NotAsked(foo), with foo in
        hide, is hidden. And everything in asked is asked. Everything else
        is not hidden.
        """
        step = self
        if mandatory:
            step = step.addMustBeFilled(mandatory)
        return step._template(asked = asked, hide = hide, modelName=modelName)
    
    @debugFun
    def _template(self, asked = frozenset(), hide = frozenset(),modelName=None):
        assert standardContainer(asked)
        assert standardContainer(hide)
        current = self
        for name in hide:
            current = current.removeName(name)
        for name in asked:
            current = current.assumeAsked(name,modelName=modelName)
        return current.noMoreAsk()
    
    @debugFun
    def addMustBeFilled(self, mandatory):
        """Self, where the display only occurs if each fields of mandatory are be filled"""
        current = self
        for field in mandatory:
            current = current.assumeFieldFilled(field)
        for field in mandatory:
            #EnsureGen of a tuple create a FilledObject.
            current = self._ensureGen((field,current))
        return current

    @ensureReturnGen
    @debugFun
    def force(self):
        """Ensure that ensureGen is called on each element recursively."""
        self.callOnChildren(method = "force")

    @ensureGenAndSetState(TEMPLATE_APPLIED)
    @ensureReturnGen
    @debugFun
    def noMoreAsk(self):
        """Remove all Asked(foo), and replace NotAsked(foo) with foo"""
        return self._noMoreAsk()
    @debugFun
    def _noMoreAsk(self):
        return self.callOnChildren(method = "noMoreAsk")

    #@emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeFieldFilled(self, field):
        """Remove Empty(field,foo) and Absent(field,foo), replace Filled(field,foo) by foo"""
        return self._assumeFieldFilled(field)
    
    @debugFun
    def _assumeFieldFilled(self, field):
        return self.callOnChildren("assumeFieldFilled", field = field)
    
    #@emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeFieldEmpty(self, field):
        """Remove Filled(field,foo), replace Empty(field,foo) by foo"""
        return self._assumeFieldEmpty(field)
    @debugFun
    def _assumeFieldEmpty(self, field):
        return self.callOnChildren("assumeFieldEmpty", field = field)
        
    #@emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeFieldPresent(self, field):
        """Remove Absent(field,foo), replace Present(field,foo) by foo"""
        return self._assumeFieldPresent(field)
    @debugFun
    def _assumeFieldPresent(self, field):
        return self.callOnChildren("assumeFieldPresent", field = field)
    
    #@emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeFieldAbsent(self, field):
        """Remove Present(field,foo) and Filled(field,foo), replace Absent(field,foo) by foo"""
        return self._assumeFieldAbsent(field)    
    @debugFun
    def _assumeFieldAbsent(self, field):
        return self.callOnChildren("assumeFieldAbsent", field = field)

    #@emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeQuestion(self, changeStep = False):
        """Assume this is question side. Replace Question(foo) by
    foo. Remove Answer(foo)"""
        assert assertType(changeStep, bool)
        ret = self._assumeQuestion(changeStep = changeStep)
        ret = self._ensureGen(ret)
        if changeStep:
            ret.setState(QUESTION_ANSWER)
        return ret
    @debugFun
    def _assumeQuestion(self, changeStep):
        return self.callOnChildren("assumeQuestion", changeStep = changeStep)
    
    #@emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeAnswer(self, changeStep = False):
        """Assume this is answer side. Replace Answer(foo) by
        foo. Remove Question(foo)"""
        ret = self._assumeAnswer(changeStep = changeStep)
        ret = self._ensureGen(ret)
        if changeStep:
            ret.setState(QUESTION_ANSWER)
        return ret
    @debugFun
    def _assumeAnswer(self, changeStep = False):
        return self.callOnChildren("assumeAnswer", changeStep = changeStep)
        
    #@emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeAsked(self, name,modelName=None):
        """Assume that name is asked. Thus remove
        notAsked(name,foo). Replace Asked(name,foo) by foo"""
        return self._assumeAsked(name,modelName)
    @debugFun
    def _assumeAsked(self, name,modelName):
        return self.callOnChildren("assumeAsked", name,modelName)
        
    #@emptyToEmpty
    @ensureReturnGen
    @debugFun
    def assumeNotAsked(self, name):
        """Assume that name is not asked. Thus remove
        Asked(name,foo). Replace NotAsked(name,foo) by foo."""
        return self._assumeNotAsked(name)
    @debugFun
    def _assumeNotAsked(self, name):
        return self.callOnChildren("assumeNotAsked", name)
        
    #@emptyToEmpty
    @ensureReturnGen
    @debugFun
    def removeName(self, name):
        """remove each instance of Asked(name,foo) and NotAsked(name,Foo)"""
        return self._removeName(name)
    @debugFun
    def _removeName(self, name):
        return self.callOnChildren("removeName", name)

    #################
    # Consider the end of compilation
        
    @debugFun
    def applyTag(self, soup):
        """A list of BeautifulSoup object representing this
        generator. 
        """
        self.ensureSingleStep(TAG)
        assert soup is not None
        new_tag = self._applyTag(soup)
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
        s=[]
        for child in self.getChildren():
            s+=child.getQuestions()
        return s
    @debugFun
    def getQuestionToAsk(self,model):
        return self._getQuestionToAsk(model)

    @debugFun
    def _getQuestionToAsk(self,model):
        for child in self.getChildren():
            q=child.getQuestionToAsk(model)
            if q is not None:
                return q
        return None

    @debugFun
    def _applyTag(self, soup):
        """A (list of) BeautifulSoup object representing this
        generator. Or None
        """
        raise ExceptionInverse(f"""_applyTag in gen for: "{self}".""")

    @debugFun
    def compile(self,
                soup = None,
                goal = None,
                fields = None,
                isQuestion = None,
                asked = None,
                mandatory = None,
                hide = None,
                hideQuestions = None,
                toPrint = False,
                modelName=None,
    ):
        """Compile as much as possible given the informations. Or up to goal."""
        if goal is None:
            if isQuestion is None:
                goal = WITHOUT_REDUNDANCY
            elif fields is None:
                goal = QUESTION_ANSWER
            elif asked is not None or hide is not None or mandatory is not None:
                goal = MODEL_APPLIED
            if soup is None:
                goal = TEMPLATE_APPLIED
            else :
                goal = TAG
                
        if toPrint: print(f"""\nTesting each step of "{self}".""")
        if goal == BASIC:
            return self

        nf = self.getNormalForm()
        if toPrint: print(f"""\nNormal form is "{nf}".""")
        if goal == NORMAL:
            return nf

        wr = nf.getWithoutRedundance()
        if toPrint: print(f"""\nWithout redundance is "{wr}".""")
        if goal == WITHOUT_REDUNDANCY:
            return wr

        assert isQuestion is not None
        questionRestriction = wr.questionOrAnswer(isQuestion = isQuestion)
        assert QUESTION_ANSWER<= questionRestriction.getState()
        if toPrint: print(f"""\nWith question restricted, "{questionRestriction}".""")
        if goal == QUESTION_ANSWER:
            return questionRestriction

        if isQuestion and hideQuestions:
            for hideQuestion in hideQuestions:
                questionRestriction = questionRestriction.removeName(hideQuestion)
                
        assert fields is not None
        modelRestriction = questionRestriction.restrictToModel(fields)
        if toPrint: print(f"""\nWith model({fields}) applied, "{modelRestriction}".""")
        if goal == MODEL_APPLIED:
            return modelRestriction
        
        if asked is None:
            asked = frozenset()
        if hide is None:
            hide = frozenset()
        assert standardContainer(asked)
        assert standardContainer(hide)
        if mandatory is None:
            mandatory = frozenset()
        missingFields=mandatory-fields
        if missingFields:
            raise Exception(f"{missingFields} are mandatory but not in the model.")
        templateRestriction = modelRestriction.template(asked = asked,
                                                        hide = hide,
                                                        mandatory = mandatory,
                                                        modelName = modelName)
        if toPrint: print(f"""\nWith template(asked = {asked}, hide = {hide}, mandatory = {mandatory}, modelName = {modelName}) applied, "{templateRestriction}".""")
        if goal == TEMPLATE_APPLIED:
            return templateRestriction

        assert soup is not None
        resultTags = templateRestriction.applyTag(soup = soup)
        if goal == TAG:
            return resultTags
        
        assert False
        
    def firstDifference(self,other):
        """A pair of generators, in the same position in the tree of self/other, which are distinct"""
        if not self._outerEq(other):
            return (self,other)
        else:
            return self._firstDifference(other)

# class Normal(Gen):
#     def __init__(self, *args, **kwargs):
#         super().__init__(self, *args, **kwargs)
#         if not hasattr(hasNormalType)
#     pass

addTypeToGenerator(Gen, identity)

#@debugFun
def shouldBeKept(gen):
    """
    True if Gen which must be kept. 
    False if Gen which can be discarded
    None if it can't yet been known."""
    if isinstance(gen,Gen):
        return gen.getToKeep()
    else:
        return None
    
def genRepr(g, label = None):
    t="  "*Gen.indentation
    if label is not None:
        t+= f"{label} = "
    if isinstance(g,Gen):
        t+= g.repr(indentDone = True)
    else:
        t+=repr(g)
    return t

class MultipleChildren(Gen):
    #@debugFun
    def __init__(self, toKeep = None,  **kwargs):
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
    def _assumeFieldFilled(self, field):
        raise ExceptionInverse(f"_assumeFieldFilled from not normal:{self}")
    def _assumeFieldEmpty(self, field):
        raise ExceptionInverse(f"_assumeFieldEmpty from not normal:{self}")
    def _assumeFieldPresent(self, field):
        raise ExceptionInverse(f"_assumeFieldPresent from not normal:{self}")
    def _assumeAnswer(self, changeStep = False):
        raise ExceptionInverse(f"_assumeAnswer from not normal:{self}")

    def _assumeFieldAbsent(self, field):
        raise ExceptionInverse(f"_assumeFieldAbsent from not normal:{self}")

    def _getQuestions(self):
        raise ExceptionInverse(f"_getQuestions from not normal:{self}")
    # def _assumeFieldInSet(self, *args, **kwargs):
    #     raise ExceptionInverse(f"_assumeFieldInSet from not normal")
    def _assumeQuestion(self, *args, **kwargs):
        raise ExceptionInverse(f"_assumeQuestion from not normal:{self}")
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse(f"_applyTag from not normal:{self}")
    def _restrictToModel(self, *args, **kwargs):
        raise ExceptionInverse(f"_restrictToModel from not normal:{self}")
    
    def _questionOrAnswer(self, *args, **kwargs):
        raise ExceptionInverse(f"_questionOrAnswer from not normal:{self}")
    
class SingleChild(MultipleChildren):
    def __init__(self, child = None, toKeep = None, **kwargs):
        self.child = child
        super().__init__(toKeep = toKeep, **kwargs)

    @debugFun
    def clone(self, elements):
        assert len(elements)==1
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
        return self.classToClone(child = child)
    
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
        return hash((self.__class__,self.child))
    
    def _repr(self):
        space = "  "*Gen.indentation
        if hasattr(self, "classToClone"):
            toClone = self.classToClone
            if toClone==self.__class__:
                className = self.__class__.__name__
            else:
                className = f"{self.__class__.__name__}/{toClone}"
        else:
            className = self.__class__.__name__
        t= f"""{className}(
{genRepr(self.child, label="child")},{self.params()})"""
        return t

    def _innerEq(self,other):
        """It may require to actually compute the child"""
        return self.getChild() == other.getChild()
    
    def _outerEq(self, other):
        return isinstance(other, SingleChild) and super()._outerEq(other)
    
    def _firstDifference(self,other):
        return self.getChild().firstDifference(other.getChild())
