from ..conditionals.branch import Branch
from ..conditionals.questionOrAnswer import QuestionOrAnswer
from ..conditionals.filledOrEmpty import Filled
from ..generators import Gen, NotNormal
from ..leaf import Field, Leaf
from ...debug import debug, assertType
from ..conditionals.askedOrNot import AskedOrNot
from ..html import CLASS, br
from ..leaf import Field
from ..conditionals.numberOfField import AtLeastOneField

class LabeledField:
    """A pair, with a label and a field."""
    def __init__(self,field, label=None):
        self.label = None
        if label is not None:
            self.label = label
        if isinstance(field,tuple):
            assert (label is None)
            self.field, self.label = field
        else:
            self.field = field
        if isinstance(self.field,str):
            self.field = Field(self.field)
        if self.label is None:
            self.label = self.field.field
        assert assertType(self.field, Field)
        assert assertType(self.label, str)

    def __eq__(self,other):
        return self.label == other.label and self.field == other.field
            

class QuestionnedField(AskedOrNot):
    """Show the content of the field. Unless the field is asked and its the question, then show ???

    This can be parametrized as any branch. To forbid the use of
    questionAsked, assign it to False.

    field is either a field name, or a Field object. It becomes the name of the Branch.
    """
    
    def __init__(self,
                 field,
                 classes = None,
                  **kwargs):
        if isinstance(field,str):
            self.fieldName = field
            self.field = Field(field)
        else:
            assert assertType(field,Field)
            self.field = field
            self.fieldName = field.field
        if classes is None:
            classes = [self.fieldName]
        if isinstance(classes,str):
            classes=[classes]
        classes = ["Answer"]+classes
        self.classes = classes
        self.asked = QuestionOrAnswer("???", CLASS(classes,self.field))
        #todo emphasize answerAsked
        super().__init__(self.fieldName,
                         self.asked,
                         self.field,
                         **kwargs)
        
    # def __repr__(self):
    #     return f"""QuestionnedField({self.field}, {self.questionAsked}, {self.default})."""

class Label(QuestionOrAnswer):
    """Apply classes to the label on question side if one of the fields is
    asked.

    """
    def __init__(self, label, fields, classes=None):
        self.classes = classes
        if self.classes is None:
            self.classes = [label]
        self.classes=["Question"]+self.classes
        questionSide = AtLeastOneField(child = CLASS(self.classes,label),
                                       fields = fields,
                                       otherwise = label,
                                       asked = True
        )
        answerSide = label
        super().__init__(questionSide,answerSide)
        
class DecoratedField(Filled):
    """A questionned field, preceded by some way to ask the question.
    If there is no question, nothing is printed."""

    def __init__(self,
                 field,
                 label = None,
                 infix = ": ",
                 prefix = None,
                 suffix = br,
                 toKeep = True,
                 **kwargs):
        """field -- a field object, or a string"""
        self.prefix=prefix
        self.infix = infix
        self.suffix=suffix
        self.field = field
        if isinstance(self.field,str):
            self.field= Field(self.field)
        if label is None:
            self.label = self.field.field
        else:
            self.label =label
        labelGen = Label(label = self.label,
                         fields = [self.field.field],
                         classes = [self.field.field])
        super().__init__(field = self.field,
                         child = [
                             self.prefix,
                             labelGen,
                             self.infix,
                             QuestionnedField(self.field),
                             self.suffix
                         ],
                         **kwargs
        )
