from ...debug import assertType, debug
from ..conditionals.askedOrNot import AskedOrNot
from ..conditionals.filledOrEmpty import Filled
from ..conditionals.numberOfField import AtLeastOneField
from ..conditionals.questionOrAnswer import QuestionOrAnswer
from ..generators import Gen, NotNormal
from ..html.atom import br, markOfQuestion
from ..html.html import * 
from ..leaf import Field, Leaf

class AskedField(QuestionOrAnswer):
    """Ask the field on question side, answer on the other side

    emphasizing -- function to apply to element we want to emphasize
    question -- The question to ask. By default the field name."""
    def __init__(self, field, question=None, emphasizing=None):
        if emphasizing is None:
            emphasizing = lambda x:x
        if question is None:
            question = field
        super().__init__([emphasizing(question), "?"], emphasizing(Field(field)))

class QuestionnedField(AskedOrNot):
    """Show the content of the field. Unless the field is asked and its the question, then show ???

    This can be parametrized as any branch. To forbid the use of
    questionAsked, assign it to False.

    field -- either a field name, or a Field object. The generator behaves differently depending on whether this field is asked
    classes -- classes to apply to all instance of the child. Field name if None. Not applied if not useClasses
    child -- the principal generator, to which class and tag may be applied depending on question/answer and what is asked
    isMandatory -- fails if the field is not present in the note type
    useClasses -- whether the name of the field, or the classes should be applied to this field.
    suffix -- after child, with same transformations
    emphasizing -- function to apply to element we want to emphasize
    """

    def __init__(self,
                 field,
                 classes=None,
                 child=None,
                 isMandatory=False,
                 useClasses=True,
                 emphasizing=None,
                 suffix=None,
                 **kwargs):

        if emphasizing is None:
            emphasizing = lambda x:x

        # Getting both the field and its name
        if isinstance(field, str):
            self.fieldName = field
            self.field = Field(field)
        else:
            assert assertType(field, Field)
            self.field = field
            self.fieldName = field.field

        # Setting the class
        self.classes = classes
        if self.classes is None:
            self.classes = [self.fieldName]
        if isinstance(self.classes, str):
            self.classes = [self.classes]
        if useClasses is False:
            self.classes = []
        self.classesAsked = ["Answer", "Emphasize"] + self.classes
        
        # Setting the child
        self.child = child
        if self.child is None:
            self.child = Field(field,
                               isMandatory=isMandatory,
                               useClasses=False)
        if suffix is not None:
            self.child = [self.child, suffix]

        self.asked = QuestionOrAnswer(markOfQuestion,
                                      emphasizing(
                                          CLASS(self.classesAsked,
                                                self.child)))
        self.notAsked = CLASS(self.classes,
                              self.child)

        super().__init__(self.fieldName,
                         self.asked,
                         self.notAsked,
                         **kwargs)

    # def __repr__(self):
    #     return f"""QuestionnedField({self.field}, {self.questionAsked}, {self.default})."""


class Label(QuestionOrAnswer):
    """Apply classes to the label on question side if one of the fields is
    asked. I.e.

    "<H2>Definition</H2>" if definition is asked, and "Definition" otherwise

    label -- the content shown
    classes -- the classes to apply to the label if emphasized. If None, field is applied
    fields -- if one of those values is asked, the label is emphasized
    emphasizing -- function to apply to elements to emphasize
    alwaysUseClasses -- whether to use classe even when no reason to emphasize
    """

    def __init__(self,
                 label,
                 fields,
                 classes=None,
                 emphasizing=None,
                 alwaysUseClasses=True):
        # Classes
        self.classes = classes
        if self.classes is None and isinstance(label, str):
            self.classes = [label]
        if isinstance(self.classes, str):
            self.classes = [self.classes]
        self.questionnedClasses = ["Question", "Emphasize"] + self.classes

        if emphasizing is None:
            emphasizing = lambda x:x
        emphasized = emphasizing(CLASS(self.questionnedClasses, label))

        if alwaysUseClasses:
            notEmphasized = CLASS(self.classes, label)
        else:
            notEmphasized = label

        questionSide = AtLeastOneField(child=emphasized,
                                       fields=fields,
                                       otherwise=notEmphasized,
                                       asked=True)
        super().__init__(questionSide, notEmphasized)


class DecoratedField(Filled):
    """Nothing if field is empty
    Otherwise:
    "prefix, label, infix, child, suffix"
    "Definition ???"/"Definition {{Definition}}"

    field -- The field that should be present, and is asked
    infix -- gen between label and field content
    prefix -- gen before label
    suffix -- gen after label
    classes -- classes to apply to element to emphasize. I.e. label in question and field in answer
    child -- the part corresponding to the answer. By default a questionned field
    isMandatory -- fails if the field is not in the note type
    useClasses -- whether to use the name of the field/classes on the question
    emphasizing -- How to emphasize elements
    """

    def __init__(self,
                 field,
                 label=None,
                 infix=": ",
                 prefix=None,
                 suffix=br,
                 classes=None,
                 child=None,
                 isMandatory=False,
                 useClasses=True,
                 emphasizing=None,
                 **kwargs):
        """field -- a field object, or a string"""
        self.prefix = prefix
        self.child = child
        self.infix = infix
        self.suffix = suffix
        self.field = field
        if isinstance(self.field, str):
            self.field = Field(
                self.field, isMandatory=isMandatory, useClasses=useClasses)
        if label is None:
            self.label = self.field.field
        else:
            self.label = label
        self.classes = [self.field.field] if classes is None else classes
        if self.child is None:
            self.child = QuestionnedField(field=self.field,
                                          classes=self.classes,
                                          isMandatory=isMandatory,
                                          useClasses=useClasses,
                                          emphasizing=emphasizing)
        labelGen = Label(label=self.label,
                         fields=[self.field.field],
                         emphasizing=emphasizing,
                         classes=self.classes)

        super().__init__(field=self.field.field,
                         child=[
                             self.prefix,
                             labelGen,
                             self.infix,
                             self.child,
                             self.suffix,
                         ],
                         **kwargs
                         )
