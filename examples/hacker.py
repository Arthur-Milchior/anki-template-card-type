from .general import header, footer
from ..generators import *

definition_hacker = TableFields(
    name = "Hacker",
    fields = [
    {"field": "Numeric",
     "classes":"Name"},
    {"field": "Binary",
     "classes":"Notation"}
    ],
    suffix=hr
)

exprs=NumberedFields("Expression",
                     6,
                     localFun=(lambda i:
                               {"child":LI([QuestionnedField(f"Expression{i}",classes="Definition"),
                                            Filled(f"Explanation{i}",Answer(Parenthesis({f"Explanation{i}"})))]),
                                "filledFields": [f"Expression{i}"],
                                "questions":{f"Expression{i}"}}),
                     suffix=hr)



hacker = [header, definition_hacker, exprs, DecoratedField("Property"), footer]
