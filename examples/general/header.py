from ...generators import *

header = HEADER (
    H1([
        Filled('Language',{"Language"}), # For programming language
        Filled("Context", Filled("Language",": ")),
        Filled('Context',{"Context"})
    ])
)

