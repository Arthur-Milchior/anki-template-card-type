from bs4 import BeautifulSoup, NavigableString
import copy
import sys
from .generators import Gen, ensureGen, modelToFields
from .leaf import emptyGen
from ..tag import singleTag, tagContent
from ..debug import debug, assertType

class SingleChild(Gen):
    def __init__(self, child, locals_ = None, **kwargs):
        self.child = ensureGen(child, locals_)
        super().__init__(**kwargs)

    def getChildren(self):
        return [self.child]
    
    def __eq__(self,other):
        return isinstance(other,SingleChild) and self.child == other.child
    def _applyRecursively(self, fun, **kwargs):
        return self
         
class Requirement(SingleChild):
    """Conditional. Both about the content of the field. And the existence of the field in the model.


    requireFilled -- the fields which must have some content, (and thus be present in the model)
    requireEmpty -- the field must be either requireEmpty or absentOfModel of the model
    inModel -- the field must be present in the model. 
    absentOfModel -- the field must not belong to the model
    requireQuestion -- None means, no requirement. False means: require answer. True: requires question
    remove -- named descendant to remove.

    requirements -- the map of set to use if the other value is not explicitly given.

    requireFilled is systematically removed from inModel, because it's redundant.
    """
    def __init__(self,
                 child,
                 requirements = None,
                 requireFilled = None,
                 requireEmpty = None,
                 requireQuestion = None,
                 inModel = None,
                 absentOfModel = None,
                 remove = None,
                 isEmpty = None,
                 toClone = None,
                 isNormal = False,
                 **kwargs):
        self.requirements = dict()
        for (name, param) in [("Filled",requireFilled),
                              ("Remove",remove),
                              ("Empty",requireEmpty),
                              ("In model",inModel),
                              ("Absent of model", absentOfModel)]:
            if param is not None:
                self.requirements[name] = frozenset(param)
            elif requirements is not None:
                self.requirements[name] = frozenset(requirements.get(name,frozenset()))
            elif toClone is not None and isinstance(toClone,Requirement):
                req = toClone.requirements[name]
                self.requirements[name] = req
            else:
                self.requirements[name] = frozenset()
        inconsistent = self.isInconsistent()
        self.requireQuestion = requireQuestion
        if inconsistent:
            print("Inconsistant requirements.",file=sys.stderr)
        super().__init__(child,
                         isEmpty = inconsistent or isEmpty,
                         toClone = toClone,
                         isNormal = isNormal or child.getIsNormal(),
                         **kwargs)
        #self.contradiction = (requireFilled & self.requirements["Absent of model"]InParent()) or (requireEmpty & self.presentInParent())
    
    def __repr__(self):
        return f"""Requirement(child = {repr(self.child)}, requirements = {self.requirements}, {self.params()})"""

    def __eq__(self,other):
        return super().__eq__(other) and isinstance(other,Requirement) and self.requirements == other.requirements
    
    def isInconsistent(self):
        return ((self.requirements["Filled"] & self.requirements["Empty"]) or
                (self.requirements["Filled"] & self.requirements["Absent of model"]) or
                (self.requirements["In model"] & self.requirements["Absent of model"]))
    
    def _applyRecursively(self, fun, **kwargs):
        #used at least for _getNormalForm
        child = fun(self.child)
        if not child:
            return emptyGen
        return Requirements(child = child, toClone = self, **kwargs)

    def _getWithoutRedundance(self):
        child = self.child
        for requirementName in self.requirements:
            for field in self.requirements[requirementName]:
                child = child.assumeFieldInSet(requirementName, field)
        if self.requireQuestion is not None:
            child = child.assumeFieldInSet("requireQuestion", self.requireQuestion)
        if child == self.child:
            return self
        if not child:
            return emptyGen
        return Requirement(child = child,
                           requirements = self.requirements,
                           isNormal = True,
                           containsRedundant = True)

    def _assumeQuestion(self, isQuestion):
        if self.requireQuestion is None:
            child = self.child.assumeFieldInSet(isQuestion,"isQuestion")
            if child == self.child:
                return self
            return Requirements(child = child, toClone = self)
        if self.requireQuestion is not isQuestion:
            return emptyGen
        requirements = copy.copy(self.requirements)
        requirements["requireQuestion"] = None
        return Requirements(child = self.child, requirements = requirements, toClone = self)
        
    def _assumeFieldInSet(self, field, setName):
        if setName == "requireQuestion":
            return self._assumeQuestion(field)
        contradictorySets = {"Absent Of Model":{"Filled", "In model"},
                             "In model":{"Absent of model"},
                             "Empty":{"Filled"},
                             "Filled": {"Empty", "Absent of model"},
                             "Remove": frozenset()}
        for contradictorySet in contradictorySets[setName]:
            if field in contradictorySet:
                return emptyGen
        
        redudantSets = {"Absent Of Model":"Empty",
                        "In model":None,
                        "Empty":None,
                        "Filled":  "In model",
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
                               requirements = self.requirements,
                               isNormal = True,
                               containsRedundant = True)
        else:
            return child

    def _restrictToModel(self,model,fields = None):
        #debug(f"""Requirement._restrictToModel({self},{model},{fields})""",1)
        if fields is None:
            fields =  modelToFields(model)
            #debug(f"""Fields become {fields} """)
        shouldBeInModel = self.requirements["In model"] - fields
        if shouldBeInModel:
            #debug(f"""should be in model: {shouldBeInModel}. Thus empty.""")
            return emptyGen
        shouldBeAbsent = self.requirements["Absent of model"]&fields
        if shouldBeAbsent:
            #debug(f"""should be absent: {shouldBeAbsent}. Thus empty.""")
            return emptyGen
        child = self.child.restrictToModel(model, fields = fields)
        if not child:
            #debug(f"""Child false: {child}, thus empty""")
            return emptyGen
        ret = Requirement(child = child,
                          requirements = self.requirements,
                          requireFilled = self.requirements["Filled"],
                          requireEmpty = self.requirements["Empty"] - fields)
        #debug(f"Requirement._restrictToModel() returns {ret}",-1)
        return ret

    def _template(self, tag, soup, isQuestion = None, **kwargs):
        #debug(f"""Requirement._template("{self}","{tag}","{isQuestion}",{kwargs})""",1)
        assert isinstance(isQuestion,bool)
        assert soup is not None
        conditional_span = soup.new_tag("span", createdBy="conditionals")
        #t =
        self.child.template( conditional_span, soup, isQuestion = isQuestion, **kwargs)
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
                #t = f"{before}{t}{after}"
        #debug(f"Extending {tag} by {conditional_span}")
        tag.contents.extend(conditional_span.contents)
        if self.requirements["Remove"]:
            raise Exception("Asking to require to remove something")
        if  self.requirements["In model"]:
            raise Exception("Asking to require the presence of a thing in model")
        if self.requirements["Absent of model"]:
            raise Exception("Asking to require the absence of a thing in model")
        #debug(f"",-1)
        #return t, conditional_span

    

    # def _restrictFields(self, fields, requireEmpty, hasContent):
    #     if (self.requirements["Empty"] & hasContent) or (self.requirements["Filled"] & requireEmpty) or (self.requirements["Filled"] - fields):
    #         return emptyGen
    #     considered = (requireEmpty|hasContent)
    #     childRestricted = self.child.restrictFields(fields,emptyGen|emptyGen,hasContent|requireFilled)
    #     if not childRestricted:
    #         return emptyGen
    #     return Requirements(child=childRestricted, requireFilled = self.requirements["Filled"] - considered, emptyGen = (self.requirements["Empty"] - considered) & fields, isNormal = True)
    

