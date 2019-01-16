from .general import header, footer
from ..generators.imports import *

definition_programmingLanguage = TableFields(
    name = "ProgrammingLanguage",
    fields = []
)
properties = TableFields([
    "Creator",
    "Storage management",
    "Pointer access",
    "Assignation by",
    "Object",
    "Functional",
    "Imperative",
    "Logic",
    "Declarative",
    "Event",
    "Concurrential",
    "Strong/weak typing",
    "Static/dynamic type",
    "Purity",
    "Strict",
    "Lazy",
    "Eager",
    "Interpreted",
    "Compiled",
    "Synchrone",
    "Asynchrone",
    "Parallel",
    "Distributed",
    "Scheduled",
    "Level",
    "Domain",
    "Maintener",
])

programmingLanguage = [header, properties, footer]
