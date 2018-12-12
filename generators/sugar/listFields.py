from .html import TR, TD
from .sugar import NotNormal
from .fields import QuestionnedField
from ...debug import debug
from ..generators import ensureGen
from .conditionals import PresentOrAbsentField, FilledOrEmptyField, AtLeastOneField
from ..children import MultipleChild, Branch

def fieldToPair(Field):
    """Given a representation of a field, returns the label to use, and the Field object"""
    if isinstance(field, str):
        return (field,field)
    elif isinstance(field,tuple) and len(field) == 2:
        (label,field) = field
        assert isinstance(field[0],str)
        if isinstance(field[1],str):
            field = Field(field)
        else:
            assert isinstance(field[1],Field)):
        return (label,field)
    elif isinstance(field,Field) :
        return (field.field, field)
    else:
        raise Exception(field)
    

class ListFields(MultipleChild, NotNormal):
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
                 **kwargs
    ):
        self.fieldsToAsk = set()
        self.originalFields = fields
        self.localFun = localFun or 
        self.globalFun = globalFun or (lambda x:x)
        self.globalSep = globalSep or (lambda x:None)
        super().__init__(
            toKeep = toKeep,
            **kwargs)
        
   def __repr__(self):
        return f"""ListFields("{self.fieldsListed}","{self.listName}","{self.localFun}","{self.globalFun}", {self.params()})"""
    
    def _getNormalForm(self):
        elements = []
        seen = []
        for field in self.fieldsListed:
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
                 localFun = None
                 globalFun = None,
                 **kwargs
    ):
        self.cascadeAsked = set()
        def localFun_(self.field):
            ret = localFun(field)
            if isinstance(ret,tuple):
                asked, ret =ret
                if asked is not None:
                    if isinstance(asked,set):
                        self.cascadeAsked|= asked
                    else:
                        self.cascadeAsked.add(asked)
            return ret
        def globalFun_(self, l):
            return Branch(name = listName,
                          default = globalFun(l),
                          cascadeAsked = self.cascadeAsked
            )
        super().__init__(fields,
                         localFun = self.localFun_,
                         globalFun = self.globalFun_,
                         listName = listName,
                         **kwargs)
    

class TableFields(ListFields):
    def __init__(self,
                 fields,
                 **kwargs):
        self.tableFields = fields
        def localFun(field):
            (label,field) = fieldToPair(field)
            return (#field.field,
                FilledField(field = field, child = TR([TD(label),TD(field)]))
                )
        def globalFun(lines):
            return HTML(tag = "table", child = lines)
        super().__init__(fields, localFun = localFun, globalFun = globalFun, **kwargs)

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
