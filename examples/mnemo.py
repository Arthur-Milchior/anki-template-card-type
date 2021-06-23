from ..generators import *
from .general import footer, header

definition_mnemo = TableFields(
    name="Mnemo",
    fields=[
        {"field": "Personne",
         "classes": "Definition"},
        {"field": "Action",
         "classes": "Definition2"},
        {"field": "Objet",
         "classes": "Definition3"},
        {"field": "Lieu",
         "classes": "Definition4"},
        {"field": "Habit",
         "classes": "Definition5"},
        {"field": "Musique",
         "classes": "Definition6"},
        {"field": "Nourriture",
         "classes": "Definition7"},
    ]
)


mnemo = [header, HTML("H1", {"Symbol"}), definition_mnemo, footer]
