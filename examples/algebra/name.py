from ...generators import *


def FOE(*args, **kwargs):
    return FilledOrEmpty(*args, isMandatory=True, **kwargs)


ringCom1 = FOE('÷',
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
                               AtLeastOneField(fields=['⋀', '⋁'],
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
            ringCom1,
            FOE('÷',
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

ring_like = Empty('Not associative',
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
                 FOE('÷',
                     FOE('\\',
                         FOE('0',
                             'Loop',
                             'Quasigroup'),
                         'Right division but no left division, while no associativity ?'
                         ),
                     'Magma'
                     ),
                 [FOE('1',
                      FOE('÷',
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
                    FOE('÷',
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
            # FOE('Set',
            #     'Group-based',
            FOE('Ring-base',
                FOE('Graduation',
                    'Graduated module',
                    'Module'
                    ),
                'Vector space'
                # )
                )
            )

lattice = FOE('⋀',  # Assumed associative commutative idempotent
              FOE('⋁',  # Assumed associative commutative idempotent, absorbtion with and over ⋀
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
                                           'Orthomodular lattice',  # Assume idempotent
                                           'Orthocomplemented lattice',  # Assume idempotent
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
              FOE('⋁',  # Assumed associative commutative umed
                  FOE('0',
                      'Bounded join-semilattice',
                      'Join-semilattice'
                      ),
                  AtLeastOneField(fields=['≤', '<'],
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

algebra_name_formatted = [HTML("h1", child=algebra_name), hr]
