from bs4 import BeautifulSoup
import copy
import sys
from .generators import Gen, ensureGen, modelToFields
from .leaf import emptyGen


class SingleChild(Gen):
    def __init__(self, child, *args, **kwargs):
        self.child = ensureGen(child)
        super().__init__(*args, **kwargs)

    def getChildren(self):
        return frozenset({self.child})
    
    def __eq__(self,other):
        return isinstance(other,SingleChild) and self.child == other.child
    def _applyRecursively(self, fun, *args, **kwargs):
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
                 *args,
                 **kwargs):
        self.requirements = dict()
        for (name, param) in {("Filled",requireFilled),
                              ("Remove",requireremove),
                              ("Empty",requireEmpty),
                              ("In model",inModel),
                              ("Absent of model", absentOfModel)}:
            if param is not None:
                self.requirements[name] = frozenset(param)
            elif requirements is not None:
                self.requirements[name] = frozenset(requirements.get(name,frozenset()))
            elif toClone is not None:
                self.requirements[name] = toClone.requirements[name]
            else:
                assert False
            inconsistent = self.isInconsistent(self)
        self.requireQuestion = requireQuestion
        if inconsistent:
            print("Inconsistant requirements.",file=sys.stderr)
        super().__init__(child,
                         isEmpty = inconsistant or isEmpty,
                         toClone = toClone,
                         isNormal = isNormal or child.getIsNormal()
                         *args,
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
    
    def _applyRecursively(self, fun, *args, **kwargs):
        #used at least for _getNormalForm
        child = fun(self.child)
        if not child:
            return emptyGen
        return Requirements(child = child, toClone = self, *args, **kwargs)

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

    def restrictToModel(self,model,fields = None):
        fields = fields or modeToFields(model)
        if self.requirements["In model"] - fields or self.requirements["Absent of model"]&fields:
            return emptyGen
        child = self.child.restrictToModel(model, fields = fields)
        if not child:
            return emptyGen()
        return Requirement(child = child,
                           requirements = self.requirements,
                           requireFilled = self.requirements["Filled"],
                           requireEmpty = self.requirements["Empty"] - fields)

    
        
        
    def _template(self, tag, soup, isQuestion, *args, **kwargs):
        if self.isQuestion is not None and self.isQuestion is not isQuestion:
            return ""
        conditional_span = soup.new_tag("span", createdBy="conditionals")
        t = self.child.template( conditional_span, soup, isQuestion, *args, **kwargs)
        if not t:
            conditional_span.decompose()
            return ""
        for (set, symbol) in [
                (self.requirements["Filled"],"#"),
                (self.requirements["Empty"],"^")
        ]:
            for element in set:
                before = f"""{{{{{symbol}{element}}}}}"""
                after = f"""{{{{/{element}}}}}"""
                conditional_span.insert(0,before)
                conditional_span.append(after)
                t = f"{before}{t}{after}"
        tag.append(conditional_span)
        if self.requirements["Remove"]:
            raise Exception("Asking to require to remove something")
        if  self.requirements["In model"]:
            raise Exception("Asking to require the presence of a thing in model")
        if self.requirements["Absent of model"]:
            raise Exception("Asking to require the absence of a thing in model")
        return t, conditional_span

    

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

    def __init__(self, tag, child = None, attrs={}, toKeep = None,
                 *args, **kwargs):
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
        super().__init__(child , toKeep = toKeep, isEmpty = isEmpty, *args, **kwargs)
    
    def __repr__(self):
        return f"""HTML(child = {repr(self.child)}, tag = {self.tag}, attrs = {self.attrs()}, {self.params()})"""

    def __eq__(self,other):
        return super().__eq__(other) and isinstance(other,HTML) and self.tag == other.tag and self.attrs == other.attrs
    def _applyRecursively(self, fun, *args, **kwargs):
        child = fun(self.child, *args,**kwargs)
        if child == self.child:
            return self
        return HTML(tag, child=child, attrs=self.attrs(),toClone = self)

    def _template(self, tag, soup, *args, **kwargs):
        newtag = soup.new_tag(tag, attrs = self.attrs)
        tag = f"""<{self.tag}"""
        for param in self.attrs:
            value = self.attrs[param]
            tag+= f""" {param}="{escape(value)}" """
        
        if self.emptyTag:
            t = f"""{tag}/>"""
        else:
            t = self.child._template(newtag,soup,*args, **kwargs)
            if not t: 
                newtag.decompose()
                return ""
            t = f"""{tag}>{t}</{self.tag}>"""
        tag.append(newtag)
        return t, newtag
        
    # def _getNormalForm(self):

    #     if not child:
    #         return Literal(f"""{tag}/>""", toKeep = self.toKeep)
    #     else:
    #         return ListElement([Literal(f"""{tag}>"""),self.child,Literal(f"""</{self.tag}>""")], toKeep=self.toKeep).getNormalForm()
