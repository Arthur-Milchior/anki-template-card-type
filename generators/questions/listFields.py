from ...debug import (ExceptionInverse, assertType, debug, debugFun, debugInit,
                      debugOnlyThisMethod)
from ...utils import checkField, identity
from ..conditionals.askedOrNot import AskedOrNot, Cascade
from ..conditionals.filledOrEmpty import Filled, FilledOrEmpty
from ..conditionals.hide import HideInSomeQuestions, ShowIfAskedOrAnswer
from ..conditionals.multiple import MultipleRequirement
from ..conditionals.numberOfField import AtLeastOneField
from ..conditionals.questionOrAnswer import QuestionOrAnswer
from ..ensureGen import ensureGen
from ..generators import Gen, NotNormal, genRepr
from ..html.atom import *
from ..html.html import *
from ..leaf import Field
from ..listGen import ListElement, MultipleChildren
from ..nonprinting import ToAsk
from .fields import DecoratedField, Label, QuestionnedField


class ListFields(ListElement):
    """
    Apply functions to each field, add separators between them, apply a function to the result

    fields -- a list of fields.
    localFun -- the function to apply to each field. Takes as argument the field, as passed in fields. return a generator to add. May return a list of fields which should be present for this line to occurs. May also return as third element of the tuple a set of questions to ask if name is asked. This set of question is also used as the set of potentially asked questions.
    globalSep -- the function to apply generate field separator. Takes as argument all the previous fields. By default, return None.
    globalFun -- the function to apply to generate the final object. Takes as argument the list of fields and separator passed as argument. By default, apply ListElement.
    name -- a name for this generator. When this name is asked, the questions returned as 3rd element by localFun are also considered to be asked
    groupSize -- stating that each subgroup containing elements groupSize*n up to groupSize *(n+1) -1 belongs to a single subgroup
    applyToGroup -- a method applied to each subgroup, with second argument the index of the subgroup
    """

    def __init__(self,
                 fields,
                 localFun=None,
                 globalSep=None,
                 globalFun=None,
                 name=None,
                 toKeep=True,
                 prefix=None,
                 suffix=None,
                 applyToGroup=None,
                 groupSize=None,
                 **kwargs):
        self.originalFields = fields
        self.name = name
        self.prefix = prefix
        self.suffix = suffix
        self.localFun = localFun or identity
        self.globalFun = globalFun or identity
        self.globalSep = globalSep or (lambda x: None)
        elements = []
        self.processedInputs = []  # List of inputs seen
        self.potentiallyFilledFields = []
        toCascade = set()
        for field in self.originalFields:
            #print(f"Considering field {field}")
            if self.processedInputs:
                sep = self.globalSep(self.processedInputs)
                if sep is not None:
                    elements.append(sep)
            self.processedInputs.append(field)
            processedFieldDic = self.localFun(field)
            if isinstance(processedFieldDic, str):
                processedFieldDic = {"child": processedField}
            processedField = processedFieldDic["child"]
            filledFields = processedFieldDic.get("filledFields", [])
            if isinstance(filledFields, str):
                checkField(filledFields)
                filledFields = [filledFields]
            else:
                assert assertType(filledFields, list)
                for field in filledFields:
                    checkField(field)
            toCascadeLocal = processedFieldDic.get("questions", frozenset())
            hideFields = processedFieldDic.get(
                "hideInSomeQuestions", frozenset())
            showIfAskedOrAnswer = processedFieldDic.get(
                "showIfAskedOrAnswer", False)
            if not processedField:
                continue
            if filledFields:
                processedField = AtLeastOneField(
                    fields=filledFields,
                    child=processedField)
                self.potentiallyFilledFields.extend(filledFields)
            if hideFields:
                processedField = HideInSomeQuestions(
                    hideFields, processedField)
            if showIfAskedOrAnswer:
                processedField = ShowIfAskedOrAnswer(
                    showIfAskedOrAnswer, processedField)
            elements.append(processedField)
            toCascade |= toCascadeLocal

        elements_ = []
        if applyToGroup and groupSize:
            i = 0
            while elements:
                subgroup = elements[:groupSize]
                elements = elements[groupSize:]
                elements_.append(applyToGroup(subgroup, i))
                i += 1
            elements = elements_

        ret = self.globalFun(elements)
        if self.suffix:  # This ensure that we don't use the big AtLeastOneField on an empty suffix
            self.suffix = AtLeastOneField(
                self.suffix, self.potentiallyFilledFields)
        ret = [self.prefix, ret, self.suffix]
        if toCascade:
            if self.name is not None:
                ret = Cascade(field=self.name,
                              child=ret,
                              cascade=toCascade)
            super().__init__([ret, ToAsk(toCascade)], toKeep=toKeep, **kwargs)
        else:
            super().__init__(ret, toKeep=toKeep, **kwargs)

