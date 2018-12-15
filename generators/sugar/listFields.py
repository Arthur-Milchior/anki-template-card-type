from .html import TR, TD
from .sugar import NotNormal
from .fields import QuestionnedField
from ...debug import debug
from ..ensureGen import ensureGen
from ..singleChild import HTML
from ..leaf import Field
from .conditionals import PresentOrAbsentField, FilledOrEmptyField, AtLeastOneField, FilledField
from ..multipleChildren import MultipleChildren
from .conditionals import Branch

def fieldToPair(field):
    """Given a representation of a field, returns the label to use, and the Field object"""
    debug("""fieldToPair({field})""",-1)
    if isinstance(field, str):
        debug("string case")
        ret = (field,Field(field))
    elif isinstance(field,tuple) and len(field) == 2:
        debug("pair case")
        (label,field) = field
        assert isinstance(field[0],str)
        if isinstance(field[1],str):
            field = Field(field)
        else:
            assert isinstance(field[1],Field)
        ret = (label,field)
    elif isinstance(field,Field) :
        debug("Field case")
        ret = (field.field, field)
    else:
        raise Exception(field)
    debug(f"""fieldToPair() returns {ret}""",-1)
    return ret
    

class ListFields(MultipleChildren, NotNormal):
    """
    Apply functions to each field, add separators between them, apply a function to the result

    fields -- a list of fields.
    localFun -- the function to apply to each field. Takes as argument the field, as passed in fields. return the object t add.
    globalSep -- the function to apply generate field separator. Takes as argument all the previous fields. By default, return None.
    globalFun -- the function to apply to generate the final object. Takes as argument the list of fields and separator passed as argument. By default, apply ListElement.
    """
    def __init__(self,
                 fields,
                 localFun = (lambda x:x),
                 globalSep = (lambda x:None),
                 globalFun = (lambda x:x),
                 toKeep = True,
                 **kwargs):
        self.originalFields = fields
        self.localFun = localFun
        self.globalFun = globalFun
        self.globalSep = globalSep
        super().__init__(
            toKeep = toKeep,
            **kwargs)

    def getChildren(self):
        return self.getNormalForm().getChildren()
    
    def __repr__(self):
        return f"""ListFields("{self.originalFields}","{self.localFun}","{self.globalSep}","{self.globalFun}", {self.params()})"""
    
    def _getNormalForm(self):
        elements = []
        seen = []
        for field in self.originalFields:
            sep = self.globalSep(seen)
            if sep is not None:
                elements.append(sep)
            seen.append(field)
            processedField = self.localFun(field)
            if processedField is not None:
                elements.append(processedField)
        elements.append(self.globalSep(seen))
        return ensureGen(self.globalFun(elements)).getNormalForm()

class ListFieldsTrigger(ListFields):
    """Similar to ListFields.

    localFun returns a pair, with a question to cascade, or None.
    Then the result is added to a Branch, with listName as name, and
    all generated elements cascading.
    """

    def __init__(self,
                 fields,
                 listName,
                 localFun = None,
                 globalFun = None,
                 **kwargs):
        self.listName = listName
        cascadeAsked = set()
        def localFun_(field):
            ret = localFun(field)
            if isinstance(ret,tuple):
                asked, ret =ret
                if asked is not None:
                    if isinstance(asked,set):
                        cascadeAsked|= asked
                    else:
                        cascadeAsked.add(asked)
            return ret
        def globalFun_(self, l):
            return Branch(name = listName,
                          default = globalFun(l),
                          cascadeAsked = cascadeAsked
            )
        self.listFields = fields
        super().__init__(fields,
                         localFun = localFun_,
                         globalFun = globalFun_,
                         **kwargs)
    
    def __repr__(self):
        return f"""ListFieldsTrigger({self.liestFields}, {self.listName}, {self.localFun}, {self.globalFun})"""

class TableFields(ListFields):
    def __init__(self,
                 fields,
                 **kwargs):
        self.tableFields = fields
        def localFun(field):
            debug(f"""TableFields.localFun({field})""",1)
            (label,field) = fieldToPair(field)
            debug(f"""pair is "{label}", "{field}".""")
            ret = (#field.field,
                FilledField(
                    field = field,
                    child = TR(
                        child = [TD(child = label),
                                 TD(child = field)]
                    )))
            debug(f"""TableFields.localFun() returns {ret}""",-1)
            return ret
        def globalFun(lines):
            debug(f"""TableFields.globalFun({lines})""",1)
            ret=HTML(tag = "table", child = lines)
            debug(f"""TableFields.globalFun() returns {ret}""", -1)
            return ret
        super().__init__(fields, localFun = localFun, globalFun = globalFun, **kwargs)
        
    def __repr__(self):
        return f"""TableFields on {super().__repr__()}"""

class NumberedFields(ListFieldsTrigger):
    
    """A list of related questions. First field is called
    fieldPrefix. Then fieldPrefix2, fieldPrefix3,... This belong to a
    question called fieldPrefixs (note the s)

    """
    def __init__(self,fieldPrefix, greater, **kwargs):
        self.fieldPrefix = fieldPrefix
        self.greater = greater
        assert(isinstance(fieldPrefix, str))
        assert(isinstance(greater, int))
        
        self.numberedFields = [fieldPrefix]+[f"""{fieldPrefix}{i}""" for i in range(2,greater+1)]
        def localFun(field):
            FilledField(field = field, child = QuestionnedField(field))
            
        def globalFun(lines):
            HTML(tag = "ul",child = lines)
        
        super().__init__(fields = self.numberedFields,
                         listName = f"""{fieldPrefix}s""",
                         localFun = localFun,
                         globalFun = globalFun,
                         **kwargs)
    def __repr__(self):
        return f"""NumberedFields("{self.fieldPrefix}","{self.greater}")"""

class PotentiallyNumberedFields(FilledOrEmptyField):
    """If the second element is present, a list is used. Otherwise, assume
no other elements are present, and show only the first element."""
    def __init__(self, fieldPrefix,greater,**kwargs):
        nf = NumberedFields(fieldPrefix,greater)
        
        super().__init__(field = f"""{fieldPrefix}2""",
                         filledCase = nf,
                         emptyCase = DecoratedField(field = fieldPrefix,
                                                    label = fieldPrefix),
                         **kwargs)

    def __repr__(self):
        return f"""PotentiallyNumberedFields() on {super().__repr__()}"""

