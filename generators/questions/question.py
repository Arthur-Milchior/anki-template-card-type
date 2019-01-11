from ..generators import NotNormal
from ..conditionals.filledOrEmpty import Filled
from ..leaf import Field
from .fields import DecoratedField
class FromAndTo(NotNormal):
    """This generator allow to create questions of the form

    ```{{English}} in CLASS(FRENCH) is {{French}}``` or
    ```{{Abbreviation}} is the CLASS(ABBREVIATION) of {{Name}}```
    From one data, ask another data, emphasize the transformation. Show only if both sides exists.
    """
    def __init__(self,questionField, fieldToQuestion, actualQuestion, questionToAnswer, answer,prefix=None,suffix=None):
        self.questionField = questionField
        self.fieldToQuestion=fieldToQuestion
        self.actualQuestion=actualQuestion
        self.questionToAnswer=questionToAnswer
        self.answer=answer
        self.prefix =prefix
        self.suffix=suffix
        super().__init__()
    def getNormalForm(self):
        prefix=[Field(self.questionField), self.fieldToQuestion]
        df= DecoratedField(prefix = prefix,
                           label = self.actualQuestion,
                           infix= self.questionToAnswer,
                           field = self.answer
        )
        l=[self.prefix,df,self.suffix]
        f=Filled(self.answer,
                 Filled(self.questionField,
                        l))
        return f.getNormalForm().assumeAsked(self.answer).getNormalForm()
