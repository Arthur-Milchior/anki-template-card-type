from ...generators import *
contextOrDeck = [FilledOrEmpty('Context',
                               DecoratedField('Context', isMandatory = True),
                               ["Deck: ",deck]), hr]
def df(name):
    return DecoratedField(name,suffix=hr)

short_header =CLASS("head",[contextOrDeck,df('Variables'),df('Assuming'),df('Intuition')] )
