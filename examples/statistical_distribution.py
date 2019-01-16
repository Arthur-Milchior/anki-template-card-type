from ..generators.imports import *
from .general import header, footer


definition_stats = TableFields(
    fields = ["Density function",
              "Cumulative function",
              {"field":"Moment generating function",
               "clasess":["Generating_function1"]},
              {"field":"Characteristic function",
               "clasess":["Generating_function2"]},
    ]
)
properties = TableFields(["Mean", "Median", "Mode", "Variance", "Standard deviation", "Skewness", "Kurtosis", "Nth moment"])

statistical_distribution = [header, definition_stats, properties, footer]
