from ...generators import *
contextOrDeck = [FilledOrEmpty('Context',
                               DecoratedField('Context', isMandatory = True),
                               ["Deck: ",deck]), hr]
short_header =CLASS("head",[contextOrDeck,('Variables', [DecoratedField('Variables'), hr] ),('Assuming',[DecoratedField('Assuming'),br])])

