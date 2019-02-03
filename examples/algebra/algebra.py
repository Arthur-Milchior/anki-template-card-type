from ...generators import *
from ..general.head import header
from ..general.foot import footer
from ..general.typ import typDic

def FOE(*args,**kwargs):
    return FilledOrEmpty(*args, isMandatory=True, **kwargs)
ringCom1 = FOE('/',
               'Field',
               FOE('Graduation',
                   'Gradued ring',
                   FOE('Euclidean function',
                       'Euclidean domain',
                       FOE('Principal ideal',
                           FOE('Integral',
                               'PID',
                               'Principal ideal ring'),
                           FOE('Unique factorization',
                               FOE('Integral',
                                   'UFD',
                                   'Unique Factorization Ring'),
                               AtLeastOneField(fields=['⋀','⋁'],
                                               child='GCD domain',
                                               otherwise=FOE('Integral',
                                                             FOE('Closed',
                                                                 'Integrally closed ring',
                                                                 'Commutative ring',
                                                             ),
                                                             'Unitary commutative ring',
                                               )
                               )
                           )
                       )
                   )
               )
)

ring1 = FOE('Commutative',
            'RingCom1',
            FOE('/',
                "Division ring",
                "Unit ring",
            )
)

ring = FOE('1',
            ring1,
            FOE('Commutative',
                'Commutative ring',
                'Ring')
)

ring_like =Empty('Not associative',
               FOE('1',
                   FOE('-',
                       FOE('Right-distributive',
                           'Near-Ring',
                           ring),
                       FOE('Commutative',
                           'Commutative semiring',
                           'Semiring',
                       )
                   ),
                   FOE('-',
                       FOE('Commutative',
                           'Commutative rng',
                           'Rng'
                       ),
                       FOE('Commutative',
                           'Commutative semirng',
                           'Semirng'
                       )
                   )
               )
)

times_only = FOE('Not associative',
                 FOE('/',
                     FOE('\\',
                         FOE('0',
                             'Loop',
                             'Quasigroup'),
                         'Right division but no left division, while no associativity ?'
                     ),
                     'Magma'
                 ),
                 [FOE('1',
                      FOE('/',
                          FOE('Commutative',
                              'Abelian group',
                              'Group'
                          ),
                          FOE('Commutative',
                              'Commutative monoid',
                              'Monoid',
                          )
                      ),
                      FOE('Commutative',
                          'Commutative semigroup',
                          'Semigroup'
                      )
                 ),
                  Filled('0',
                         ' with zero')]
)

plus_only = Empty('Not associative',
                  FOE('0',
                      FOE('-',
                          FOE('Commutative',
                              'Abelian group',
                              'Group'
                          ),
                          FOE('Commutative',
                              'Commutative monoid',
                              'Monoid',
                          )
                      ),
                      FOE('Commutative',
                          'Commutative semigroup',
                          'Semigroup'
                      )
                  )
)

outer = FOE('*',
            [Filled('Quadratic form',
                    'Composition '),
             Filled('1',
                    FOE('/',
                        'division',
                        'unital '
                    )
             ),
             Filled('Not associative',
                    'non'),
             'associative algebra',
             Filled('Commutative',
                    ' commutative'),
             Filled('Ring-base', ' over a ring')
            ],
            FOE('Set',
                'Group-based',
                FOE('Ring-base',
                    FOE('Graduation',
                        'Graduated module',
                        'Module'
                    ),
                    'Vector space'
                )
            )
)

lattice = FOE('⋀',#Assumed associative commutative idempotent
              FOE('⋁',#Assumed associative commutative idempotent, absorbtion with and over ⋀
                  [Filled('Distributive', 'Distributive'),
                   FOE('0',
                       FOE('1',
                           FOE('→',
                               FOE('Complete',
                                   'Complete Heyting algebra',
                                   'Heyting algebra'
                               ),
                               FOE('¬',
                                   FOE('Distributive',
                                       'Boolean algebra',
                                       FOE('Modular',
                                           'Orthomodular lattice',#Assume idempotent
                                           'Orthocomplemented lattice',#Assume idempotent
                                       ),
                                   ),
                                   'Bounded lattice'
                               )
                           ),
                           'Lattice with 0 but no 1?'
                       ),
                       'Lattice'
                   )],
                  FOE('1',
                      'Bounded Meet-semilattice',
                      'Meet-semilattice'
                  )
              ),
              FOE('⋁',#Assumed associative commutative umed
                  FOE('0',
                      'Bounded join-semilattice',
                      'Join-semilattice'
                  ),
                  AtLeastOneField(fields=['≤','<'],
                                  child=FOE('Total',
                                            'Total order',
                                            'Poset'
                                  ),
                  )
              )
)
triangle = FOE('Idempotent',
               'Quandle',
               'Rack')

algebra_name = FOE('+',
                   FOE('×',
                       outer,
                       FOE('*',
                           ring_like,
                           plus_only)),
                   FOE('*',
                       times_only,
                       FOE('◁',
                           triangle,
                           lattice
                       )
                   )
)

algebra_name_formatted = [HTML("h1", child = algebra_name),hr]

inner_function = TableFields(
    [
        {"field":"Ring-base",
         "label": "Base",
         "classes": "Definition6"},
        {"field":"Field-base",
         "label": "Base",
         "classes": "Definition6"},
        {"field":"+",
         "classes":"Definition"},
        {"field":    "0",
         "classes":"Definition2"},
        {"field":    "-",
         "classes":"Definition3"},
        {"field":    "*",
         "classes":"Definition4"},
        {"field":    "1",
         "classes":"Definition5"},
        {"field":    "/",
         "classes":"Definition6"},
        {"field":    "\\",
         "classes":"Definition"},
        {"field":    "×",
         "classes":"Definition7"},
        {"field":    "⋀",
         "classes":"Definition8"},
        {"field":    "⋁",
         "classes":"Definition9"},
        {"field":    "→",
         "classes":"Definition"},
        {"field":    "¬",
         "classes":"Definition4"},
        {"field":    "◁",
         "classes":"Definition5"},
    ],
    name = "Explicit definition",
    suffix = hr
)

presentation = ("Relation",
                PotentiallyNumberedFields(label = Cascade("Relations",
                                                          QuestionnedField("Generating family"),
                                                          {"Generating family"}),
                                          greater = 5,
                                          fieldPrefix = "Relation",
                                          suffix = hr))
outer_function = TableFields(
    ["Graduation",
     "Norm",
     "Euclidean function",
     "Quadratic form",
    ],
    name = "Explicit definition"
)
definition = Cascade("Definitions",
                     [presentation,
                      inner_function,
                      outer_function],
                     {"Relations", "Explicit definition"})
                      
            
                
properties = TableFields(
    ["Principal ideal",
     "Integral",
     "Unique factorization",
     "Closed",
     "Commutative",
     "Not associative",
     "Right-distributive",
     "Complete",
     "Idempotent",
     "Base",
     "Base2",
     "Base3",
     "Dimension",
     typDic,
     "Free family",
     "Generating family",
     "Inner product",
     "Cover",
     "Minimals",
     "Maximals",
     "Well-founded"
    ]
)

algebra = [header, algebra_name_formatted, definition, properties, footer]
