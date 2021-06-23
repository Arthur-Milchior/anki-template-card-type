from ..generators import *
from .general import footer, header
from .general.namesNotationsDenotedBy import namesNotationsDenotedBy
from .util import *
from .style import *

definition_stats = TableFields(
    fields=[
        {"field": "Density function",
         "classes": "Definition1"},
        {"field": "Cumulative function",
         "classes": "Definition2"},
        [{"field": "Moment generating function",
          "classes": "Definition3"},
         {"field": "Characteristic function",
          "classes": "Definition4"}]
    ], answer=" computation"
)
properties = TableFields(["Mean", "Median", "Mode", ["Variance", "Standard deviation"], "Skewness", "Kurtosis",
                          "Nth moment", "Nth factorial moment", "Nth cumulant", "Nth central moment"], answer=" computation", emphasizing=decorateQuestion)

statistical_distribution = addBoilerplate([namesNotationsDenotedBy, definition_stats, properties])
