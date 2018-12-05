import sys
# from ..editTemplate import modelToFields
modelToId_ =dict()
modelToId_max = 0
fieldsToId_ = dict()
idToFields_ = dict()

def modelToFields(model):
    """The set of fields of the model given in argument"""
    return frozenset({f["name"] for fld in model.flds})

def fieldsToHashFields(fields):
    """A hash for this set of fields. 
    And the original saved set of fields which was used to create this hash."""
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
    pair = (model["hash"], model["mod"])
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
    --- _getUnRedundate, a method removing redundate constraint, 
    fields which can't ever appear, and things to delete. Each child
    are also unredundated.
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
                 normal = None,
                 normalized = False,
                 toKeep = None,
                 unRedundanted = False,
                 unRedundante = None,
                 empty = None,
                 toClone = None):
        """to Clone. We assume that transformations keep the fact that it
        should be kept, being normal, empty, and not redundant. Thus,
        if not otherwise stated, it is copied from toClone.

        normal and normalized should not both be given. 
        unRedundante and unRedundanted should not both be given. 
        """
        if normalized is not None:
            self.normalized = normalized
        elif toClone is not None:
            self.normalized = toClone.normalized
        else:
            self.normalized = False
                
        assert (normalized is False or normal is None)
        assert (unRedundanted is False or unRedundante is None)

        if self.normalized:
            self._normal = self
        if normal:
            self._normal = normal


        if unRedundanted is not None:
            self.unRedundanted = unRedundanted
        elif toClone is not None:
            self.unRedundanted = toClone.unRedundanted
        else:
            self.unRedundanted = False

        if toKeep is not None:
            self.__toKeep = toKeep
        elif toClone is not None:
            self.__toKeep = toClone.__toKeep
        else:
            self.__toKeep = True
            
        if empty is not None:
            self.__empty = empty
        elif toClone is not None:
            self.__empty = toClone.__empty
        else:
            self.__empty = False
        #dicts used for memoization
        self.__fieldInSets = dict()
        self.__toModels = dict()
        self.__templates = dict()

    # def __str__(self):
    #     return f"""{self.__class____name__}({self._dic()})"""
    # def _dic(self):
    #     """A dictionnary used for """
    
    def isEmpty(self):
        if self.__empty is None:
            self.__empty = self._isEmpty()
        return self.__empty
    
    def _isEmpty(self):
        for child in self.getChildren():
            if child:
                return True
        return False

    def __bool__(self):
        return not self.isEmpty()

    def toKeep(self):
        """In a list, does the presence of this element justify the fact that this element is kept.

        It memoize, so don't call when you intend to change children.
        Implemented only for classes which can be normal.
        """
        if self.__toKeep is None:
            self.__toKeep = bool(self._toKeep())
        return self.__toKeep

    def _toKeep(self):
        for element in self.getChildren():
            if element.toKeep():
                return True
        return False
    
    # def _toKeep(self):
    #     """(Re)Compute the normal form.

    #     Reimplement it in every descendants which are not already normal. 
    #     It may rise an exception if the class only generate normal elements."""
    #     raise Exception("_toKeep a Gen")

    def isNormal(self):
        return self._normalized

    def getNormalForm(self):
        """Compute the normal form, memoize it.  

        Thus, should not be called if you intend to change the
        descendant. 

        Don't reimplement this, implement _getNormalForm.
        """
        if self._normal is None:
            self._normal = self._getNormalForm()
        return self._normal
    
    def _getNormalForm(self, ):
        """(Re)Compute the normal form.
        Assuming self is not already normal, otherwise an exception may be raised."""
        return self._applyRecursively((lambda element:
                                       element._getNormalForm()),
                                      normalized = True,
                                      toClone = self)
       

    def getUnRedundate(self):
        """Remove redundant, like {{#foo}}{{#foo}}, {{#foo}}{{^foo}}
        on the normalized form of self.
        
        Memoize. Unreduntate is also set for each descendant of self.
        
        The time is square in the depth of the tree. However, a
        descendant occurring in mulitple tree to be unredundanted won't
        have to be considered multiple time, except for the elements
        which are specific to the new tree.
        """
        if self._unRedundate is None:
            self._unRedundate = self.getNormalForm()._getUnRedundate()
        return self._unRedundate
            
    def _getUnRedundate(self):
        """Similar to getUnRedundate. Assume normalized. Have to be
        reimplemented in normal form. Don't take memoization into account."""
        return self._applyRecursively( (lambda element:
                                        element._getUnRedundate()),
                                       unRedundanted = True,
                                       toClone = self)
    
    def assumeFieldInSet(self, field, setName):
        """return a copy of self, where the field is assumed to be in the set.
        
        Assume self and descendant unredundant and normalized.
        set should be one of "Absent of model", "In model", "Empty",
        "Filled", "Remove".
        Memoize. Don't redefine. Call _restrictFields
        """
        if (field,setName) not in self.__fieldInSets:
            self.__fieldInSets[(field,set)] = self.getUnRedundate()._assumeFieldInSet(field,setName)
        return self.__fieldInSets[(field,set)]
    
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
        (hash, fields) = modelToHashFields(model, fields = fields)
        if hash not in self.__models:
            self.__models[hash] = self._restrictToModel(model, fields)
        return self.__models[hash]
    
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

    #     raise an exception if the generator is not normalized.
    #     call _restrictFields, which does the actual job.
    #     Do not memoize

    #     Assume normalized."""
    #     if self.isNormal():
    #         return self._restrictFields(fields)
    #     else:
    #         raise Exception("Restricting a note not normalized",self)

    # def _restrictFields(self, fields, emptyGen, hasContent)
    #     """Similar to restrictFields, assuming normalized. This is the
    #     method which should be redefined.

    #     """
    #     raise Exception("Context from a Gen")
        
    def template(self, tag, soup, asked = None, hide = None, isQuestion = None):
        """Print the actual template, given the asked questions, list
        of things to hide (as frozen set)."""
        ret = self.__template.get(tag, soup, asked, hide, isQuestion)
        if ret is None:
            ret =self._template(tag, soup, asked, hide,isQuestion)
            self.__template[(tag,soup,asked,hide,isQuestion)] = ret
        else:
            if isinstance(ret,tuple):
                (text,tag) = ret
                ret = (text, copy.copy(tag))
        return self.__template[(tag,soup,asked,hide,isQuestion)]

    def _template(self, *args, **kwargs):
        raise Exception("_template in gen")


typeToGenerator= dict()
def addTypeToGenerator(type,generator):
    typeToGenerator[type]=generator
def ensureGen(element):
    if isinstance(element,Gen):
        return element
    for typ in typeToGenerator:
        if isinstance(ensure, str):
            return typeToGenerator[typ](ensure)
    assert False

