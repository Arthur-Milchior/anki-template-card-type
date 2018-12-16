import sys
from ..debug import debug, assertType, debugFun
from ..utils import identity
from .ensureGen import ensureGen, addTypeToGenerator
from .constants import *


def modelToFields(model):
    """The set of fields of the model given in argument"""
    if "set of fields" not in model:
        model["set of fields"] = frozenset({fld["name"] for fld in model["flds"]})
    return model["set of fields"]

def modelToHash(model):
    """Given the model, return the hash of its set of fields."""
    return (model["name"], model["mod"])
    

#refer to README.md to understand what this class is about
class Gen:
    """
    Inheriting classes should implement: 
    - either:
    -- _callOnChildren(self, method, *args, force = True, **kwargs):
    a copy of self's class, with method called on each children.
    kwargs are passed to the method's argument.  
    - or reimplement:
    -- _computeStep(step, **kwargs): 
    --- _assumeFieldInSet(element,fieldName), assume that element
    belongs to fieldName.

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
        self.versions = dict()
        self.state = state

    def _ensureGen(self, element):
        debug(f"_ensureGen({element})",1)
        ret = ensureGen(element, self.locals_)
        debug(f"_ensureGen() returns {ret}",-1)
        return ret

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

    @debugFun
    def dontKeep(self):
        self.toKeep = False

    @debugFun
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
            key = modelToHash(model)
        elif state  ==  QUESTION_ANSWER:
            key = isQuestion
        elif state  ==  TEMPLATE_APPLIED:
            key = (asked, hide)
        else:
            raise Exception(f"State should not be {state}")
        return key
            
    @debugFun
    def computeStep(self, goal, model = None, asked = None, isQuestion = None, hide = None):
        """Compute step goal. Do the recursive computation if it is a step
        before MODEL_APPLIED.
        """
        key = Gen.getKey(goal,
                         model = model,
                         asked = asked,
                         hide = hide,
                         isQuestion = isQuestion)        
        if goal not in self.versions:
            debug(f"goal is not present in versions")
            self.versions[goal] = dict()
        else:
            debug(f"goal is present in versions")
        if key not in self.versions[goal]:
            debug(f"key is not present in versions[goal]")
            self.versions[goal][key] = self.computeMultiStep(goal, model = model, asked = asked, isQuestion = isQuestion, hide = hide)
        else:
            debug(f"key is present in versions[goal]")
        self.versions[goal][key] = self._ensureGen(self.versions[goal][key])
        return self.versions[goal][key]
    
    @debugFun
    def computeMultiStep(self, goal, model = None, asked = None, isQuestion = None, hide = None):
        currentState = self.getState()
        if self.isEmpty():
            return None
        if goal <= currentState:
            #debug("computeStep: step<=currentState, thus return self")
            return self
        previousStep = goal.previousStep()
        if currentState < previousStep:
            assert goal <= MODEL_APPLIED
            #debug("computeStep: currentState < goal.previousStep()")
            stepMinusOne = self.computeStep(goal.previousStep(),
                                            model = model,
                                            asked = asked,
                                            hide = hide,
                                            isQuestion = isQuestion)
        elif currentState == previousStep:
            #debug("computeStep: currentState == previousStep")
            stepMinusOne = self
        else:
            print(f"goal is {goal}, previousStep is {previousStep}, state is {currentState}", file=sys.stderr)
            assert False
        #debug(f"computeStep: stepMinusOne is {stepMinusOne}")
        single = stepMinusOne.computeSingleStep(goal,
                                                model = model,
                                                asked = asked,
                                                hide = hide,
                                                isQuestion = isQuestion)
        #debug(f"computeStep: single is {single}")
        return self._ensureGen(single)
            
    @debugFun
    def computeSingleStep(self, goal, model = None, asked = None, isQuestion = None, hide = None):
        """compute the next step. 

        Assume current state.successor ==goal."""
        if self.isEmpty():
            return None
        if goal == NORMAL:
            debug(f"calling _getNormalForm()")
            ret = self._getNormalForm()
        elif goal == WITHOUT_REDUNDANCY:
            debug(f"calling _getWithoutRedundance()")
            ret = self._getWithoutRedundance()
        elif goal == MODEL_APPLIED:
            debug(f"calling _restrictToModel()")
            ret = self._restrictToModel(model)
        elif goal == TEMPLATE_APPLIED:
            debug(f"calling _template()")
            ret = self._template(asked = asked,
                                 hide = hide)
        elif goal == QUESTION_ANSWER:
            debug(f"calling _questionOrAnswer()")
            ret = self._questionOrAnswer(isQuestion = isQuestion)
        else:
            raise Exception(f"self.getState() should not be {self.getState()}")
        debug(f"versions[goal][key] has been set to {ret}")
        ret = ret._ensureGen(ret)
        ret.setState(goal)
        return ret
        
    @debugFun
    def _computeStep(self, goal, **kwargs):
        #not directly called from computeGoal, but from functions _getFoo
        ret = self.callOnChildren(method = "computeStep", goal = goal, **kwargs)
        ret = self._ensureGen(ret)
        return ret


    @debugFun
    def getNormalForm(self):
        return self.computeStep(NORMAL)
    @debugFun
    def _getNormalForm(self):
        return self._computeStep(NORMAL)
    
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
        return self.computeStep(WITHOUT_REDUNDANCY)
    @debugFun
    def _getWithoutRedundance(self):
        return self._computeStep(WITHOUT_REDUNDANCY)

    @debugFun
    def restrictToModel(self,model):
        """Given the model, restrict the generator according the fields
        existing. It follows that the returned answer contains no
        requireInModel/requireAbsentOfModel requirement.

        memoized. 
        don't reimplement.
        """
        return self.computeStep(MODEL_APPLIED, model = model)
    @debugFun
    def _restrictToModel(self,model):
        return self._computeStep(MODEL_APPLIED, model = model)

    @debugFun
    def template(self, asked, hide):
        return self.computeStep(TEMPLATE_APPLIED, asked = asked, hide = hide)
    @debugFun
    def _template(self, asked = frozenset(), hide = frozenset()):
        return self._computeStep(TEMPLATE_APPLIED, asked = asked, hide = hide)

    @debugFun
    def questionOrAnswer(self, isQuestion):
        return self.computeStep(QUESTION_ANSWER, isQuestion = isQuestion)
    @debugFun
    def _questionOrAnswer(self, isQuestion):
        return self._computeStep(QUESTION_ANSWER, isQuestion = isQuestion)

    @debugFun
    def _assumeQuestion(self, isQuestion):
        return self.callOnChildren(method = "questionOrAnswer", isQuestion = isQuestion)
        
    @debugFun
    def memoize(self,method,*args, **kwargs):
        return (getattr(self,method))(*args, **kwargs)
    
    # def memoize(gen,method,*args, **kwargs):
    #     computed = False
    #     mem = None
    #     @debugFun
    #     def memoizeAux():
    #         nonlocal computed, mem
    #         if not computed:
    #             mem = (getattr(child,method))(*args, **kwargs)
    #             computed = True
    #         return mem
    #     memoize.__name__ = f"memoizeAux_of_{method}"
    #     memoize.__qualname__ = f"memoizeAux_of_{method}"
    #     return self._ensureGen(memoizeAux)
    
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
    
    @debugFun
    def assumeFieldInSet(self, field, setName):
        """return a copy of self, where the field is assumed to be in the set.
        
        Assume self and descendant unredundant and normal.
        set should be one of "Absent of model", "In model", "Empty",
        "Filled", "Remove".
        Don't redefine. Call _assumeFieldInSet
        """
        return self._assumeFieldInSet(field,setName)
    
    @debugFun
    def _assumeFieldInSet(self, field, setName):
        """Similar to assumeFieldInSet. 
        
        Recompute instead of memoizing.
        """
        return self.callOnChildren("assumeFieldInSet", field = field, setName = setName)
        
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
        raise Exception(f"""_applyTag in gen for: "{self}".""")

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
    def all(self,
            model = None,
            isQuestion = None,
            asked = frozenset(),
            hide = frozenset()):
        return self.getNormalForm(
        ).getWithoutRedundance(
        ).questionOrAnswer(
            isQuestion
        ).restrictToModel(
            model
        ).template(
            asked = asked,
            hide = hide,
        )

    def allAndTag(self,
                  tag = None,
                  soup = None,
                  model = None,
                  isQuestion = None,
                  asked = frozenset(),
                  hide = frozenset()):
        return self.all(
            model = model,
            isQuestion = isQuestion,
            asked = asked,
            hide = hide,
        ).applyTag(tag, soup)
        
addTypeToGenerator(Gen, identity)

@debugFun
def shouldBeKept(gen):
    """
    True if Gen which must be kept. 
    False if Gen which can be discarded
    None if it can't yet been known."""
    if isinstance(gen,Gen):
        return gen.toKeep
    else:
        return None
