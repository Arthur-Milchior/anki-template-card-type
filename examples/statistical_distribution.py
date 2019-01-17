from ..generators import *
from .general import header, footer


definition_stats = TableFields(
    fields = [
        {"field":"Density function",
         "classes":"Definition1"},
        {"field": "Cumulative function",
         "classes":"Definition2"},
        {"field":"Moment generating function",
         "clasess":"Definition3"},
        {"field":"Characteristic function",
         "clasess":"Definition4"},
    ]
)
properties = TableFields(["Mean", "Median", "Mode", "Variance", "Standard deviation", "Skewness", "Kurtosis", "Nth moment"])

statistical_distribution = [header, definition_stats, properties, footer]
