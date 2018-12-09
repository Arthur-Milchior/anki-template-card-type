jsonTest = """{
    "instructions":[
        ["test", "'test'"],
        ["foo","[\\"foo\\",None, Field(\\"FrontField\\")]"],
        ["front", "DecoratedField('FrontField')"]
    ]
}"""

model = {'sortf': 0, 'did': 1, 'latexPre': '\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n', 'latexPost': '\\end{document}', 'mod': 1544145481, 'usn': -1, 'vers': [], 'type': 0, 'css': '.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n', 'name': 'Basic', 'flds': [{'name': 'FrontField', 'ord': 0, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}, {'name': 'Back', 'ord': 1, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}], 'tmpls': [{'name': 'Card 1', 'ord': 0, 'qfmt': '\n <span object="test" template="object"/>\n', 'afmt': '<span template="Front Side"/>', 'did': None, 'bqfmt': '\n', 'bafmt': '\n'}, {'name': 'Card 2', 'ord': 1, 'qfmt': '\n <span object="front" asked="FrontField" template="object"/>\n', 'afmt': '<span template="Front Side"/>', 'did': None, 'bqfmt': '\n', 'bafmt': '\n'}], 'tags': [], 'id': '1542656718186', 'req': [[0, 'none', []]]}
