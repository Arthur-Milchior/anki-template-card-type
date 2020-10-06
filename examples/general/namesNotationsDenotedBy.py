from ...generators import *
from .footer import footer
from .names import names
from .notations import notations
from .header import header

"""All informations about names, notations, and denoted by. Ask name number nameNumber potentially"""
namesNotationsDenotedBy = Cascade(child=
                                  [
                                      names(),
                                      notations,
                                      DecoratedField( 'Representation', suffix=hr),
                                      DecoratedField('Denoted by', suffix=hr)],
                                  cascade={"Names", "Notations",
                                           "Representation", "Denoted by"},
                                  field="NamesNotationsDenotedBy")

toNotations = Filled("Name",
                   Filled("Notation",
                         [
                             header,
                             notations,
                             names(),
                             footer,
                         ]
                   )).assumeAsked("Notations")


toNames = Filled("Name",
                Filled("Notation",
                      [
                          header,
                          names(),
                          notations,
                          footer,
                      ]
                )).assumeAsked("Names")
