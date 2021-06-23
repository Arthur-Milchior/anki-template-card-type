from ..generators import *
from .general import footer, header, namesNotationsDenotedBy
from .util import addBoilerplate


definition_hacker = TableFields(
    name="Hacker",
    fields=[
        {"field": "Numeric",
         "classes": "Name"},
        {"field": "Binary",
         "classes": "Notation"}
    ],
    suffix=hr
)

exprs = NumberedFields("Expression",
                       6,
                       localFun=(lambda i:
                                 {"child": LI([QuestionnedField(f"Expression{i}", classes="Definition"),
                                               Filled(f"Explanation{i}", Answer(Parenthesis({f"Explanation{i}"})))]),
                                  "filledFields": [f"Expression{i}"],
                                  "questions": {f"Expression{i}"}}),
                       suffix=hr)


hacker = addBoilerplate([namesNotationsDenotedBy, definition_hacker, exprs, DecoratedField("Property")])
