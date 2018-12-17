from .conditionals import  Branch
from ..singleChild import Filled
from ..generators import Gen
from ..leaf import Field
from ...debug import debug, assertType
from .sugar import NotNormal


class QuestionnedField(Branch):
    """Show the content of the field. Unless the field is asked and its the question, then show ???

    This can be parametrized as any branch. To forbid the use of
    questionAsked, assign it to False.

    field is either a field name, or a Field object. It becomes the name of the Branch.
    """
    
    def __init__(self,
                 field,
                 questionAsked = None,
                 default = None,
                  **kwargs):
        if isinstance(field,str):
            self.fieldName = field
            self.field = Field(field)
        else:
            assert assertType(field,Field)
            self.field = field
            self.fieldName = field.field
        if questionAsked is None:
            questionAsked = "???"
        if default is None:
            default = self.field
        self.questionAsked = questionAsked
        self.default = default
        #todo emphasize answerAsked
        super().__init__(name = self.fieldName,
                         questionAsked = questionAsked,
                         default = default,
                         **kwargs)
        
    # def __repr__(self):
    #     return f"""QuestionnedField({self.field}, {self.questionAsked}, {self.default})."""
        
class DecoratedField(Gen):
    """A questionned field, preceded by some way to ask the question.
    If there is no question, nothing is printed."""

    def __init__(self,
                 field,
                 label = None,
                 **kwargs):
        """field -- a field object, or a string"""
        if isinstance(field,str):
            field = Field(field)
        if label is None:
            label = field.field
        self.label = label
        self.field = field
        super().__init__(**kwargs)

    def _getNormalForm(self):
        return Filled(field = self.field.field,
                      child = [
                          self.label,
                          ": ",
                          QuestionnedField(self.field)]
        ).getNormalForm()
        

    # def __repr__(self):
    #     return f"""DecoratedField({self.field})"""