"""A  dic may contain:
field - the field name
"hideInSomeQuestion -- set of fields. When one of this field is asked, the question side should not be shown. This ensure that a similar field does not give too good of a hint (e.g. when asking for variance, hide the standard deviation)
child -- an initial version of the child. It may be modified to add conditionals on it
???
"""
            
class TableFields(ListFields):
    @debugInit
    def __init__(self,
                 fields,
                 name=None,
                 attrs=dict(),
                 trAttrs=dict(),
                 tdLabelAttrs=dict(),
                 tdFieldAttrs=dict(),
                 tdAttrs=dict(),
                 greater=1,
                 isMandatory=True,
                 useClasses=True,
                 defaultClasses=None,
                 header_decoration=H3,
                 label=None,
                 answer=None,
                 emphasizing=(lambda x:x),
                 numbered_field=None,
                 **kwargs):
        self.fields = []
        if numbered_field is None:
            assert greater == 1
            def numbered_field(field, i):
                return field
        for field_s in fields:
            if isinstance(field_s, list):
                group = set()
                for field in field_s:
                    if isinstance(field, str):
                        group.add(field)
                    else:
                        assert isinstance(field, dict)
                        assert "field" in field
                        group.add(field["field"])
                for field in field_s:
                    if isinstance(field, str):
                        d = {"field": field}
                    elif isinstance(field, dict):
                        d = field
                    else:
                        assert False
                    d["hideInSomeQuestions"] = group - {d["field"]}
                    self.fields.append(d)
            else:
                self.fields.append(field_s)
        self.attrs = attrs
        self.greater = greater
        self.trAttrs = trAttrs
        self.tdLabelAttrs = tdLabelAttrs
        self.tdFieldAttrs = tdFieldAttrs
        self.tdAttrs = tdAttrs

        tdLabelAttrs = {**tdLabelAttrs, ** tdAttrs}
        tdFieldAttrs = {**tdFieldAttrs, ** tdAttrs}

        def localFun(fieldInputDic):
            ret = dict()
            # Ensuring the input is a dic
            if isinstance(fieldInputDic, str):
                fieldInputDic = {"field": fieldInputDic}
            assert assertType(fieldInputDic, dict)

            fieldName = fieldInputDic["field"]
            label = fieldInputDic.get("label", f"{fieldName}:")

            # Choosing the class to apply
            if "classes" in fieldInputDic:
                classes = fieldInputDic["classes"]
            elif defaultClasses is not None:
                classes = defaultClasses
            elif useClasses:
                classes = fieldName
            else:
                classes = []

            # The label
            labelGen = Label(label=label,
                             fields=[fieldName],
                             emphasizing=emphasizing,
                             classes=classes
                             )
            tdLabel = header_decoration(child=labelGen, attrs=tdLabelAttrs)

            # The fields
            def tdField(i=1):
                """Returns the entry for the current question i-th column."""
                fieldName_ = numbered_field(fieldName, i)
                if "function" in fieldInputDic:
                    child = fieldInputDic["function"](i)
                else:
                    child = Field(fieldName_,
                                  isMandatory=isMandatory,
                                  useClasses=False)
                if "emptyCase" in fieldInputDic:
                    child = FilledOrEmpty(fieldName_,
                                          child,
                                          fieldInputDic["emptyCase"])
                questionnedField = QuestionnedField(fieldName_,
                                                    child=child,
                                                    isMandatory=isMandatory,
                                                    useClasses=useClasses,
                                                    emphasizing=emphasizing,
                                                    classes=classes)
                td = SPAN(child=questionnedField, attrs=tdFieldAttrs)
                if not answer:
                    return td
                answerField = f"{fieldName}{answer}"
                answerQuestionned = QuestionnedField(answerField,
                                                     useClasses=useClasses,
                                                     emphasizing=emphasizing,
                                                     classes=classes)
                answerTd = SPAN(child=answerQuestionned,
                              attrs=tdFieldAttrs)
                return QuestionOrAnswer(td, [td, answerTd])

            trChild = P([tdLabel, tdField()]+[[br,tdField(i)]
                                            for i in range(2, self.greater+1)])

            # The whole line
            ret["child"] = SPAN(child=trChild,
                              attrs=trAttrs)
            indexes = range(1, self.greater+1)
            name = fieldInputDic["field"]
            defaultList = [numbered_field(name, i) for i in indexes]
            defaultSet = set(defaultList)
            ret["questions"] = fieldInputDic.get("questions", defaultSet)

            # filledFields
            if "filledFields" in fieldInputDic:
                ret["filledFields"] = fieldInputDic["filledFields"]
            elif "emptyCase" in fieldInputDic:
                ret["filledFields"] = []
            else:
                ret["filledFields"] = defaultList

            ret["hideInSomeQuestions"] = fieldInputDic.get(
                "hideInSomeQuestions", frozenset())
            if fieldInputDic.get("showIfAskedOrAnswer"):
                ret["showIfAskedOrAnswer"] = fieldName
            return ret

        @debugFun
        def globalFun(lines):
            ret = SPAN(lines, attrs=attrs, )
            return ret
        super().__init__(self.fields,
                         localFun=localFun,
                         globalFun=globalFun,
                         name=name,
                         **kwargs)

    def _repr(self):
        t = f"""TableFields({self.fields},"""
        if self.name is not None:
            t += genRepr(self.name, label="name")
        if self.attrs:
            t += genRepr(self.attrs, label="attrs")
        if self.trAttrs:
            t += genRepr(self.trAttrs, label="trAttrs")
        if self.tdLabelAttrs:
            t += genRepr(self.tdLabelAttrs, label="tdLabelAttrs")
        if self.tdFieldAttrs:
            t += genRepr(self.tdFieldAttrs, label="tdFieldAttrs")
        if self.tdAttrs:
            t += genRepr(self.tdAttrs, label="tdAttrs")
        t += ")"
        return t


