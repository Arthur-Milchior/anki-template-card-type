from ...generators import *
from .footer import footer
from .names import names
from .notations import notations
from .header import header
from ..util import *

"""All informations about names, notations, and denoted by. Ask name number nameNumber potentially"""
namesNotationsDenotedBy = Cascade(child=
                                  [
                                      names(br),
                                      notations(br),
                                      DecoratedField('Representation', suffix=hr),
                                      DecoratedField('Denoted by', suffix=hr),
                                      DecoratedField('Japonais', suffix=hr),
                                      DecoratedField('Intuition', suffix=hr),
                                  ],
                                  cascade={"Names", "Notations",
                                           "Representation", "Denoted by"},
                                  field="NamesNotationsDenotedBy")

toNotations = Filled("Name",
                   Filled("Notation",
                         addBoilerplate([
                             names(),
                            notations(),
                         ])
                   )).assumeAsked("Notations")


toNames = Filled("Name",
                Filled("Notation",
                      addBoilerplate([
                          notations(),
                          names(),
                      ])
                )).assumeAsked("Names")
