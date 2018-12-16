class AtLeastNField(SingleChild, NotNormal):
    """Show the child if at least n of the fields have content.

    If there are m fields, then the length of the text generated is
    O(m choose n). For n=1, it means the text is linear in the number
    of fields. For n=2, it means the text is square in the number of fields.

    So use this only for small text, such as
    <table>.
    """
    def __init__(self, child, fields, n=1):
        self.child = child
        super().__init__(child)
        self.n = n
        self.fields = fields
        
    # def __repr__(self):
    #     return f"""AtLeastNField({self.child},{self.fields},{self.n})"""

    def _getNormalForm(self):
        if self.n == 0:
            return self.child.getNormalForm()
        seen = set()
        seen_card = 0
        actual = emptyGen
        for condition in self.fields:
            if seen_card >= self.n-1:
                actual = FilledOrEmptyField(condition,
                                            filledCase = AtLeastNField(self.child, seen, self.n-1),
                                            emptyCase = actual)
            seen_card +=1
            seen.add(condition)
        return actual.getNormalForm()

class AtLeastOneField(AtLeastNField):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, n=1,**kwargs)
class AtLeastTwoField(AtLeastNField):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, n=2,**kwargs)
