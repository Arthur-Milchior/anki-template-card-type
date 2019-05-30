from ..generators import *
from .general import header, footer


definition_stats = TableFields(
    fields = [
        {"field":"Density function",
         "classes":"Definition1"},
        {"field": "Cumulative function",
         "classes":"Definition2"},
        [{"field":"Moment generating function",
         "classes":"Definition3"},
        {"field":"Characteristic function",
         "classes":"Definition4"}]
    ], answer = " computation"
)
properties = TableFields(["Mean", "Median", "Mode", ["Variance", "Standard deviation"], "Skewness", "Kurtosis", "Nth moment", "Nth factorial moment", "Nth cumulant", "Nth central moment"], answer = " computation")

statistical_distribution = [header, definition_stats, properties, footer]
