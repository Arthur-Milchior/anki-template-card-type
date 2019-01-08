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
        if label is not None:
            self.label = label
            if isinstance(field,str):
                self.field = Field(field)
            elif isinstance(field,Field):
                self.field = field
            else:
                raise Exception
        else:# label is not given
            if isinstance(field,tuple):
                assert (label is None)
                self.field, self.label = field
            elif isinstance(field,LabeledField):
                self.field = field.field
                self.label = field.label
            else:
                # label is a copy of label
                if isinstance(field, Field):
                    self.field = field.field
                elif isinstance(field,str):
                    self.field = field
                else:
                    raise Exception
                self.label = self.field

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
                  **kwargs):
        if isinstance(field,str):
            self.fieldName = field
            self.field = Field(field)
        else:
            assert assertType(field,Field)
            self.field = field
            self.fieldName = field.field
        self.asked = QuestionOrAnswer("???", CLASS(["Answer", f"Answer_{self.fieldName}"],self.field))
        #todo emphasize answerAsked
        super().__init__(self.fieldName,
                         self.asked,
                         self.field,
                         **kwargs)
        
    # def __repr__(self):
    #     return f"""QuestionnedField({self.field}, {self.questionAsked}, {self.default})."""

class Label(QuestionOrAnswer):
    """Apply classes to the label on question side if one of the field is
asked."""
    def __init__(self, label, fields, classes):
        questionSide = AtLeastOneField(child = CLASS(classes,label),
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
                 labeledField,
                 infix = ": ",
                 prefix = None,
                 suffix = br,
                 toKeep = True,
                 **kwargs):
        """field -- a field object, or a string"""
        self.labeledField = LabeledField(labeledField)
        self.infix = infix
        labelGen = Label(label = self.labeledField.label,
                         fields = [self.labeledField.field],
                         classes = ["Question","Question_{self.labeledField.field}"])
        super().__init__(field = self.labeledField.field,
                         child = [
                             labelGen,
                             self.infix,
                             QuestionnedField(self.labeledField.field),
                             suffix
                         ],
                         **kwargs
        )
