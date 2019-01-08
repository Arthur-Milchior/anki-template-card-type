import aqt
import json
from copy import copy

from .debug import debug, assertEqual, assertType, startDebug, endDebug

from .generators.imports import *

from .templates.templates import compile_, clean, tagsToEdit
from .templates.soupAndHtml import soupFromTemplate, templateFromSoup

