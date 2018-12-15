import sys
from ..debug import debug, assertType, debugFun, identity
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
    -- getChildren (returning the list of all children. Assuming
    that the container is useless if no children are present) and
    -- _applyRecursively(self,fun,**kwargs): return a copy of self,
    with fun applied to each children. kwargs are passed to the
    function's argument.
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
        self.toKeep = toKeep
        self.versions = dict()
        self.state = state
        self.locals_ = locals_

    def _ensureGen(self, element):
        debug(f"_ensureGen({element})",1)
        ret = ensureGen(element, self.locals_)
        debug(f"_ensureGen() returns {ret}",-1)
        return ret

    def __repr__(self):
        return f"""{self.__class____name__}(without repr,{self.params()})"""
    

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
    def getState(self):
        return self.state

    @debugFun
    def isAtLeast(self,state):
        return state <= self.state
    
    @debugFun
    def isEmpty(self):
        return self.isAtLeast(EMPTY)

    @debugFun
    def isNormal(self):
        return self.isAtLeast(NORMAL)
    
    @debugFun
    def isWithoutRedundancy(self):
        return self.isAtLeast(WITHOUT_REDUNDANCY)

    @debugFun
    def getAppliedModel(self):
        if hasattr(self,"model"):
            return self.model
        return None

    @debugFun
    def isModelApplied(self):
        return self.isAtLeast(MODEL_APPLIED)
    
    @debugFun
    def isTemplateApplied(self):
        return self.isAtLeast(TEMPLATE_APPLIED)

    
    @debugFun
    def __bool__(self):
        #debug(f"""__bool__({self})""",1)
        ret = not self.isEmpty()
        #debug(f"""__bool__() returns {ret}""",-1)
        return ret
    

    @debugFun
    def shouldBeKept(self):
        """In a list, does the presence of this element justify the fact that
        this element is kept.

        It memoize, so don't call when you intend to change children.
        Implemented only for classes which can be normal.

        """
        if self.toKeep is None:
            self.toKeep = bool(self._toKeep())
        return self.toKeep

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

    @debugFun
    def getKey(state,
               model = None,
               asked = None,
               hide = None,
               isQuestion = None):
        if state == NORMAL or state == WITHOUT_REDUNDANCY:
            key = None
        elif state == MODEL_APPLIED:
            key = modelToHash(model)
        elif state  ==  TEMPLATE_APPLIED:
            key = (asked, hide, isQuestion)
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
        if key not in self.versions[goal]:
            self.versions[goal][key] = self.computeMultiStep(goal, model = model, asked = asked, isQuestion = isQuestion, hide = hide)
        self.versions[goal][key] = self._ensureGen(self.versions[goal][key])
        return self.versions[goal][key]
    
    @debugFun
    def computeMultiStep(self, goal, model = None, asked = None, isQuestion = None, hide = None):
        if goal <= self.state:
            #debug("computeStep: step<=self.state, thus return self")
            return self
        previousStep = goal.previousStep()
        if self.state < previousStep:
            assert goal <= MODEL_APPLIED
            #debug("computeStep: self.state < goal.previousStep()")
            stepMinusOne = self.computeStep(goal.previousStep(),
                                            model = model,
                                            asked = asked,
                                            hide = hide,
                                            isQuestion = isQuestion)
        elif self.state == previousStep:
            #debug("computeStep: self.state == previousStep")
            stepMinusOne = self
        else:
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
                                 hide = hide,
                                 isQuestion = isQuestion)
            
        else:
            raise Exception(f"self.state should not be {self.state}")
        debug(f"versions[goal][key] has been set to {ret}")
        ret = ret._ensureGen(ret)
        ret.setState(goal)
        return ret
        
    @debugFun
    def _computeStep(self, step, **kwargs):
        #not directly called from computeStep, but from functions _getFoo
        def computeStepAux(element):
            return element.computeStep(step, **kwargs)
        ret = self.applyRecursively(computeStepAux)
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
        on the isNormal form of self.
        
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
    def template(self, asked, hide, isQuestion):
        return self.computeStep(TEMPLATE_APPLIED, asked = asked, hide = hide, isQuestion = isQuestion)
    @debugFun
    def _template(self, asked, hide, isQuestion):
        return self._computeStep(TEMPLATE_APPLIED, asked = asked, hide = hide, isQuestion = isQuestion)

    
    @debugFun
    def assumeQuestion(self, isQuestion):
        """return a copy, where it is assumed that it is a question.
        """
        return self._assumeQuestion(isQuestion)
    
    @debugFun
    def _assumeQuestion(self, isQuestion):
        def assumeQuestionAux(element):
            return element.assumeQuestion(isQuestion)
        return self.applyRecursively(assumeQuestionAux,
                                     toClone = self)
        
    @debugFun
    def applyRecursively(self, fun, force = False, **kwargs):
        computed = False
        mem = None
        @debugFun
        def memoize(*args, **kwargs):
            nonlocal computed, mem
            if not computed:
                mem = fun(*args, **kwargs)
                computed = True
            return mem
        memoize.__name__ = f"memoizeOf_{fun.__name__}"
        fun_ = fun if force else memoize
        return self._applyRecursively(fun_, **kwargs)

    @debugFun
    def force(self):
        """Ensure that ensureGen is called on each element recursively."""
        def forceAux(element):
            return element.force()
        self.applyRecursively(forceAux, force = True)
    
    @debugFun
    def assumeFieldInSet(self, field, setName):
        """return a copy of self, where the field is assumed to be in the set.
        
        Assume self and descendant unredundant and isNormal.
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
        def assumeFieldInSetAux(element):
            return element.assumeFieldInSet(field,setName)
        return self.applyRecursively(assumeFieldInSetAux, toClone = self)
        
    @debugFun
    def applyTag(self, tag, soup):
        """Print the actual template, given the asked questions, list
        of things to hide (as frozen set)."""
        #debug (f"""template("{self}", "{tag}", "{soup}", "{isQuestion}", "{asked}", "{hide}")""",1)
        assert soup is not None
        self._applyTag(tag, soup)
        #debug (f"template()= {ret}",-1)

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
        return f"toKeep = {self.toKeep}, state = {self.state}"

    @debugFun
    def all(self, tag = None, soup = None, model = None, isQuestion =
            None, asked = frozenset(), hide = frozenset()):
        self.getNormalForm(
        ).getWithoutRedundance(
        ).restrictToModel(
            model
        ).template(
            asked = asked,
            hide = hide,
            isQuestion = isQuestion
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
