from ..conditionals.filledOrEmpty import Filled
from ..generators import NotNormal
from ..leaf import Field
from .fields import DecoratedField


class FromAndTo(NotNormal):
    """This generator allow to create questions of the form

    ```{{English}} in CLASS(FRENCH) is {{French}}``` or
    ```{{Abbreviation}} is the CLASS(ABBREVIATION) of {{Name}}```
    From one data, ask another data, emphasize the transformation. Show only if both sides exists.
    """

    def __init__(self, questionField, fieldToQuestion, actualQuestion, questionToAnswer, answer, prefix=None, suffix=None, classes=None):
        self.questionField = questionField
        self.fieldToQuestion = fieldToQuestion
        self.actualQuestion = actualQuestion
        self.questionToAnswer = questionToAnswer
        self.answer = answer
        self.prefix = prefix
        self.suffix = suffix
        self.classes = classes
        super().__init__()

    def _getNormalForm(self):
        prefix = [Field(self.questionField,
                        classes=self.classes),
                  self.fieldToQuestion]
        df = DecoratedField(prefix=prefix,
                            label=self.actualQuestion,
                            infix=self.questionToAnswer,
                            field=self.answer,
                            classes=self.classes
                            )
        l = [self.prefix, df, self.suffix]
        f = Filled(self.answer,
                   Filled(self.questionField,
                          l))
        return f.getNormalForm().assumeAsked(self.answer).getNormalForm()
