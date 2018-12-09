import sys
from ..debug import debug, assertType

modelToHash_ =dict()
modelToHash_max = 0
fieldsToHash_ = dict()
hashToFields_ = dict()


def modelToFields(model):
    """The set of fields of the model given in argument"""
    return frozenset({fld["name"] for fld in model["flds"]})

def fieldsToHashFields(fields):
    """A hash for this set of fields. 
    And the original saved set of fields which was used to create this hash."""
    global modelToHash_max
    hash = fieldsToHash_.get(fields)
    if hash:
        return (hash, hashToFields_[hash])
    modelToHash_max +=1
    hash = modelToHash_max
    fieldsToHash_[fields] = hash
    hashToFields_[hash] = fields
    return (hash, fields)

def modelToHashFields(model, fields = None):
    """Given the model, return the hash of its set of fields. And the set
    of fields used to create this hash originally.
    
    fields -- if given, the set of fields of the model.
    """
    pair = (model["name"], model["mod"])
    if pair in modelToHash_:
        hash = modelToHash_[pair]
        fields = hashToFields_[hash]
    else:
        fields = fields or modelToFields(model)
        (hash,fields) = fieldsToHashFields(fields)
        modelToHash_[pair] = hash
    return (hash,fields)
    

#refer to README.md to understand what this class is about
class Gen:
    """
    Inheriting classes should implement: 
    - either:
    -- getChildren (returning the list of all children. Assuming
    that the container is useless if no children are present) and
    -- _applyRecursively: which return a copy of self, with first
    argument passed to each children.
    - or reimplement:
    -- _toKeep, whether the presence of self in a list justify to keep
    the list
    -- _getNormalForm, return a generator, similar to self, composed
    only of normal generators. (It can be avoided if all object of
    this class are in normal form)
    -- If furthermore, if the class has normal objects, it should implement:
    --- _getWithoutRedundance, a method removing redundante constraint, 
    fields which can't ever appear, and things to delete. Each child
    are also unredundanted.
    --- _assumeFieldInSet, given a field and a set, assuming the field
    is in this set, return the corrected version of self
    --- _restrictToModel, remove part which are incompatible with the
    given model.

    Furthermore:
    isEmpty, returning True if the object can be deleted, (i.e. its
    text is always "" )
    _template(self,soup, tag, asked = None, hide = None, isQuestion = None):
    with soup the soup of the current xml, and tag the container
    currently processed, in which to add currently generated elements.  
    """
    def __init__(self,
                 *,
                 normalVersion = None,
                 isNormal = False,
                 toKeep = None,
                 containsRedundant = True,
                 versionWithoutRedundancy = None,
                 isEmpty = None,
                 toClone = None):
        """to Clone. We assume that transformations keep the fact that it
        should be kept, being normal, empty, and not redundant. Thus,
        if not otherwise stated, it is copied from toClone.

        normal and isNormal should not both be given. 
        versionWithoutRedundancy and containsRedundant should not both be given. 
        """
        if toClone:
            assert isinstance(toClone,Gen)
        if isNormal is not None:
            self.isNormal = isNormal
        elif toClone is not None:
            self.isNormal = toClone.isNormal
        else:
            self.isNormal = False
                
        assert (isNormal is False or normalVersion is None)
        assert ((not containsRedundant) or (versionWithoutRedundancy is None))

        if self.isNormal:
            self.normalVersion = self
        else:
            self.normalVersion = normalVersion
            assert normalVersion is None or assertType(normalVersion,Gen)


        if containsRedundant is not None:
            self.containsRedundant = containsRedundant
        elif toClone is not None:
            self.containsRedundant = toClone.containsRedundant
        else:
            self.containsRedundant = True

        if not self.containsRedundant:
            self.versionWithoutRedundancy = self
        else:
            self.versionWithoutRedundancy = versionWithoutRedundancy
            assert versionWithoutRedundancy is None or assertType(normalVersion,Gen)
            
        # if toKeep is not None:
        self.toKeep = toKeep
        # elif toClone is not None:
        #   self.toKeep = toClone.getToKeep()
        # else:
        #     self.toKeep = True
            
        # if isEmpty is not None:
        self.isEmpty = isEmpty
        # elif toClone is not None:
        #     self.isEmpty = toClone.isEmpty
        # else:
        #     self.isEmpty = None
        #dicts used for memoization
        self.fieldSetToNotRedundant = dict()
        self.hashToRestrictedModel = dict()
        self.tagAskedHideIsQuestionToTemplate = dict()
        

    # def __str__(self):
    #     return f"""{self.__class____name__}({self._dic()})"""
    # def _dic(self):
    #     """A dictionnary used for """
    # def __eq__(self,other):
    #     return self.normalVersion == other.normalVersion and self.containsRedundant == other.containsRedundant and self.isEmpty == other.isEmpty
    
    def getIsEmpty(self):
        debug(f"getIsEmpty({self})",1)
        if self.isEmpty is None:
            debug(f"whether it is empty is not yet known")
            self.isEmpty = self._getIsEmpty()
            debug(f"getIsEmpty() is {self.isEmpty}",-1)
        else:
            debug(f"whether it is empty is known to be {self.isEmpty}",-1)
            pass
        return self.isEmpty
    
    def _getIsEmpty(self):
        debug(f"_getIsEmpty({self})",1)
        ret = True
        children = self.getChildren()
        debug(f"Children are {children}")
        for child in children:
            if not child.getIsEmpty():
                debug(f"its child ({child}) is not empty. Thus self is not either.")
                ret = False
                break
            else:
                debug(f"its child ({child}) is empty")
                pass
        debug(f"self._getIsEmpty() is {ret}",-1)
        return ret

    def __bool__(self):
        debug(f"""__bool__({self})""",1)
        ret = not self.getIsEmpty()
        debug(f"""__bool__() returns {ret}""",-1)
        return ret

    def getToKeep(self):
        """In a list, does the presence of this element justify the fact that this element is kept.

        It memoize, so don't call when you intend to change children.
        Implemented only for classes which can be normal.
        """
        if self.toKeep is None:
            self.toKeep = bool(self._toKeep())
        return self.toKeep

    def _toKeep(self):
        for element in self.getChildren():
            if element.getToKeep():
                return True
        return False
    
    # def _toKeep(self):
    #     """(Re)Compute the normal form.

    #     Reimplement it in every descendants which are not already normal. 
    #     It may rise an exception if the class only generate normal elements."""
    #     raise Exception("_toKeep a Gen")

    def getIsNormal(self):
        return self.isNormal

    def getNormalForm(self):
        """Compute the normal form, memoize it.  

        Thus, should not be called if you intend to change the
        descendant. 

        Don't reimplement this, implement _getNormalForm.
        """
        #debug(f"""getNormalForm({self})""",1)
        if self.normalVersion is None:
            #debug("Normal form must be computed")
            self.normalVersion = self._getNormalForm()
            assert assertType(self.normalVersion,Gen)
        ret = self.normalVersion
        #debug(f"""getNormalForm() returns {ret}""",-1)
        return ret
    
    def _getNormalForm(self):
        """(Re)Compute the normal form.
        Assuming self is not already normal, otherwise an exception may be raised."""
        return self._applyRecursively((lambda element:
                                       element._getNormalForm()),
                                      isNormal = True,
                                      toClone = self)
       

    def getWithoutRedundance(self):
        """Remove redundant, like {{#foo}}{{#foo}}, {{#foo}}{{^foo}}
        on the isNormal form of self.
        
        Memoize. Unreduntate is also set for each descendant of self.
        
        The time is square in the depth of the tree. However, a
        descendant occurring in mulitple tree to be containsRedundant won't
        have to be considered multiple time, except for the elements
        which are specific to the new tree.
        """
        if self.versionWithoutRedundancy is None:
            normalForm = self.getNormalForm()
            if not isinstance(normalForm, Gen):
                raise Exception(f"""normalForm of "{self}" is "{normalForm}", not of type Gen""")
            self.versionWithoutRedundancy = normalForm._getWithoutRedundance()
            assert assertType(self.versionWithoutRedundancy, Gen)
        return self.versionWithoutRedundancy
            
    def _getWithoutRedundance(self):
        """Similar to getWithoutRedundance. Assume isNormal. Have to be
        reimplemented in normal form. Don't take memoization into account."""
        return self._applyRecursively((lambda element:
                                       element._getWithoutRedundance()),
                                      containsRedundant = False,
                                      toClone = self)
    
    def assumeFieldInSet(self, field, setName):
        """return a copy of self, where the field is assumed to be in the set.
        
        Assume self and descendant unredundant and isNormal.
        set should be one of "Absent of model", "In model", "Empty",
        "Filled", "Remove".
        Memoize. Don't redefine. Call _restrictFields
        """
        if (field,setName) not in self.fieldSetToNotRedundant:
            assumed = self.getWithoutRedundance()._assumeFieldInSet(field,setName)
            assert assertType(assumed, Gen)
            self.fieldSetToNotRedundant[(field,set)] = assumed
        return self.fieldSetToNotRedundant[(field,set)]
    
    def _assumeFieldInSet(self, field, setName):
        """Similar to assumeFieldInSet. 
        
        Recompute instead of memoizing.
        """
        return self._applyRecursively( (lambda element:
                                        element.assumeFieldInSet(field,set)),
                                       toClone = self)

    def restrictToModel(self,model, fields = None):
        """Given the model, restrict the generator according the fields
        existing. It follows that the returned answer contains no
        inModel/absentOfModel requirement.

        memoized. 
        don't reimplement.
        """
        debug(f"""restrictToModel({self})""",1)
        (hash, fields) = modelToHashFields(model, fields = fields)
        if hash not in self.hashToRestrictedModel:
            debug(f"""hash {hash} not memoized. It must be computed.""")
            if not self.hashToRestrictedModel:
                debug("In fact hashToRestrictedModel is empty")
            restricted = self.getWithoutRedundance()._restrictToModel(model, fields)
            assert assertType(restricted, Gen)
            self.hashToRestrictedModel[hash] = restricted
        else:
            debug(f"""hash {hash} already memoized.""")
            pass
        ret = self.hashToRestrictedModel[hash]
        debug(f"""restrictToModel() returns "{ret}".""",-1)
        return ret
    
    def _restrictToModel(self, model, fields = None):
        """Similar to restrictToModel. Do the computation and don't
        memoize. Should be implemented in inheriting normal class."""
        return self._applyRecursively( (lambda element:
                                        element.restrictToModel(model, fields = fields)), toClone = self)
    
        
    # def restrictFields(self, fields, emptyGen, hasContent)
    #     """
        
    #     fields -- if None, don't consider. Otherwise, the frozenset of fields appearing in the note type.
    #     emptyGen -- the set of fields garanteed to be emptyGen (i.e. foo, when under {{^foo}})
    #     hasContent -- the set of fields garanteed to have some content (i.e. foo, when under {{#foo}})

    #     raise an exception if the generator is not isNormal.
    #     call _restrictFields, which does the actual job.
    #     Do not memoize

    #     Assume isNormal."""
    #     if self.isNormal():
    #         return self._restrictFields(fields)
    #     else:
    #         raise Exception("Restricting a note not isNormal",self)

    # def _restrictFields(self, fields, emptyGen, hasContent)
    #     """Similar to restrictFields, assuming isNormal. This is the
    #     method which should be redefined.

    #     """
    #     raise Exception("Context from a Gen")
        
    def template(self, tag, soup, isQuestion, asked = None, hide = None):
        """Print the actual template, given the asked questions, list
        of things to hide (as frozen set)."""
        #debug (f"template({tag}, {soup}, {isQuestion} {asked}, {hide})",1)
        ret = self.tagAskedHideIsQuestionToTemplate.get((tag, asked, hide, isQuestion))
        if ret is None:
            ret =self._template(tag, soup, isQuestion, asked= asked,hide= hide)
            self.tagAskedHideIsQuestionToTemplate[(tag, asked, hide, isQuestion)] = ret
        elif isinstance(ret,tuple):
            (text,tag) = ret
            ret = (text, copy.copy(tag))
        #debug (f"template()= {ret}",-1)
        return ret

    def _template(self, tag, soup, isQuestion, asked, hide, **kwargs):
        raise Exception(f"""_template in gen for: "{self}".""")

    def __repr__(self):
        return f"Generator({self.params()})"
    
    def params(self, show = False):
        if not show:
            return ""
        if self.normalVersion == self:
            normal = "self"
        else:
            normal = repr(self.normalVersion)
        if self.versionWithoutRedundancy == self:
            versionWithoutRedundancy = "self"
        else:
            versionWithoutRedundancy = repr(self.versionWithoutRedundancy)
        return f"normal = {normal}, isNormal = {self.isNormal}, toKeep = {self.toKeep}, containsRedundant = {self.containsRedundant}, versionWithoutRedundancy = {versionWithoutRedundancy}, isEmpty = {self.isEmpty}"

typeToGenerator= dict()

def addTypeToGenerator(type,generator):
    typeToGenerator[type]=generator
    
def ensureGen(element):
    """Element if it is a Gen, or construct it. The type is chosen
    according to typeToGenerator.

    """
    #debug(f"ensureGen({element})", 1)
    ret = None
    if isinstance(element,Gen):
        #debug(f"is already a generator")
        ret = element
    for typ in typeToGenerator:
        if isinstance(element, typ):
            gen = typeToGenerator[typ]
            ret = gen(element)
            #debug(f"has type {typ}, thus use type {gen} and become {ret}")
        else:
            #debug(f"has not type {type}")
            pass
    if ret is None:
        #debug("has no type we can consider")
        assert False
    #debug("", -1)
    return ret

