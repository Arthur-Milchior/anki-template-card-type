class MultipleRequirement(SingleChild, NotNormal):
    """Conditional. Both about the content of the field. And the existence of the field in the model.  And request that this is a question side.


    requireFilled -- the fields which must have some content, (and thus be present in the model)
    requireEmpty -- the field must be either requireEmpty or absentOfModel of the model
    requireInModel -- the field must be present in the model. 
    requireAbsentOfModel -- the field must not belong to the model

    requirements -- the map of set to use if the other value is not explicitly given.
    """
    def __init__(self,
                 requirements = None,
                 
                 requireFilled = None,
                 requireEmpty = None,
                 requireInModel = None,
                 requireAbsentOfModel = None,
                 requireAsked = None,
                 requireNotAsked = None,
                 
                 state = BASIC,
                 **kwargs):
        self.requirements = dict()
        for (name, param) in[("requireFilled", requireFilled),
                             ("requireEmpty", requireEmpty),
                             ("requireInModel", requireInModel),
                             ("requireAsked", requireAsked),
                             ("requireNotAsked", requireNotAsked),
                             ("requireAbsentOfModel", requireAbsentOfModel)]:
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

    @debugFun
    def _getNormalForm(self):
        current = self.getChild()
        assoc = {"requireFilled":Filled,
                 "requireAsked": Asked,
                 "requireNotAsked": NotAsked,
                 "requireEmpty":Empty,
                 "requireInModel":Present,
                 "requireAbsentOfModel":Absent}
        for key in assoc:
            debug("  Considering key {key}")
            gen = assoc[key]
            for field in self.requirements[key]:
                debug("    Considering field {field}")
                current = gen(field = field, child = current)
                debug("    current now is {current}")

        return current.getNormalForm()
    
    def __eq__(self,other):
        return super().__eq__(other) and isinstance(other,Requirement) and self.requirements == other.requirements
    
    def isInconsistent(self):
        #debug("""isInconsistent("{self}")""",1)
        for left, right in [("requireFilled", "requireEmpty"), ("requireFilled", "requireAbsentOfModel"), ("requireInModel", "requireAbsentOfModel")]:
            intersection = self.requirements[left] & self.requirements[right]
            #debug("""Computing intersection of {left} and {right}, ie. "{self.requirements["requireFilled"]}" & "{self.requirements["requireEmpty"]}".""")
            if intersection:
                #debug("is not empty, thus {filledAndEmpty}, thus returning True", -1)
                return True
        #debug("""isInconsistent() returns False""",-1)
        return False
    
