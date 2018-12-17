import sys
from ..debug import debug, assertType, debugFun, ExceptionInverse
from ..utils import identity
from .ensureGen import ensureGen, addTypeToGenerator
from .constants import *

def memoize(computeKey):
    def actualArobase(f):
        fname = f.__name__
        #@debugFun
        def f_(self, *args, **kwargs):
            if not hasattr(self, "versions"):
                self.versions = dict()
            if fname not in self.versions:
                self.versions[fname] = dict()
            key = computeKey(*args, **kwargs)
            if key not in self.versions:
                debug("Computation is done explicitly")
                self.versions[fname][key] = f(self, *args, **kwargs)
            else:
                debug("Computation is retrieved from memoization")
            return self.versions[fname][key]
        f_.__name__=f"Memoized_{f.__name__}"
        f_.__qualname__=f"Memoized_{f.__qualname__}"
        return f_
    return actualArobase
    

def modelToFields(model):
    """The set of fields of the model given in argument"""
    if "set of fields" not in model:
        model["set of fields"] = frozenset({fld["name"] for fld in model["flds"]})
    return model["set of fields"]

def modelToHash(model):
    """Given the model, return the hash of its set of fields."""
    return (model["name"], model["mod"])

def ensureGenAndSetState(state):
    def actualArobase(f):
        #@debugFun
        def f_(self, *args, **kwargs):
            ret = f(self, *args, **kwargs)
            ret = self._ensureGen(ret)
            ret.setState(state)
            return ret
        return f_
        f_.__name__=f"SetState({State})__{f.__name__}"
        f_.__qualname__=f"SetState({State})__{f.__qualname__}"
    return actualArobase

def emptyToEmpty(f):
    #@debugFun
    def f_(self, *args, **kwargs):
        if self.isEmpty():
            return None
        else:
            return f(self, *args, **kwargs)
    f_.__name__=f"EmptyToEmpty_{f.__name__}"
    f_.__qualname__=f"EmptyToEmpty_{f.__qualname__}"
    return f_

