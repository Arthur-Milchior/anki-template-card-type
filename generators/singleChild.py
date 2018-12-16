from bs4 import BeautifulSoup, NavigableString
import copy
import sys
from .constants import *
from .generators import Gen, modelToFields, shouldBeKept
from .leaf import emptyGen
from ..tag import singleTag, tagContent
from ..debug import debug, assertType, debugFun
from .multipleChildren import MultipleChildren

class SingleChild(MultipleChildren):
    def __init__(self, child = None, toKeep = None, **kwargs):
        self.child = child
        super().__init__(toKeep = toKeep, **kwargs)

    def getChild(self):
        if not isinstance(self.child, Gen):
            self.child = self._ensureGen(self.child)
        return self.child
        
    def getChildren(self):
        return [self.getChild()]
    
    def __eq__(self,other):
        """It may require to actually compute the child"""
        return isinstance(other,SingleChild) and self.getChild() == other.getChild()
    
class HTML(SingleChild):
    """A html tag, and its content.

    A tag directly closed, such as br or img, should have child emptyGen
    (default value). Values are escaped.
    If child is an Empty object, then toKeep is assumed to be
    true."""

    def __init__(self,
                 tag = None,
                 attrs={},
                 **kwargs):
        assert assertType(tag,str)
        self.tag = tag
        self.attrs = attrs
        super().__init__(**kwargs)
        if self.child is None:
            self.doKeep()
        self.emptyTag = self.child is None

    def clone(self, elements):
        assert len(elements)==1
        element = elements[0]
        if element == self.child:
            return self
        return HTML(tag = self.tag,
                    attrs = self.attrs,
                    child = element)
    
    def __repr__(self):
        return f"""HTML(child = {repr(self.child)}, tag = "{self.tag}", attrs = "{self.attrs}", {self.params()})"""

    def __eq__(self,other):
        return super().__eq__(other) and isinstance(other,HTML) and self.tag == other.tag and self.attrs == other.attrs

    @debugFun
    def _applyTag(self, tag, soup):
        #debug(f"self.tag = {self.tag}")
        #debug(f"self.attrs = {self.attrs}")
        newtag = soup.new_tag(self.tag, **self.attrs)
        #debug(f"New tag is {newtag}")
        if not self.emptyTag:
            self.child.applyTag(newtag, soup)
        #debug(f"New tag became {newtag}")
        tag.append(newtag)
        #debug(f"Tag became {tag}")
         
