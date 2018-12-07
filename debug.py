indentation = 0
def debug(text, indent=0):
    if indent>0:
        sep = "{"
    elif indent==0:
        sep = ""
    else:
        sep = "}"
    print (f"""{" "*indent}{sep}{text}""")
    indent +=indent
    pass
