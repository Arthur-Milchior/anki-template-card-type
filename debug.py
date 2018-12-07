import re

indentation = 0
def debug(text, indent=0):
    global indentation
    if indent>0:
        sep = "{"
    elif indent==0:
        sep = ""
    else:
        sep = "}"
    space = " "*indentation
    newline = "\n"
    print (f"""{space}{sep}{re.sub(newline,newline+space,text)}""")
    indentation +=indent
    pass
