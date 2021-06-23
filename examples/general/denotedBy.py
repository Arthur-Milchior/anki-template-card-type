from ..util import *
from ..style import *
from ...generators import *

denotedBy = Filled(
    "Denoted by",
    addBoilerplate(
        [FilledOrEmpty("Name", {"Name"}, {"Notation"}),
         " is denoted by ",
         QuestionnedField("Denoted by")
        ]
    )
)
