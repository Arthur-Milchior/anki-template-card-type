from general import header, footer

definition_foo = TableFields(
    fields = ["Density funciton", "Cumulative function", "Moment generating function", "Characteristic function"]
)
properties = TableFields(["Mean", "Median", "Mode", "Variance", "Standard deviation", "Skewness", "Kurtosis", "Nth moment"])

statistical_distribution = [header, definition_foo, properties, footer]