class Requirement(SingleChild):
    """Conditional. Both about the content of the field. And the existence of the field in the model. Also allow to remove a child. And request that this is a question side.


    requireFilled -- the fields which must have some content, (and thus be present in the model)
    requireEmpty -- the field must be either requireEmpty or absentOfModel of the model
    requireInModel -- the field must be present in the model. 
    requireAbsentOfModel -- the field must not belong to the model
    remove -- named descendant to remove.

    requirements -- the map of set to use if the other value is not explicitly given.
    """
    def __init__(self,
                 requirements = None,
                 
                 requireFilled = None,
                 requireEmpty = None,
                 requireInModel = None,
                 requireAbsentOfModel = None,
                 remove = None,
                 
                 state = BASIC,
                 **kwargs):
        self.requirements = dict()
        for (name, param) in[("Filled",requireFilled),
                             ("Remove",remove),
                             ("Empty",requireEmpty),
                             ("In model",requireInModel),
                             ("Absent of model", requireAbsentOfModel)]:
            default = frozenset()
            fun = frozenset
            if param is not None:
                self.requirements[name] = fun(param)
            elif requirements is not None:
                self.requirements[name] = fun(requirements.get(name,default))
            else:
                self.requirements[name] = default
        inconsistent = self.isInconsistent()
        if inconsistent:
            print("Inconsistent requirements.",file=sys.stderr)
            state = EMPTY
        super().__init__(state = state,
                         **kwargs)

    def clone(self, elements):
        assert len(elements) ==1
        element = elements[0]
        if element == self.child:
            return self
        return Requirement(requirements = self.requirements,
                           child = element)
        
    
    def __repr__(self):
        t = f"""Requirement(child = {self.child}"""
        for key in self.requirements:
            t+=f", {key}={self.requirements[key]}"
        t+=f", {self.params()})"
        return t

    def __eq__(self,other):
        return super().__eq__(other) and isinstance(other,Requirement) and self.requirements == other.requirements
    
    def isInconsistent(self):
        #debug(f"""isInconsistent("{self}")""",1)
        for left, right in [("Filled", "Empty"), ("Filled", "Absent of model"), ("In model", "Absent of model")]:
            intersection = self.requirements[left] & self.requirements[right]
            #debug(f"""Computing intersection of {left} and {right}, ie. "{self.requirements["Filled"]}" & "{self.requirements["Empty"]}".""")
            if intersection:
                #debug(f"is not empty, thus {filledAndEmpty}, thus returning True", -1)
                return True
        #debug(f"""isInconsistent() returns False""",-1)
        return False
            
        
    def _getWithoutRedundance(self):
        child = self.child
        for requirementName in ["Filled", "Remove", "Empty", "In model", "Absent of model"]:
            for field in self.requirements[requirementName]:
                child = child.assumeFieldInSet(field, requirementName)
        if child == self.child:
            self.setState(WITHOUT_REDUNDANCY)
            return self
        if not child:
            return emptyGen
        return Requirement(child = child,
                           requirements = self.requirements,
                           state = WITHOUT_REDUNDANCY)
        
    def _assumeFieldInSet(self, field, setName):
        contradictorySets = {"Absent Of Model":{"Filled", "In model"},
                             "In model":{"Absent of model"},
                             "Empty":{"Filled"},
                             "Filled": {"Empty", "Absent of model"},
                             "Remove": frozenset()}
        for contradictorySet in contradictorySets[setName]:
            if field in contradictorySet:
                return emptyGen
        
        redudantSets = {"Absent Of Model":"Empty",
                        "In model": None,
                        "Empty": None,
                        "Filled": "In model",
                        "Remove": None}
        redudantSet = redudantSets[setName]
        requirements = copy.copy(self.requirements)
        change = False
        if redudantSet and field in self.requirements[redudantSet]:
            requirements[redudantSet] = requirements[redudantSet]-{field}
            change = True
        if field in self.requirements[setName]:
            requirements[setName] = requirements[setName]-{field}
            change = True
        if change: #since self is not redundant, the removed requirement was already taken in consideration.
            child = self.child
        else:
            child = self.child.assumeFieldInSet(field,setName)
            if not child:
                return emptyGen
            if child == self.child:
                return self
        if (requirements["Filled"] or
            requirements["Empty"] or
            requirements["In model"] or
            requirements["Absent of model"] or
            requirements["Remove"]):
            return Requirement(child = child,
                               requirements = self.requirements)
        else:
            return child

    @debugFun
    def _restrictToModel(self,model):
        fields = modelToFields(model)
        #debug(f"""Requirement._restrictToModel({self},{model},{fields})""",1)
        if fields is None:
            fields =  modelToFields(model)
            #debug(f"""Fields become {fields} """)
        shouldBeInModel = self.requirements["In model"] - fields
        if shouldBeInModel:
            #debug(f"""should be in model: {shouldBeInModel}. Thus empty.""")
            return emptyGen
        cantBiFilledIfAbsent = self.requirements["Filled"] - fields
        if cantBiFilledIfAbsent:
            #debug(f"""should be in model: {cantBiFilledIfAbsent}. Thus empty.""")
            return emptyGen
        shouldBeAbsent = self.requirements["Absent of model"]&fields
        if shouldBeAbsent:
            #debug(f"""should be absent: {shouldBeAbsent}. Thus empty.""")
            return emptyGen
        child = self.child.restrictToModel(model)
        if not child:
            #debug(f"""Child false: {child}, thus empty""")
            return emptyGen
        ret = Requirement(child = child,
                          requireFilled = self.requirements["Filled"],
                          requireEmpty = self.requirements["Empty"] & fields,
                          remove =  self.requirements["Remove"])
        #debug(f"Requirement._restrictToModel() returns {ret}",-1)
        return ret

    def _applyTag(self, tag, soup):
        assert soup is not None
        conditional_span = soup.new_tag(f"span", createdBy="conditionals")
        self.child.applyTag(conditional_span, soup)
        for (set, symbol) in [
                (self.requirements["Filled"],"#"),
                (self.requirements["Empty"],"^")
        ]:
            for element in set:
                before = NavigableString(f"""{{{{{symbol}{element}}}}}""")
                after = NavigableString(f"""{{{{/{element}}}}}""")
                #debug(f"Enclosing {conditional_span} by {before}/{after}")
                conditional_span.insert(0,before)
                conditional_span.append(after)
        #debug(f"Extending {tag} by {conditional_span}")
        tag.contents.extend(conditional_span.contents)
        if self.requirements["Remove"]:
            raise Exception(f"Asking to require to remove something")
        if  self.requirements["In model"]:
            raise Exception(f"Asking to require the presence of a thing in model")
        if self.requirements["Absent of model"]:
            raise Exception(f"Asking to require the absence of a thing in model")
