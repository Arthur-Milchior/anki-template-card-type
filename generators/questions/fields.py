from ...debug import assertType, debug
from ..conditionals.askedOrNot import AskedOrNot
from ..conditionals.filledOrEmpty import Filled
from ..conditionals.numberOfField import AtLeastOneField
from ..conditionals.questionOrAnswer import QuestionOrAnswer
from ..generators import Gen, NotNormal
from ..html.atom import br, markOfQuestion
from ..html.html import CLASS
from ..leaf import Field, Leaf


class QuestionnedField(AskedOrNot):
    """Show the content of the field. Unless the field is asked and its the question, then show ???

    This can be parametrized as any branch. To forbid the use of
    questionAsked, assign it to False.

    field is either a field name, or a Field object. It becomes the name of the Branch.
    """

    def __init__(self,
                 field,
                 classes = None,
                 child=None,
                 isMandatory = False,
                 emphasize = True,
                 useClasses = True,
                 suffix = None,
                 **kwargs):
        """
        useClasses -- whether the name of the field/classes should be applied to this field.
        emphasize -- apply emphasize and Answer on answer side when this is asked
        """

        # Getting both the field and its name
        if isinstance(field,str):
            self.fieldName = field
            self.field = Field(field)
        else:
            assert assertType(field,Field)
            self.field = field
            self.fieldName = field.field

        # Setting the class
        self.classes = classes
        if self.classes is None:
            self.classes = [self.fieldName]
        if isinstance(self.classes,str):
            self.classes=[self.classes]
        if useClasses is False:
            self.classes = []
        self.emphasize = ["Answer", "Emphasize"] if emphasize else []
        self.classesAsked = self.emphasize + self.classes

        # Setting the child
        self.child = child
        if self.child is None:
            self.child = Field(field,
                               isMandatory=isMandatory,
                               useClasses = False)
        if suffix is not None:
            self.child = [self.child, suffix]

        self.asked = QuestionOrAnswer(markOfQuestion,
                                      CLASS(self.classesAsked,
                                            self.child))
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
    asked.

    label -- the content shown
    classes -- the classes to apply to the label
    fields -- if one of those values is asked, the label is emphasized
    """
    def __init__(self,
                 label,
                 fields,
                 classes = None,
                 alwaysUseClasses = True):
        # Classes
        self.classes = classes
        if self.classes is None and isinstance(label,str) :
                self.classes = [label]
        if isinstance(self.classes,str):
            self.classes=[self.classes]
        self.questionnedClasses = ["Question","Emphasize"]+self.classes

        emphasized = CLASS(self.questionnedClasses,label)

        if alwaysUseClasses:
            notEmphasized = CLASS(self.classes,label)
        else:
            notEmphasized = label

        questionSide = AtLeastOneField(child = emphasized,
                                       fields = fields,
                                       otherwise = notEmphasized,
                                       asked = True)
        super().__init__(questionSide,notEmphasized)

class DecoratedField(Filled):
    """A questionned field, preceded by some way to ask the question.
    If there is no question, nothing is printed.

    Emphasize -- whether to add Emphasize and Question/Answer class when this field is asked.
    useClasses -- whether to use the name of the field/classes on label and question
    """

    def __init__(self,
                 field,
                 label = None,
                 infix = ": ",
                 prefix = None,
                 suffix = br,
                 toKeep = True,
                 classes = None,
                 child = None,
                 isMandatory = False,
                 useClasses = True,
                 emphasize = True,
                 **kwargs):
        """field -- a field object, or a string"""
        self.prefix=prefix
        self.child=child
        self.infix = infix
        self.suffix=suffix
        self.field = field
        if isinstance(self.field,str):
            self.field= Field(self.field, isMandatory = isMandatory, useClasses = useClasses)
        if label is None:
            self.label = self.field.field
        else:
            self.label =label
        if classes is None:
            self.classes=[self.field.field]
        else:
            self.classes=classes
        if self.child is None:
            self.child = QuestionnedField(field = self.field,
                                          classes = self.classes,
                                          isMandatory = isMandatory,
                                          useClasses = useClasses,
                                          emphasize =  emphasize)
        if emphasize:
            labelGen = Label(label = self.label,
                             fields = [self.field.field],
                             classes = self.classes)
        else:
            labelGen = self.label

        super().__init__(field = self.field.field,
                         child = [
                             self.prefix,
                             labelGen,
                             self.infix,
                             self.child,
                             self.suffix,
                         ],
                         **kwargs
        )