#refer to README.md to understand what this class is about
class Gen:
    """
    Inheriting classes should implement: 
    # - either:
    -- _callOnChildren(self, method, *args, force = True, **kwargs):
    a copy of self's class, with method called on each children.
    kwargs are passed to the method's argument.  
    -- assumeFoo: when assuming foo change the element. Otherwise, it is just called recursively on child. Leafs are returned unchanged.
    # - or reimplement:
    # -- _computeStep(step, **kwargs): 
    # --- _assumeFieldInSet(element,fieldName), assume that element
    # belongs to fieldName.

    Furthermore:
    _applyTag(self, tag, soup): edit the BeautifulSoup tag, appending the
    current object to the end of it.
    __hash__, __eq__, __repr__
    """
    #@debugFun
    def __init__(self,
                 *,
                 toKeep = None,
                 state = BASIC,
                 locals_ = None,
    ):
        self.locals_ = locals_
        self.toKeep = toKeep
        self.state = state

    #@debugFun
    def _ensureGen(self, element):
        return ensureGen(element, self.locals_)
        

    def __repr__(self):
        return f"""{self.__class__.__name__}(without repr,{self.params()})"""
    

    @debugFun
    def setState(self, state):
        """State that the state is at least state. If the state is already higher, then it is not changed. 
        Return the actual state."""
        if not hasattr(self, "state"):
            self.state = state
        else:
            self.state = self.state.union(state)
        return self.getState()
    
    @debugFun
    def clone(self,children):
        assert False

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
        #debug(f"""__bool__({self})""",1)
        ret = not self.isEmpty()
        #debug(f"""__bool__() returns {ret}""",-1)
        return ret
    

    # @debugFun
    # def shouldBeKept(self):
    #     """In a list, does the presence of this element justify the fact that
    #     this element is kept.

    #     It memoize, so don't call when you intend to change children.
    #     Implemented only for classes which can be normal.

    #     """
    #     if self.toKeep is None:
    #         self.toKeep = bool(self._toKeep())
    #     return self.toKeep

    #@debugFun
    def dontKeep(self):
        self.toKeep = False

    #@debugFun
    def doKeep(self):
        self.toKeep = True

    # @debugFun
    # def _toKeep(self):
    #     for element in self.getChildren():
    #         if element.getToKeep():
    #             return True
    #     return False

    #@debugFun
    def getKey(state,
               model = None,
               asked = None,
               hide = None,
               isQuestion = None):
        if state == NORMAL or state == WITHOUT_REDUNDANCY:
            key = None
        elif state == MODEL_APPLIED:
            assert model is not None
            key = modelToHash(model)
        elif state  ==  QUESTION_ANSWER:
            assert isinstance(isQuestion, bool)
            key = isQuestion
        elif state  ==  TEMPLATE_APPLIED:
            key = (asked, hide)
        else:
            raise ExceptionInverse(f"State should not be {state}")
        return key
            
    # @debugFun
    # def computeStep(self, goal, **kwargs):
    #     """Compute step goal. Do the recursive computation if it is a step
    #     before QUESTION_ANSWER.
    #     """
    #     key = Gen.getKey(goal, **kwargs)
    #     if goal not in self.versions:
    #         debug(f"goal is not present in versions")
    #         self.versions[goal] = dict()
    #     else:
    #         debug(f"goal is present in versions")
    #     if key not in self.versions[goal]:
    #         debug(f"key is not present in versions[goal]")
    #         self.versions[goal][key] = self.computeMultiStep(goal, **kwargs)
    #     else:
    #         debug(f"key is present in versions[goal]")
    #     self.versions[goal][key] = self._ensureGen(self.versions[goal][key])
    #     self.versions[goal][key].setState(goal)
    #     debug(f"versions[goal][key] has been set to {ret}")
    #     return self.versions[goal][key]

    def ensureSingleStep(self,goal):
        if self.getState().nextStep() < goal:
            raise ExceptionInverse(f"Can't compute {goal} from state {self.getState()} of {self}")
    
    # @debugFun
    # def computeMultiStep(self, goal, **kwargs):
    #     currentState = self.getState()
    #     if self.isEmpty():
    #         return None
    #     if goal <= currentState:
    #         #debug("computeStep: step<=currentState, thus return self")
    #         return self
    #     previousStep = goal.previousStep()
    #     if currentState < previousStep:
    #         if goal > QUESTION_ANSWER:
    #             raise ExceptionInverse(f"Trying to have goal {goal}, while at state {self.getState()} for {self}")
    #         #debug("computeStep: currentState < goal.previousStep()")
    #         stepMinusOne = self.computeStep(goal.previousStep(), **kwargs)
    #     elif currentState == previousStep:
    #         #debug("computeStep: currentState == previousStep")
    #         stepMinusOne = self
    #     else:
    #         print(f"goal is {goal}, previousStep is {previousStep}, state is {currentState}", file=sys.stderr)
    #         assert False
    #     #debug(f"computeStep: stepMinusOne is {stepMinusOne}")
    #     single = stepMinusOne.computeSingleStep(goal, **kwargs)
    #     #debug(f"computeStep: single is {single}")
    #     return self._ensureGen(single)
            
    # @debugFun
    # def computeSingleStep(self, goal, model = None, asked = None, isQuestion = None, hide = None):
    #     """compute the next step. 

    #     Assume current state.successor ==goal."""
    #     if self.isEmpty():
    #         return None
    #     if goal == NORMAL:
    #         debug(f"calling _getNormalForm()")
    #         ret = self._getNormalForm()
    #     elif goal == WITHOUT_REDUNDANCY:
    #         debug(f"calling _getWithoutRedundance()")
    #         ret = self._getWithoutRedundance()
    #     elif goal == QUESTION_ANSWER:
    #         debug(f"calling _questionOrAnswer()")
    #         ret = self._questionOrAnswer(isQuestion = isQuestion)
    #     elif goal == MODEL_APPLIED:
    #         debug(f"calling _restrictToModel()")
    #         ret = self._restrictToModel(model)
    #     elif goal == TEMPLATE_APPLIED:
    #         debug(f"calling _template()")
    #         ret = self._template(asked = asked,
    #                              hide = hide)
    #     else:
    #         raise ExceptionInverse(f"goal should not be {goal}")
    #     ret = ret._ensureGen(ret)
    #     ret.setState(goal)
    #     return ret
        
    # @debugFun
    # def _computeStep(self, goal, **kwargs):
    #     #not directly called from computeGoal, but from functions _getFoo
    #     ret = self.callOnChildren(method = "computeStep", goal = goal, **kwargs)
    #     ret = self._ensureGen(ret)
    #     return ret


    @memoize((lambda:None))
    @ensureGenAndSetState(NORMAL)
    @emptyToEmpty
    @debugFun
    def getNormalForm(self):
        self.ensureSingleStep(NORMAL)
        return self._getNormalForm()
    @debugFun
    def _getNormalForm(self):
        return self.callOnChildren(method = "getNormalForm")
    
    @memoize((lambda:None))
    @ensureGenAndSetState(WITHOUT_REDUNDANCY)
    @emptyToEmpty
    @debugFun
    def getWithoutRedundance(self):
        """Remove redundant, like {{#foo}}{{#foo}}, {{#foo}}{{^foo}}
        on the normal form of self.
        
        Memoize. Unreduntate is also set for each descendant of self.
        
        The time is square in the depth of the tree. However, a
        descendant occurring in mulitple tree to be containsRedundant won't
        have to be considered multiple time, except for the elements
        which are specific to the new tree.
        """        
        self.ensureSingleStep(WITHOUT_REDUNDANCY)
        return self._getWithoutRedundance()
    
    @debugFun
    def _getWithoutRedundance(self):
        return self.callOnChildren(method = "getWithoutRedundance")
    
    @memoize((lambda isQuestion:isQuestion))
    @ensureGenAndSetState(QUESTION_ANSWER)
    @emptyToEmpty
    @debugFun
    def questionOrAnswer(self, isQuestion):
        self.ensureSingleStep(QUESTION_ANSWER)
        return self._questionOrAnswer(isQuestion = isQuestion)
    
    @debugFun
    def _questionOrAnswer(self, isQuestion):
        if isQuestion:
            return self.assumeQuestion(changeStep = True)
        else:
            return self.assumeAnswer(changeStep = True)

    @memoize((lambda fields:fields))
    @ensureGenAndSetState(MODEL_APPLIED)
    @emptyToEmpty
    @debugFun
    def restrictToModel(self,fields):
        """Given the model, restrict the generator according the fields
        existing. It follows that the returned answer contains no
        requireInModel/requireAbsentOfModel requirement.

        memoized. 
        don't reimplement.
        """
        self.ensureSingleStep(MODEL_APPLIED)
        return self._restrictToModel(fields = fields)
    
    @debugFun
    def _restrictToModel(self,fields):
        return self.callOnChildren(method = "restrictToModel", fields = fields)

    @memoize((lambda asked, hide:(asked,hide)))
    @ensureGenAndSetState(TEMPLATE_APPLIED)
    @emptyToEmpty
    @debugFun
    def template(self, asked, hide):
        self.ensureSingleStep(TEMPLATE_APPLIED)
        return self._template(asked = asked, hide = hide)
    @debugFun
    def _template(self, asked = frozenset(), hide = frozenset()):
        return self.callOnChildren(method = "template", asked = asked, hide = hide)

    @debugFun
    def callOnChildren(self, method, *args, force = True, **kwargs):
        # memoize.__name__ = f"memoize_of_{method}"
        # memoize.__qualname__ = f"memoize_of_{method}"
        # fun_ = fun if force else memoize
        ret = self._callOnChildren(method, *args, **kwargs)
        ret = self._ensureGen(ret)
        if ret.isEmpty():
            ret = self._ensureGen(None)
        return ret
    
    @debugFun
    def _callOnChildren(self, method, *args, force = True, **kwargs):
        elements = []
        someChange = False
        for element in self.getChildren():
            newElement = (getattr(element, method))(*args, **kwargs)
            if newElement != element:
                someChange = True
            elements.append(newElement)
        if someChange:
            ret = self.clone(elements = elements)
            if ret == self:
                ret = self
        else:
            ret = self
        return ret

    @debugFun
    def force(self):
        """Ensure that ensureGen is called on each element recursively."""
        self.callOnChildren(method = "force")
    
    # @debugFun
    # def assumeFieldInSet(self, field, setName):
    #     """return a copy of self, where the field is assumed to be in the set.
        
    #     Assume self and descendant unredundant and normal.
    #     set should be one of "requireAbsentOfModel", "requireInModel", "requireEmpty",
    #     "requireFilled", "remove".
    #     Don't redefine. Call _assumeFieldInSet
    #     """
    #     return self._assumeFieldInSet(field,setName)
    
    # @debugFun
    # def _assumeFieldInSet(self, field, setName):
    #     """Similar to assumeFieldInSet. 
        
    #     Recompute instead of memoizing.
    #     """
    #     return self.callOnChildren("assumeFieldInSet", field = field, setName = setName)
    
    @emptyToEmpty
    @debugFun
    def assumeFieldFilled(self, field):
        return self._assumeFieldFilled(field)
    
    @debugFun
    def _assumeFieldFilled(self, field):
        return self.callOnChildren("assumeFieldFilled", field = field)
    
    @emptyToEmpty
    @debugFun
    def assumeFieldEmpty(self, field):
        return self._assumeFieldEmpty(field)
    @debugFun
    def _assumeFieldEmpty(self, field):
        return self.callOnChildren("assumeFieldEmpty", field = field)
        
    @emptyToEmpty
    @debugFun
    def assumeFieldPresent(self, field):
        return self._assumeFieldPresent(field)
    @debugFun
    def _assumeFieldPresent(self, field):
        return self.callOnChildren("assumeFieldPresent", field = field)
    
    @emptyToEmpty
    @debugFun
    def assumeQuestion(self, changeStep = False):
        if changeStep:
            self.setState(QUESTION_ANSWER)
        return self._assumeQuestion(changeStep = changeStep)
    @debugFun
    def _assumeQuestion(self, changeStep):
        return self.callOnChildren("assumeQuestion", changeStep = changeStep)
    
    @emptyToEmpty
    @debugFun
    def assumeAnswer(self, changeStep = False):
        return self._assumeAnswer(changeStep = changeStep)
    @debugFun
    def _assumeAnswer(self, changeStep = False):
        return self.callOnChildren("assumeAnswer", changeStep = changeStep)
        
    @emptyToEmpty
    @debugFun
    def assumeFieldAbsent(self, field):
        return self._assumeFieldAbsent(field)    
    @debugFun
    def _assumeFieldAbsent(self, field):
        return self.callOnChildren("assumeFieldAbsent", field = field)
        
    @debugFun
    def applyTag(self, tag, soup):
        """Print the actual template, given the asked questions, list
        of things to hide (as frozen set)."""
        assert soup is not None
        assert tag is not None
        assert TEMPLATE_APPLIED <= self.getState()
        self._applyTag(tag, soup)

    @debugFun
    def _applyTag(self, tag, soup):
        raise ExceptionInverse(f"""_applyTag in gen for: "{self}".""")

    def params(self, show = False):
        """The list of params as string. So that it can be printed."""
        if not hasattr(self,"toKeep"):
            self.toKeep = None
        if not hasattr(self,"state"):
            self.state = None
        if not show:
            return ""
        return f"toKeep = {self.toKeep}, state = {self.getState()}"

    @debugFun
    def compile(self,
            fields = None,
            isQuestion = None,
            asked = frozenset(),
            hide = frozenset()):
        return self.getNormalForm(
        ).getWithoutRedundance(
        ).questionOrAnswer(
            isQuestion
        ).restrictToModel(
            fields
        ).template(
            asked = asked,
            hide = hide,
        )

    def compileAndTag(self,
                      tag = None,
                      soup = None,
                      fields = None,
                      isQuestion = None,
                      asked = frozenset(),
                      hide = frozenset()):
        return self.compile(
            fields = fields,
            isQuestion = isQuestion,
            asked = asked,
            hide = hide,
        ).applyTag(tag, soup)
        
addTypeToGenerator(Gen, identity)

#@debugFun
def shouldBeKept(gen):
    """
    True if Gen which must be kept. 
    False if Gen which can be discarded
    None if it can't yet been known."""
    if isinstance(gen,Gen):
        return gen.toKeep
    else:
        return None
