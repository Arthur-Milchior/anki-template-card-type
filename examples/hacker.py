from .general import header, footer
from ..generators.imports import *

definition_hacker = TableFields(
    name = "Hacker",
    fields = ["Numeric","Binary"],
    suffix=hr
)

exprs=NumberedFields("Expression",
                     6,
                     localFun=(lambda i:
                               {"child":LI([QuestionnedField(f"Expression{i}",classes=["Expression"]),
                                            Filled(f"Explanation{i}",Answer(Parenthesis({f"Explanation{i}"})))]),
                                "filledFields": [f"Expression{i}"],
                                "questions":{f"Expression{i}"}}),
                     suffix=hr)



hacker = [header, definition_hacker, DecoratedField("Property"),exprs, footer]
