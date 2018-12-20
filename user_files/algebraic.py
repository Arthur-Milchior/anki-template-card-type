from ..generators.imports import *
FOE= FilledOrEmpty

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
                               AtLeastOneField(['⋀','⋁'],
                                               'GCD domain',
                                               FOE('Integral',
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

ring1 = FOE('commutative',
            RingCom1
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

inner = FOE('Not associative',
                   FOE('0',
                       FOE('-',
                           Foe('*',
                               FOE('Right-distributive',
                                   'Near-Ring',
                                   ring),
                               FOE('Commutative',
                                   'Abelian group',
                                   'Group'
                               )
                           ),
                           FOE('Commutative',
                               FOE('*',
                                   'Commutative semiring',
                                   'Commutative monoid'
                               ),
                               FOE('*',
                                   'Semiring',
                                   'Monoid'
                               )
                           )
                       ),
                       FOE('Commutative',
                           'Commutative semigroup',
                           'Semigroup')
                   )
                   FOE('/',
                       Foe('\\',
                           FOE('0',
                               'Loop',
                               'Quasigroup'),
                           'Right division but no left division, while no associativity ?'
                       ),
                       'Magma')
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
             filled('Not associative',
                    'non'),
             'associative algebra',
             Filled('Commutative',
                    ' commutative'),
             Filled('Ring-based', ' over a ring')
            ],
            FOE('Set',
                'Group-based',
                FOE('Ring-based',
                    FOE('Graduation',
                        'Graduated module',
                        'Module'
                        p),
                    'Vector space'
                )
            )
)
sg = FOE('×', #outer product
         outer,
         inner)

lat = FOE('⋀',#Assumed associative commutative idempotent
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
                                   FOE('Modular'
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
          )
          FOE('⋁',#Assumed associative commutative umed
              FOE('0',
                  'Bounded join-semilattice',
                  'Join-semilattice'
              ),
              AtLeastOneField(['≤','<'],
                              FOE('Total',
                                  'Total order',
                                  'Poset'
                              ),
              )
          ),
)
triangle = FOE('Idempotent',
               'Quandle',
               'Rack')

algebras = FOE('+',
               sg,
               FOE('◁',
                   triangle,
                   lat
               )
)

otherFields = [
    'cover'
]
