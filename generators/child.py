import copy
import sys
from .generator import Gen, ensureGen, modeToFields
from .leaf import emptyGen


class SingleChild(Gen):
    def __init__(self, child, *args, **kwargs):
        self.child = ensureGen(child)
        super().__init__(*args, **kwargs)

    def getChildren(self):
        return frozenset({self.child})
    
    def _applyRecursively(self, fun, *args, **kwargs):
        return self
         
class Requirement(SingleChild):
    """Conditional. Both about the content of the field. And the existence of the field in the model.


    requireFilled -- the fields which must have some content, (and thus be present in the model)
    requireEmpty -- the field must be either requireEmpty or absentOfModel of the model
    inModel -- the field must be present in the model. 
    absentOfModel -- the field must not belong to the model
    remove -- named descendant to remove.

    requirements -- the map of set to use if the other value is not explicitly given.

    requireFilled is systematically removed from inModel, because it's redundant.
    """
    def __init__(self,
                 child,
                 requirements = None,
                 requireFilled = None,
                 requireEmpty = None,
                 inModel = None,
                 absentOfModel = None,
                 remove = None,
                 empty = None,#added to be sure not to have it in *kwargs
                 toClone = None,
                 normalized = False,
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
        if inconsistent:
            print("Inconsistant requirements.",file=sys.stderr)
        super().__init__(child,
                         empty = inconsistant or empty,
                         toClone = toClone,
                         normalized = normalized or child.isNormal()
                         *args,
                         **kwargs)
        #self.contradiction = (requireFilled & self.requirements["Absent of model"]InParent()) or (requireEmpty & self.presentInParent())

    def isInconsistent(self):
        return ((self.requirements["Filled"] & self.requirements["Empty"]) or
                (self.requirements["Filled"] & self.requirements["Absent of model"]) or
                (self.requirements["In model"] & self.requirements["Absent of model"]))
    
    def _applyRecursively(self, fun, *args, **kwargs):
        #used at least for _getNormalForm
        child = fun(self.child)
        if not child:
            return False
        return Requirements(child = child, toClone = self, *args, **kwargs)

    def _getUnRedundate(self):
        child = self.child
        for requirementName in self.requirements:
            for field in self.requirements[requirementName]:
                child = child.assumeFieldInSet(requirementName, field)
        if child == self.child:
            return self
        if not child:
            return emptyGen
        return Requirement(child = child,
                           requirements = self.requirements,
                           normalized = True,
                           unRedundanted = True)
    
    def _assumeFieldInSet(self, field, set):
        contradictorySets = {"Absent Of Model":{"Filled", "In model"},
                             "In model":{"Absent of model"},
                             "Empty":{"Filled"},
                             "Filled": {"Empty", "Absent of model"},
                             "Remove": frozenset()}
        for contradictorySet in contradictorySets[set]:
            if field in contradictorySet:
                return empty
        
        redudantSets = {"Absent Of Model":"Empty",
                        "In model":None,
                        "Empty":None,
                        "Filled":  "In model",
                        "Remove": None}
        redudantSet = redudantSets[set]
        requirements = copy.copy(self.requirements)
        change = False
        if redudantSet and field in self.requirements[redudantSet]:
            requirements[redudantSet] = requirements[redudantSet]-{field}
            change = True
        if field in self.requirements[set]:
            requirements[set] = requirements[set]-{field}
            change = True
        if change: #since self is not redundant, the removed requirement was already taken in consideration.
            child = self.child
        else:
            child = self.child.assumeFieldInSet(field,set)
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
                               normalized = True,
                               unRedundanted = True)
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

    
        
        
    def _template(self, *args, **kwargs):
        t = self.child.template(asked = asked, *args, **kwargs)
        if not t:
           return ""
        for (set, symbol) in [
                (self.requirements["Filled"],"#"),
                (self.requirements["Empty"],"^")
        ]:
            for element in set:
                t = f"{{{{{symbol}{element}}}}}{t}{{{{/{element}}}}}"
        if self.requirements["Remove"]:
            raise Exception("Asking to require to remove something")
        if  self.requirements["In model"]:
            raise Exception("Asking to require the presence of a thing in model")
        if self.requirements["Absent of model"]:
            raise Exception("Asking to require the absence of a thing in model")
        return t

    

    # def _restrictFields(self, fields, requireEmpty, hasContent):
    #     if (self.requirements["Empty"] & hasContent) or (self.requirements["Filled"] & requireEmpty) or (self.requirements["Filled"] - fields):
    #         return emptyGen
    #     considered = (requireEmpty|hasContent)
    #     childRestricted = self.child.restrictFields(fields,emptyGen|emptyGen,hasContent|requireFilled)
    #     if not childRestricted:
    #         return emptyGen
    #     return Requirements(child=childRestricted, requireFilled = self.requirements["Filled"] - considered, emptyGen = (self.requirements["Empty"] - considered) & fields, normalized = True)
    

