from ...debug import debug, ExceptionInverse, debugFun, assertType, debugInit
from ...utils import identity
from ..conditionals.askedOrNot import  AskedOrNot, Cascade
from ..conditionals.numberOfField import AtLeastOneField
from ..conditionals.filledOrEmpty import Filled, FilledOrEmpty
from ..ensureGen import ensureGen
from ..generators import NotNormal, Gen, genRepr
from ..html import TR, TD, br, HTML, LI
from ..leaf import Field
from ..list import MultipleChildren, ListElement
from .fields import QuestionnedField, LabeledField, Label

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
    
    def _getNormalForm(self):
        elements = []
        seen = []
        toCascade = set()
        for field in self.originalFields:
            #print(f"Considering field {field}")
            if seen:
                sep = self.globalSep(seen)
                if sep is not None:
                    elements.append(sep)
            seen.append(field)
            processedField = self.localFun(field)
            if isinstance(processedField,tuple):
                processedField,toCascadeLocal = processedField
            else:
                toCascadeLocal= set()
            if processedField is not None:
                elements.append(processedField)
            toCascade |= toCascadeLocal
            #print(f"Adding {toCascadeLocal} to toCascade, it's now {toCascade}")
        #print(f"toCascade is finally {toCascade}")
        ret = self.globalFun(elements)
        if self.name is not None and toCascade:
            #print("Adding toCascade to ret")
            ret = Cascade(field = self.name,
                          child = ret,
                          cascade = toCascade)
        ret = self._ensureGen(ret)
        ret = ret.getNormalForm()
        return ret

class TableFields(ListFields):
    @debugInit
    def __init__(self,
                 fields,
                 name=None,
                 attrs = dict(),
                 trAttrs = dict(),
                 tdLabelAttrs= dict(),
                 tdFieldAttrs = dict(),
                 tdAttrs = dict(),
                 **kwargs):
        self.fields = fields
        self.attrs = attrs
        self.trAttrs = trAttrs
        self.tdLabelAttrs = tdLabelAttrs
        self.tdFieldAttrs= tdFieldAttrs
        self.tdAttrs = tdAttrs
        
        tdLabelAttrs = {**tdLabelAttrs,** tdAttrs}
        tdFieldAttrs = {**tdFieldAttrs,** tdAttrs}
        def localFun(fieldInput):
            labeledField = LabeledField(fieldInput)
            field = labeledField.field
            fieldName = field.field
            label = labeledField.label
            questionnedField = QuestionnedField(field)
            debug("""pair is "{labeledField.label}", "{fieldName}".""")
            labelGen = Label(label = label,
                             fields = [fieldName],
                             classes = ["Question",f"Question_{fieldName}"]
            )
            tdLabel = TD(child = labelGen, attrs=tdLabelAttrs)
            tdField = TD(child = questionnedField, attrs = tdFieldAttrs)
            tr = TR(child = [tdLabel, tdField], attrs = trAttrs)
            ret = Filled(
                field = fieldName,
                child = tr)
            return (ret, {fieldName})
        @debugFun
        def globalFun(lines):
            ret=HTML(tag = "table", child = lines, attrs = attrs)
            return ret
        super().__init__(fields, localFun = localFun, globalFun = globalFun, name = name)

    def _repr(self):
        t= f"""TableFields({self.fields},"""
        if self.name is not None:
            t+=genRepr(self.name,label="name")
        if self.attrs:
            t+=genRepr(self.attrs,label="attrs")
        if self.trAttrs:
            t+=genRepr(self.trAttrs,label="trAttrs")
        if self.tdLabelAttrs:
            t+=genRepr(self.tdLabelAttrs,label="tdLabelAttrs")
        if self.tdFieldAttrs:
            t+=genRepr(self.tdFieldAttrs,label="tdFieldAttrs")
        if self.tdAttrs:
            t+=genRepr(self.tdAttrs,label="tdAttrs")
        t+=")"
        return t

class NumberedFields(ListFields):
    """A list of related questions. First field is called
    fieldPrefix. Then fieldPrefix2, fieldPrefix3,... This belong to a
    question called fieldPrefixs (note the s)

    """
    def __init__(self,fieldPrefix, greater, attrs= dict(), liAttrs=dict(), unordered= False,  **kwargs):
        self.fieldPrefix = fieldPrefix
        self.greater = greater
        self.attrs =attrs
        self.liAttrs= liAttrs
        self.unordered=unordered
        self.name = self.fieldPrefix+"s"
        assert(isinstance(fieldPrefix, str))
        assert(isinstance(greater, int))
        self.numberedFields = [fieldPrefix]+[f"""{fieldPrefix}{i}""" for i in range(2,greater+1)]

        
        def localFun(field):
            li = Filled(field = field,child=LI(child = QuestionnedField(field,classes=["Answer", f"Answer_{fieldPrefix}"]), attrs = liAttrs))
            return (li, {field})
            
        def globalFun(lines):
            labelGen = Label(label = f"{fieldPrefix}s",
                             fields =self.numberedFields,
                             classes = ["Question",f"Question_{fieldPrefix}s"]
            )
            return [labelGen, ": ", HTML(tag = "ul" if unordered else "ol",child = lines, attrs = attrs)]
        
        super().__init__(fields = self.numberedFields,
                         name = self.name,
                         localFun = localFun,
                         globalFun = globalFun,
                         **kwargs)

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

