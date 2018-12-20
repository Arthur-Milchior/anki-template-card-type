from ..html import TR, TD
from .sugar import NotNormal
from .fields import QuestionnedField
from ...debug import debug, ExceptionInverse, debugFun, assertType
from ...utils import identity
from ..ensureGen import ensureGen
from ..singleChild import Filled
from ..html import HTML, LI
from ..leaf import Field
from .conditionals import FilledOrEmpty, AskedOrNot
from .numberOfField import AtLeastOneField
from ..multipleChildren import MultipleChildren
from .conditionals import Branch

@debugFun
def fieldToPair(field):
    """Given a representation of a field, returns the label to use, and the Field object"""
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
        raise ExceptionInverse(field)
    # (label,field) =ret
    # assert assertType(label, str)
    # assert assertType(field, Field)
    # assert assertType(field.field, str)
    return ret
    

class ListFields(NotNormal):
    """
    Apply functions to each field, add separators between them, apply a function to the result

    fields -- a list of fields.
    localFun -- the function to apply to each field. Takes as argument the field, as passed in fields. return the object t add.
    globalSep -- the function to apply generate field separator. Takes as argument all the previous fields. By default, return None.
    globalFun -- the function to apply to generate the final object. Takes as argument the list of fields and separator passed as argument. By default, apply ListElement.
    """
    def __init__(self,
                 fields,
                 localFun = None,
                 globalSep = None,
                 globalFun = None,
                 toKeep = True,
                 **kwargs):
        self.originalFields = fields
        self.localFun = localFun or identity
        self.globalFun = globalFun or identity
        self.globalSep = globalSep or (lambda x:None)
        
        super().__init__(
            toKeep = toKeep,
            **kwargs)
    
    # def __repr__(self):
    #     return f"""ListFields("{self.originalFields}","{self.localFun}","{self.globalSep}","{self.globalFun}", {self.params()})"""
    
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
        globalApplied = self.globalFun(elements)
        globalEnsured = ensureGen(globalApplied)
        return globalEnsured.getNormalForm()

class NamedListFields(AskedOrNot):
    """Similar to ListFields.

    similar to ListField, where localFun depends on whether listName is asked or not.
    """

    def __init__(self,
                 fields,
                 listName,
                 localAskedFun = None,
                 localDefaultFun = None,
                 globalSep = None,
                 globalFun = None,
                 **kwargs):
        self.listName = listName
        self.listFields = fields
        self.localAskedFun = localAskedFun
        self.localDefaultFun = localDefaultFun
        self.globalSep = globalSep
        self.globalFun = globalFun
        asked = ListFields(self.listFields, localFun = self.localAskedFun, globalFun = self.globalFun, globalSep = self.globalSep)
        notAsked = ListFields(self.listFields, localFun = self.localDefaultFun, globalFun = self.globalFun, globalSep = self.globalSep)
        return super().__init__(field = self.listName,
                                asked = asked,
                                notAsked = notAsked,
        )
        
    
    # def __repr__(self):
    #     return f"""ListFieldsTrigger({self.liestFields}, {self.listName}, {self.localFun}, {self.globalFun})"""

class TableFields(ListFields):
    def __init__(self,
                 fields,
                 **kwargs):
        self.tableFields = fields
        def localFun(field):
            debug("""TableFields.localFun({field})""",1)
            (label,field) = fieldToPair(field)
            questionnedField = QuestionnedField(field)
            debug("""pair is "{label}", "{field}".""")
            tdLabel = TD(child = label)
            tdField = TD(child = questionnedField)
            tr = TR(child = [tdLabel, tdField])
            ret = Filled(
                field = field.field,
                child = tr)
            debug("""TableFields.localFun() returns {ret}""",-1)
            return ret
        def globalFun(lines):
            debug("""TableFields.globalFun({lines})""",1)
            ret=HTML(tag = "table", child = lines)
            debug("""TableFields.globalFun() returns {ret}""", -1)
            return ret
        super().__init__(fields, localFun = localFun, globalFun = globalFun, **kwargs)
        
    # def __repr__(self):
    #     return f"""TableFields on {super().__repr__()}"""

class NumberedFields(NamedListFields):
    
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
        def localAskedFun(field):
            return LI(child = Filled(field = field, child = QuestionnedField(field).assumeAsked(field)))
        def localDefaultFun(field):
            return LI(child = Filled(field = field, child = QuestionnedField(field)))
            
        def globalFun(lines):
            return [f"{fieldPrefix}s", ": ", HTML(tag = "ul",child = lines)]
        
        super().__init__(fields = self.numberedFields,
                         listName = f"""{fieldPrefix}s""",
                         localAskedFun = localAskedFun,
                         localDefaultFun = localDefaultFun,
                         globalFun = globalFun,
                         **kwargs)
    # def __repr__(self):
    #     return f"""NumberedFields("{self.fieldPrefix}","{self.greater}")"""

class PotentiallyNumberedFields(FilledOrEmpty):
    """If the second element is present, a list is used. Otherwise, assume
no other elements are present, and show only the first element."""
    def __init__(self, fieldPrefix, greater,**kwargs):
        nf = NumberedFields(fieldPrefix,greater)
        
        super().__init__(field = f"""{fieldPrefix}2""",
                         filledCase = nf,
                         emptyCase = DecoratedField(field = fieldPrefix,
                                                    label = fieldPrefix),
                         **kwargs)

    # def __repr__(self):
    #     return f"""PotentiallyNumberedFields() on {super().__repr__()}"""

