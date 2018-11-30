open sys
class Gen:
    """
    self.normalized: whether the version is normalized.
    self._normal: the normal version of the generator. Access it by self.getNormalForm()
    self.__toKeep: In a list, does the presence of this element justify the fact that this element is kept. Use self.toKeep() instead.
    """

    def __init__(normalized = False, toKeep = None):
        self.normalized = normalized
        self._normal = self if normalized else None
        self.__toKeep = toKeep

    def toKeep(self):
        """In a list, does the presence of this element justify the fact that this element is kept.

        It memoize, so don't call when you intend to change children.
        Implemented only for classes which can be normal.
        """
        if self.__toKeep is None:
            self.__toKeep = self._toKeep()
        return self.__toKeep

    def isNormal(self):
        return self._normal

    def _getNormalForm(self):
        """(Re)Compute the normal form."""
        raise Exception("Normalize a Gen")
    
    def getNormalForm(self):
        """compute the normalization, memoize it.  

        Thus, should not be called if you intend to change the
        descendant.

        """
        if self._normal is None:
            self._normal = self._getNormalForm()
        return self._normal
    
    def restrictToNoteType(self,fields):
        """A copy of the current generator, restricted to fields present in
        this note type.
        
        raise an exception if the generator is not normalized.
        call restrictFields, which does the actual job
        Do not memoize

        fields -- the set of field in this note type. Should be a frozenset."""
        return 
        
    def restrictFields(self,fields,empty,hasContent)
        """
        
        fields -- if None, don't consider. Otherwise, the frozenset of fields appearing in the note type.
        empty -- the set of fields garanteed to be empty (i.e. foo, when under {{^foo}})
        hasContent -- the set of fields garanteed to have some content (i.e. foo, when under {{#foo}})

        raise an exception if the generator is not normalized.
        call _restrictFields, which does the actual job.
        Do not memoize

        Assume normalized."""
        if self.isNormal():
            return self._restrictFields(fields)
        else:
            raise Exception("Restricting a note not normalized",self)

    def _restrictFields(self,fields,empty,hasContent)
        """Similar to restrictFields, assuming normalized. This is the
        method which should be redefined.

        """
        raise Exception("Context from a Gen")
        
