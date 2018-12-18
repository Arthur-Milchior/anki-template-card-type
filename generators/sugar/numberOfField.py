from ...debug import debugFun, debugInit, debug
from ..singleChild import SingleChild
from ..leaf import emptyGen
from .sugar import NotNormal
from .conditionals import FilledOrEmpty
from ..constants import *
from ..generators import Gen

class AtLeastNField(SingleChild, NotNormal):
    """Show the child if at least n of the fields have content.

    If there are m fields, then the length of the text generated is
    O(m choose n). For n=1, it means the text is linear in the number
    of fields. For n=2, it means the text is square in the number of fields.

    So use this only for small text, such as
    <table>.
    """
    @debugInit
    def __init__(self, child, fields, n=1):
        self.child = child
        super().__init__(child)
        self.n = n
        self.fields = fields
        if n> len(fields):
            self.setState(EMPTY)
        
    # def __repr__(self):
    #     space  = "  "*Gen.indentation
    #     return f"""{space}AtLeastNField(\n{space}  {self.child},\n{space}  {self.fields},{self.n})"""

    @debugFun
    def _getNormalForm(self):
        if self.n == 0:
            return self.child.getNormalForm()
        if not self.fields:
            return emptyGen
        element = self.fields[-1]
        remaining = self.fields[:-1]
        filledCase = AtLeastNField(child = self.child,
                                   fields = remaining,
                                   n = self.n-1)
        emptyCase = AtLeastNField(child = self.child,
                                  fields = remaining,
                                  n = self.n)
        dichotomy = FilledOrEmpty(element,
                                  filledCase = filledCase,
                                  emptyCase =  emptyCase,
        )
        return dichotomy.getNormalForm()


class AtLeastOneField(AtLeastNField):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, n=1,**kwargs)
class AtLeastTwoFields(AtLeastNField):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, n=2,**kwargs)
