from .general import header, footer
from ..generators.imports import *


definition_mnemo = TableFields(
    name = "Mnemo",
    fields = ["Personne","Action","Objet","Lieu","Habit","Musique","Nourriture"]
)


mnemo = [header, HTML("H1",{"Symbol"}), definition_mnemo, footer]