class NumberedFields(ListFields):
    """A list of related questions. First field is called
    fieldPrefix. Then fieldPrefix2, fieldPrefix3,... This belong to a
    question called fieldPrefixs (note the s)

    """

    def __init__(self,
                 fieldPrefix,
                 greater,
                 numbered_field,
                 label=None,
                 attrs=dict(),
                 liAttrs=dict(),
                 unordered=False,
                 localFun=None,
                 globalFun=None,
                 emphasizingField=None,
                 firstField=None,
                 smaller=1,
                 isMandatory=True,
                 useClasses=True,
                 classes=None,
                 **kwargs):
        self.fieldPrefix = fieldPrefix
        self.greater = greater
        self.attrs = attrs
        self.liAttrs = liAttrs
        self.unordered = unordered
        self.plural = f"{fieldPrefix}s"
        self.label = label if label is not None else self.plural
        assert(isinstance(fieldPrefix, str))
        assert(isinstance(greater, int))
        self.suffixes = [i for i in range(smaller, greater+1)]
        self.numberedFields = [numbered_field(fieldPrefix, i) for i in self.suffixes]
        self.firstField = fieldPrefix
        self.groupName = f"{fieldPrefix}s"
        if classes is None:
            classes = fieldPrefix
        if localFun is None:
            def localFun(i):
                field = numbered_field(fieldPrefix, i)
                li = LI(child=QuestionnedField(field,
                                               isMandatory=isMandatory,
                                               useClasses=useClasses,
                                               emphasizing=emphasizingField,
                                               classes=classes),
                        attrs=liAttrs)
                return {"child": li,
                        "questions": {field},
                        "filledFields": [field]}

        if globalFun is None:
            def globalFun(lines):
                labelGen = Label(label=self.label,
                                 fields=self.numberedFields+[self.groupName],
                                 classes=classes)
                return [labelGen, ": ", HTML(tag="ul" if unordered else "ol", child=lines, attrs=attrs)]

        super().__init__(fields=self.suffixes,
                         name=self.plural,
                         localFun=localFun,
                         globalFun=globalFun,
                         **kwargs)


class PotentiallyNumberedFields(Cascade):
    """If the second element is absent show singleCase. Otherwise, show a
    list of elements."""

    def __init__(self,
                 fieldPrefix,
                 greater,
                 label=None,
                 toKeep=None,
                 emphasizingField=None,
                 attrs=dict(),
                 classes=None,
                 localFunMultiple=None,
                 singleCase=None,
                 liAttrs=dict(),
                 suffix=br,
                 prefix=None,
                 infix=": ",
                 isMandatory=False,
                 numbered_field=None,
                 applyToGroup=None,
                 groupSize=None,
                 **kwargs):
        if numbered_field is None:
            assert greater == 1
            numbered_field = lambda prefix, i: prefix
        nf = NumberedFields(fieldPrefix,
                            greater,
                            numbered_field,
                            label=label,
                            attrs=attrs,
                            liAttrs=liAttrs,
                            classes=classes,
                            localFun=localFunMultiple,
                            isMandatory=isMandatory,
                            applyToGroup=applyToGroup,
                            emphasizingField=emphasizingField,
                            groupSize=groupSize,
                            )
        if singleCase is None:
            singleCase = DecoratedField(field=fieldPrefix,
                                        label=label,
                                        infix=infix,
                                        classes=classes,
                                        emphasizingField=emphasizingField,
                                        prefix=prefix,
                                        suffix=suffix,
                                        isMandatory=isMandatory)
        singleCase = Cascade(field=f"{fieldPrefix}s",
                             child=singleCase,
                             cascade={fieldPrefix})
        foe = FilledOrEmpty(numbered_field(fieldPrefix,2),
                            nf,
                            singleCase)
        super().__init__(child=foe,
                         cascade={fieldPrefix},
                         field=fieldPrefix+"s",
                         **kwargs)

    # def __repr__(self):
    #     return f"""PotentiallyNumberedFields() on {super().__repr__()}"""
