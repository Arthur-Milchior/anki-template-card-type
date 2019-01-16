from ..generators.imports import *
from .general import header, footer


definition_topology = TableFields(
    name = "Topology",
    fields = ["Set", "Definition", "Definition2", "Opens", "Compactification of", "Completion of", "Base", "Base2", "Order", "Metric", "Prebase", "Prebase2"]
)
compactness= TableFields(name="Compactness",
                         fields = ['A paracompact',
                                   'Compact',
                                   'Sequentially compact',
                                   'Locally compact',
                                   'Feebly compact',
                                   'Limit point compact',
                                   'Paracompact',
                                   'Sigma-compact',
                                   'Countably compact',
                                   'Hemicompact',
                                   'Mesocompact',
                                   'Metacompact',
                                   'Orthocompact',
                                   'Pseudocompact',
                                   'Realcompact',
                                   'Supercompact',
                                   'Freebly compact']
)

bounded =TableFields(name="Bounded",
            fields=[
                'bounded',
                'totally bounded'
            ]
)

points = TableFields(name="Points",
 fields=[
'Limit points',
'Isolated points',
])

sets =TableFields(name="Sets",
            fields=[
                'clopen',
                'dense',
            ]
)
separationTable = [
    ['T0/Kolmogorov',None],
    ['T1/accessible/Tichonov/Fréchet topology','R0/Symmetric'],
    ['T2/Hausdorff/separated','R1/preregular'],
    ['T2 1/2/Urysohn',None],
    ['Completely T2/completely Hausdorff',None],
    ['T3/regular Hausdorff','Regular'],
    ['T3 1/2/Tychonoff','Completely regular'],
    ['Normal T0','Normal'],
    ['T4/normal Hausdorff','Normal regular'],
    ['Completely normal T0', 'Completely normal'],
    ['T5/completely normal Hausdorff','Completely normal regular'],
    ['Perfectly normal T0', 'Perfectly normal'],
    ['T6/perfectly normal Hausdorff','Perfectly normal regular'],
]

other_separations =['Weak Hausdorff', 'locally Hausdorff', 'Collectionwise Hausdorff',
 'Locally regular', 'Locally normal', 'Collectionwise normal',
 'Monotonically normal', 'Paranormal', 'Pseudonormal',]

allSeparations=[]+other_separations
for line in separationTable:
    for elt in line:
        if elt is not None:
            allSeparations.append(elt)

separations= TableFields(
    name="Separation",
    fields=allSeparations)

connexion = TableFields(name="Connexion",
            fields = [
                'Connected',
                'Arc connected',
                'Path connected',
                'Locally connected',
                'Locally simply connected',
                'Extremmaly disconnected',
                'Hyperconnected',
                'N connected',
                'Semi-locally simply connected',
                'Simply connected',
                'Simply-connected at infinity',
                'Totally disconnected',
                'Ultraconnected'
            ])

group = TableFields(name="Group",
            fields=[
                'Connected',
                'Fundamental group',
            ])

cardinal = TableFields(name="Cardinal",
            fields=[
                'Cardinality',
                'Locally finite',
                'Sequential',
                'First-countable',
                'Second-countable',
                'Separable',
                'Lindelof',
            ])

others = TableFields(name="Other",
            fields=[
                'Interior',
                'Closure',
                'Alexandrov',
                'Baire',
                'Cellular',
                'Sober',
                'Semiregular',
                'Quasiregular',
                'Contractible',
                'D-space',
                'Door space',
                'Dowker',
                'Dyadic',
                'Ends',
                'H-closed',
                'Hurewicz',
                'Luzin',
                'Manifold',
                'Menger',
                'Noetherian',
                'Omega-bounded',
                'Perfect',
                'Polish',
                'Polyadic',
                'Resolvable',
                'Rickart',
                'Rothberger',
                'Shrinking',
                'Scattered',
                'Sub-stonean',
                'Toronto',
                'Uniformizable',
                'Universal cover',
                'Volterra',
                'Zero-dimensional',
                'Dimension',
            ])
                             
properties = [compactness,bounded,points, sets, separations,connexion,
              group, cardinal,others]
topology = [header, definition_topology, properties, footer]
topologyBody = topology
topologyHead = topology
