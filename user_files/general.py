def name(nb):
    text = "name"+nb
    return Filled(text,
                  Asked(text,
                        [QuestionnedField(field = text),
                         AskedOrNot("name2", "<br/>:","</li>")
                         NotAsked(text,
                                  [
                                      DecoratedField(field = kind+nb, label = kind, prefix = "(", suffix = ")")
                                      for kind in ["french", "etymology", "abbreviation"]
                                  ]
                         )
                        )
                  )
    )

names = ('name',[PotentiallyNumberedFields('Name',4),br])

namesNotationsDenotedBy = [names,
                           ('Notation',[PotentiallyNumberedFields('Notation',4),br]),
                           DecoratedField('Representation'),
                           DecoratedField('Denoted by'),
]

contextOrDeck = [FilledOrEmpty('Context', Field('Context'),deck), hr]
head = [contextOrDeck,('Variables', [{{'Variables'}}, hr] )]
extendedHead = [head, ('Assuming',[{{'Assuming'}},br]), namesNotationsDenotedBy]

footer = [Filled('Extra', Field('Extra')), hr]