class HTML(SingleChild):
    """A html tag, and its content.

    A tag directly closed, such as br or img, should have child emptyGen
    (default value). Values are escaped.
    If child is an Empty object, then toKeep is assumed to be
    true."""

    def __init__(self, tag, child = None, attrs={}, toKeep = None, **kwargs):
        self.emptyTag = child is None
        if self.emptyTag:
            child = emptyGen
        self.tag = tag
        self.attrs = attrs
        if toKeep is None and not child:
            toKeep = True
            isEmpty = True
        else:
            isEmpty = False
        super().__init__(child , toKeep = toKeep, isEmpty = isEmpty, **kwargs)
    
    def __repr__(self):
        return f"""HTML(child = {repr(self.child)}, tag = {self.tag}, attrs = {self.attrs}, {self.params()})"""

    def __eq__(self,other):
        return super().__eq__(other) and isinstance(other,HTML) and self.tag == other.tag and self.attrs == other.attrs
    
    def _applyRecursively(self, fun, **kwargs):
        child = fun(self.child, **kwargs)
        if child == self.child:
            return self
        return HTML(tag, child=child, attrs=self.attrs(),toClone = self)

    def _template(self, tag, soup, **kwargs):
        newtag = soup.new_tag(tag, attrs = self.attrs)
        if self.emptyTag:
            t = singleTag(self.tag,self.attrs)
        else:
            t = tagContent(t,self.tag,self.attrs)
        tag.append(newtag)
        return t, newtag

    def _template(self, tag, soup, **kwargs):
        newtag = soup.new_tag(tag, attrs = self.attrs)
        if self.emptyTag:
            t = singleTag(self.tag,self.attrs)
        else:
            t = self.child._template(newtag,soup, **kwargs)
            if not t: 
                newtag.decompose()
                return "", NavigableString("")
            t = tagContent(self.tag, self.attrs, t)
        tag.append(newtag)
        return t, newtag
        
    # def _getNormalForm(self):

    #     if not child:
    #         return Literal(f"""{tag}/>""", toKeep = self.toKeep)
    #     else:
    #         return ListElement([Literal(f"""{tag}>"""),self.child,Literal(f"""</{self.tag}>""")], toKeep=self.toKeep).getNormalForm()
