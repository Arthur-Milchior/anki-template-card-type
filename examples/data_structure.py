from ..generators.questions.fields import QuestionnedField
from ..generators.questions.listFields import TableFields
from .general.typ import typDic
from .general.examples import examples
from .general.namesNotationsDenotedBy import namesNotationsDenotedBy
from .util import addBoilerplate, code, empty1, numbered_field
from aqt.qt import debug
from ..generators.html.atom import hr

fields = []
for i in range(1, 13):
    # the value of i is fixed here.
    field_name = numbered_field("Implementation", i)
    field = {field_name}
    label = [{numbered_field("Function name", i)}, ":"]
    def function(field_name):
        output = QuestionnedField(field=field_name,
            child=code("Language")({field_name})
        )

        return lambda _: output
    fields.append({
            "label": label,
            "field": field_name,
            "function": function(field_name),
        })

functions = TableFields(
    fields,
    isMandatory=False,
    suffix=hr
    )

data_structure = addBoilerplate([
    namesNotationsDenotedBy,
    functions
])