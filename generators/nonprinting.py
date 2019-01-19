from .leaf import Leaf
from .constants import *
from .generators import thisClassIsClonable
from ..debug import  debugInit, debug, debugFun

class NoPrint(Leaf):
    def _createHtml(self, soup):
        return []

class Failure(NoPrint):
    """This structure should fail if it appears at a step where it should not be exists anymore"""
    def __init__(self,last_step):
        self.last_step = last_step

    def setState(self,state):
        if state != EMPTY and self.last_step < state:
            raise Exception
        
    def _repr(self):
        return f"Failure({self.last_step})"

    def _outerEq(self,other):
        return isinstance(other,NoPrint) and self.last_step==other.last_step
    

@thisClassIsClonable
class ToAsk(NoPrint):

    """
    questionAsked -- associating a key to the set of model in which it was asked
    setQuestions -- the set of questions one may ask
"""
    @debugInit
    def __init__(self,setQuestions,*args,**kwargs):
        self.setQuestions = frozenset(setQuestions)
        self.questionsAsked = {question: frozenset() for  question in setQuestions}
        super().__init__(*args,**kwargs)

    @debugFun
    def _getQuestions(self):
        return self.setQuestions

    @debugFun
    def _getQuestionToAsk(self,model):
        for key in self.questionsAsked:
            models = self.questionsAsked[key]
            if model not in models:
                return key

        return None

    @debugFun
    def _assumeAsked(self, fields, modelName, changeState):
        for field in fields:
            if field in self.setQuestions:
                self.questionsAsked[field]|={modelName}
        return self
    
    def _repr(self):
        return f"ToAsk({self.questionsAsked})"
    
    def _outerEq(self,other):
        #For debugging purpose, we want to have an exact match, and not only on sets.
        return isinstance(other,ToAsk)

    def _innerEq(self,other):
        return True # self.questionsAsked==other.questionsAsked
    
@thisClassIsClonable
class Name(NoPrint):
    """The only purpose of this class is to return a name""" 
    def __init__(self,name):
        self.name = name

    def _getName(self):
        return name

    
    def _repr(self):
        return f"Name({self.name})"
    
    def _outerEq(self,other):
        #For debugging purpose, we want to have an exact match, and not only on sets.
        return isinstance(other,Name)

    def _innerEq(self,other):
        return True # self.questionsAsked==other.questionsAsked
    
    
