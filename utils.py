def firstTruth(l):
    for elt in l:
        if elt: 
            return elt
        
def identity(x):
    return x

def standardContainer(cont):
    return isinstance(cont,list) or isinstance(cont,set)  or isinstance(cont,frozenset)
