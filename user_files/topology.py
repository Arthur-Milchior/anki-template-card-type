from general import header, footer

definition_topology = TableFields(
    listName = "topology",
    fields = ["Set", "Definition", "Definition2", "Opens", "Compactification of", "Completion of", "Base", "Base2", "Order", "Metric", "Prebase", "Prebase2"]
)
compactness= TableFields(tableName="Compactness",
                         fields = ['a paracompact',
                                   'compact',
                                   'sequentially compact',
                                   'locally compact',
                                   'feebly compact',
                                   'limit point compact',
                                   'paracompact',
                                   'sigma-compact',
                                   'countably compact',
                                   'Hemicompact',
                                   'mesocompact',
                                   'metacompact',
                                   'orthocompact',
                                   'pseudocompact',
                                   'realcompact',
                                   'supercompact',
                                   'freebly compact']
)

TableFields(tableName="Bounded",
            fields=[
                'bounded',
                'totally bounded'
            ]
)

TableFields(tableName="Points",
 fields=[
'limit points',
'isolated points',
])

TableFields(tableName="Sets",
            fields=[
                'clopen',
                'dense',
            ]
)

TableFields(
    tableName="Separation",
    fields=[
        'T0 Kolmogorov',
        'R0 Symmetric',
        'T1 Tikhonov',
        'R1 preregular',
        'weAk Hausdorff',
        'T2 HAusdorff separated',
        'T2 1/2 UrysoHn',
        'completely T2 Completely Hausdorff',
        'regular',
        'T3 regular Hausdorff',
        'coMpletely regular',
        'T3 1/2 TycHonoff',
        'normal',
        'T4 
normal Hausdorff',
        'coMpletely normal',
        'T5 completEly normal Hausdorff',
        'perfectly norMal',
        'T6 perfectly norMal Hausdorff',
        'locally Hausdorff',
        'Collectionwise Hausdorff',
        'locally regulaR',
        'locally normal',
        'Collectionwise normal',
        'monotonically Normal',
        'paranormal',
        'Pseudonormal',
    ])

Tablefields(tableName="Connexion",
            'Connected',
'arc connected',
            'Path connected',
            'locally connecteD',
'locally simply connected',
            'Extremmaly disconnected',
'hyperconnected',
            'N connected',
            'semi-locally Simply connected',
'simply connected',
            'Simply-connected at infinity',
'totally disconnected',
'ultraconnected',
])

TableFields(tableName="Group",
            fields=[
                'connected',
                'fundamental group',
            ])

TableFields(tableName="Cardinal",
            fields=[
                'cardinality',
                'locally finite',
                'sequential',
                'first-countable',
                'second-countable',
                'separable',
                'Lindelof',
            ])

TableFields(tableName="Other",
            fields=[
                'interior',
                'closure',
                'Alexandrov',
                'Baire',
                'cellular',
                'sober',
                'semiregular',
                'quasiregular',
                'contractible',
                'D-space',
                'Door space',
                'Dowker',
                'dyadic',
                'ends',
                'H-closed',
                'Hurewicz',
                'Luzin',
                'manifold',
                'Menger',
                'Noetherian',
                'omega-bounded',
                'perfect',
                'Polish',
                'polyadic',
                'resolvable',
                'Rickart',
                'Rothberger',
                'shrinking',
                'scattered',
                'sub-stonean',
                'Toronto',
                'uniformizable',
                'universal cover',
                'Volterra',
                'zero-dimensional',
                'dimension',
            ])
                             
properties = TableFields([]])

topology = [header, definition_topology, properties, footer]
