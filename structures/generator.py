import sys
from leaf import Literal

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
    _template(self, asked = None, hide = None, question = None):
    returning the string implementing what is wanted 
    """

    def __init__(normalized = False,
                 normal = None,
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
                
        assert (normalized is None or not normal):
        assert (unRedundante is None or not unRedundanted):

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
        """.
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
    
    def assumeFieldInSet(self, field, set):
        """return a copy of self, where the field is assumed to be in the set.
        
        Assume self and descendant unredundant and normalized.
        set should be one of "Absent of model", "In model", "Empty",
        "Filled", "Remove".
        Memoize. Don't redefine. Call _restrictFields
        """
        if (field,set) not in self.__fieldInSets:
            self.__fieldInSets[(field,set)] = self._assumeFieldInSet(field,set)
        return self.__fieldInSets[(field,set)]
    
    def _assumeFieldInSet(self, field, set):
        """Similar to assumeFieldInSet. 
        
        Recompute instead of memoizing.
        """
        return self._applyRecursively( (lambda element:
                                        element.assumeFieldInSet(field,set)),
                                       toClone = self)

    def restrictToModel(self,fields):
        """Given the model (as a set of fields), restrict the generator
        according the fields existing. It follows that the returned
        answer contains no inModel/absentOfModel requirement.

        memoized. Thus fields should be a frozenset.
        don't reimplement.
        """
        if fields not in self.__models:
            self.__models[fields] = self._restrictToModel(fields)
        raise Exception("restrictToModel a Gen")
    
    def _restrictToModel(self,fields):
        """Similar to restrictToModel. Do the computation and don't
        memoize. Should be implemented in inheriting normal class."""
        return self._applyRecursively( (lambda element:
                                        element.restrictToModel(fields)), toClone = self)
    
        
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
        
    def template(self, asked = None, hide = None, question = None):
        """Print the actual template, given the asked questions, list
        of things to hide (as frozen set)."""
        if (asked,hide, question) in self.__template:
            self.__template[(asked,hide,question)] = self._template(asked, hide,question)
        return self.__template[(asked,hide,question)]

    def _template(self, asked = None, hide = None, isQuestion = None):
        raise Exception("_template in gen")
