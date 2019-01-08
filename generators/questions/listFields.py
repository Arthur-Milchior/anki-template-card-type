from ..html import TR, TD, br, HTML, LI
from ..generators import NotNormal, Gen
from .fields import QuestionnedField, LabeledField
from ...debug import debug, ExceptionInverse, debugFun, assertType
from ...utils import identity
from ..list import ListElement
from ..ensureGen import ensureGen
from ..leaf import Field
from ..conditionals.askedOrNot import  AskedOrNot
from ..conditionals.numberOfField import AtLeastOneField
from ..conditionals.filledOrEmpty import Filled, FilledOrEmpty
from ..list import MultipleChildren

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
                 name = None,
                 toKeep = True,
                 **kwargs):
        self.originalFields = fields
        self.name = name
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
        toCascade = set()
        for field in self.originalFields:
            if seen:
                sep = self.globalSep(seen)
                if sep is not None:
                    elements.append(sep)
            seen.append(field)
            processedField = self.localFun(field)
            if isinstance(processedField,tuple):
                processedField,toCascadeLocal = processedField
            if processedField is not None:
                elements.append(processedField)
            toCascade |= toCascadeLocal
        ret = self.globalFun(elements)
        if self.name is not None:
            ret = Cascade(name = self.name,
                          child = ret,
                          cascade = toCascade)
        ret = self._ensureGen(ret)
        ret = ret.getNormalForm()
        return ret

class TableFields(ListFields):
    @debugFun
    def __init__(self,
                 fields,
                 attrs = dict(),
                 trAttrs = dict(),
                 tdLabelAttrs= dict(),
                 tdFieldAttrs = dict(),
                 tdAttrs = dict(),
                 **kwargs):
        tdLabelAttrs = {**tdLabelAttrs,** tdAttrs}
        tdFieldAttrs = {**tdFieldAttrs,** tdAttrs}
        def localFun(field):
            field = labeledField(field)
            questionnedField = QuestionnedField(field.field)
            debug("""pair is "{field.label}", "{field.field}".""")
            labelGen = Label(label = field.label,
                             fields = [field],
                             classes = ["Question",f"Question_{field}"]
            )            
            tdLabel = TD(child = field.label, attrs=tdLabelAttrs)
            tdField = TD(child = questionnedField, attrs = tdFieldAttrs)
            tr = TR(child = [tdLabel, tdField], attrs = trAttrs)
            ret = Filled(
                field = field.field,
                child = tr)
            return (ret, {field.field})
        @debugFun
        def globalFun(lines):
            ret=HTML(tag = "table", child = lines, attrs = attrs)
            return ret
        super().__init__(fields, localFun = localFun, globalFun = globalFun)

class NumberedFields(ListFields):
    """A list of related questions. First field is called
    fieldPrefix. Then fieldPrefix2, fieldPrefix3,... This belong to a
    question called fieldPrefixs (note the s)

    """
    def __init__(self,fieldPrefix, greater, attrs= dict(), liAttrs=dict(), unordered= False, name= None,  **kwargs):
        self.fieldPrefix = fieldPrefix
        self.greater = greater
        self.attrs =attrs
        self.liAttrs= liAttrs
        self.unordered=unordered
        assert(isinstance(fieldPrefix, str))
        assert(isinstance(greater, int))
        self.numberedFields = [fieldPrefix]+[f"""{fieldPrefix}{i}""" for i in range(2,greater+1)]

        
        def localFun(field):
            li = LI(child = Filled(field = field, child = QuestionnedField(field)), attrs = liAttrs)
            return (li, field)
            
        def globalFun(lines):
            labelGen = Label(label = f"{fieldPrefix}s",
                             fields =self.numberedFields,
                             classes = ["Question"]+[f"Question_{field}" for field in self.numberedFields]
            )
            return [labelGen, ": ", HTML(tag = "ul" if unordered else "ol",child = lines, attrs = attrs)]
        
        super().__init__(fields = self.numberedFields,
                         name = name,
                         localFun = localFun,
                         globalFun = globalFun,
                         **kwargs)
    # def __repr__(self):
    #     return f"""NumberedFields("{self.fieldPrefix}","{self.greater}")"""

class PotentiallyNumberedFields(FilledOrEmpty):
    """If the second element is present, a list is used. Otherwise, assume
no other elements are present, and show only the first element."""
    def __init__(self,
                 fieldPrefix,
                 greater,
                 label = None,
                 toKeep = None,
                 attrs = dict(),
                 liAttrs = dict(),
                 suffix = br,
                 prefix = None,
                 infix = ": "):
        nf = NumberedFields(fieldPrefix,greater, label = label, attrs = attrs, liAttrs = liAttrs)
        qu = DecoratedField(field = fieldPrefix,
                            label = label,
                            infix = infix,
                            prefix = prefix,
                            suffix = suffix)
        
        super().__init__(field = f"""{fieldPrefix}2""",
                         filledCase = nf,
                         emptyCase = qu)

    # def __repr__(self):
    #     return f"""PotentiallyNumberedFields() on {super().__repr__()}"""

