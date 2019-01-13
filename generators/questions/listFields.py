from ...debug import debug, ExceptionInverse, debugFun, assertType, debugInit, debugOnlyThisMethod
from ...utils import identity
from ..conditionals.askedOrNot import  AskedOrNot, Cascade
from ..conditionals.numberOfField import AtLeastOneField
from ..conditionals.filledOrEmpty import Filled, FilledOrEmpty
from ..conditionals.multiple import MultipleRequirement
from ..ensureGen import ensureGen
from ..generators import NotNormal, Gen, genRepr
from ..html import TR, TD, br, HTML, LI
from ..leaf import Field, ToAsk
from ..list import MultipleChildren, ListElement
from .fields import QuestionnedField, LabeledField, Label, DecoratedField

class ListFields(NotNormal):
    """
    Apply functions to each field, add separators between them, apply a function to the result

    fields -- a list of fields.
    localFun -- the function to apply to each field. Takes as argument the field, as passed in fields. return a generator to add. May return a list of fields which should be present for this line to occurs. May also return as third element of the tuple a set of questions to ask if name is asked. This set of question is also used as the set of potentially asked questions.
    globalSep -- the function to apply generate field separator. Takes as argument all the previous fields. By default, return None.
    globalFun -- the function to apply to generate the final object. Takes as argument the list of fields and separator passed as argument. By default, apply ListElement.
    name -- a name for this generator. When this name is asked, the questions returned as 3rd element by localFun are also considered to be asked
    """
    def __init__(self,
                 fields,
                 localFun = None,
                 globalSep = None,
                 globalFun = None,
                 name = None,
                 toKeep = True,
                 prefix=None,
                 suffix=None,
                 **kwargs):
        self.originalFields = fields
        self.name = name
        self.prefix=prefix
        self.suffix=suffix
        self.localFun = localFun or identity
        self.globalFun = globalFun or identity
        self.globalSep = globalSep or (lambda x:None)
        
        super().__init__(
            toKeep = toKeep,
            **kwargs)
    
    def _getNormalForm(self):
        elements = []
        seen = []
        toCascade = []
        for field in self.originalFields:
            #print(f"Considering field {field}")
            if seen:
                sep = self.globalSep(seen)
                if sep is not None:
                    elements.append(sep)
            seen.append(field)
            processedField = self.localFun(field)
            if isinstance(processedField,tuple):
                if len(processedField) is 2:
                    processedField,filledField = processedField
                    toCascadeLocal=[]
                elif len(processedField) is 3:
                    processedField,filledField, toCascadeLocal = processedField
                else:
                    assert False
            else:
                toCascadeLocal= []
                filledField = set()
            if processedField is not None:
                if filledField:
                    processedField = MultipleRequirement(
                        requireFilled=filledField,
                        child = processedField)
                elements.append(processedField)
            toCascade += toCascadeLocal
        ret = self.globalFun(elements)
        ret = [self.prefix,ret,self.suffix]
        if toCascade:
            if self.name is not None:
                ret = Cascade(field = self.name,
                              child = ret,
                              cascade = toCascade)
            ret = [ret,ToAsk(toCascade)]
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
                             classes = [fieldName]
            )
            tdLabel = TD(child = labelGen, attrs=tdLabelAttrs)
            tdField = TD(child = questionnedField, attrs = tdFieldAttrs)
            tr = TR(child = [tdLabel, tdField], attrs = trAttrs)
            return (tr,{fieldName}, {fieldName})
        @debugFun
        def globalFun(lines):
            ret=HTML(tag = "table", child = lines, attrs = attrs)
            return ret
        super().__init__(fields, localFun = localFun, globalFun = globalFun, name = name,**kwargs)

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
    def __init__(self,fieldPrefix, greater,label = None, attrs= dict(), liAttrs=dict(), unordered= False,localFun=None,globalFun=None, firstField=None,  **kwargs):
        self.fieldPrefix = fieldPrefix
        self.greater = greater
        self.attrs =attrs
        self.liAttrs= liAttrs
        self.unordered=unordered
        self.label = label if label is not None else f"{fieldPrefix}s"
        self.name = self.fieldPrefix+"s"
        assert(isinstance(fieldPrefix, str))
        assert(isinstance(greater, int))
        self.suffixes = [""]+[str(i) for i in range(2,greater+1)]
        self.numberedFields=[f"{fieldPrefix}{i}" for i in self.suffixes]
        self.firstField=fieldPrefix
        self.groupName=f"{fieldPrefix}s"
        if localFun is None:
            def localFun(i):
                field=f"""{fieldPrefix}{i}"""
                li = LI(child = QuestionnedField(field,classes=[fieldPrefix]), attrs = liAttrs)
                return (li, {field}, {field})

        if globalFun is None:
            def globalFun(lines):
                labelGen = Label(label = self.label,
                                 fields =self.numberedFields+[self.groupName],
                                 classes = [self.groupName])
                return [labelGen, ": ", HTML(tag = "ul" if unordered else "ol",child = lines, attrs = attrs)]
        
        super().__init__(fields = self.suffixes,
                         name = self.name,
                         localFun = localFun,
                         globalFun = globalFun,
                         **kwargs)

class PotentiallyNumberedFields(Cascade):
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
        nf = NumberedFields(fieldPrefix,
                            greater,
                            label = label,
                            attrs = attrs,
                            liAttrs = liAttrs)
        qu = DecoratedField(field = fieldPrefix,
                            label = label,
                            infix = infix,
                            prefix = prefix,
                            suffix = suffix)
        foe=FilledOrEmpty(field = f"""{fieldPrefix}2""",
                         filledCase = nf,
                         emptyCase = qu)
        super().__init__(child=foe,
                         cascade=[fieldPrefix],
                         field=fieldPrefix+"s")

    # def __repr__(self):
    #     return f"""PotentiallyNumberedFields() on {super().__repr__()}"""

