from ..generators import *
from .util import *

instrument = [{"Instrument name"}, {"Instrument image"}]
note = [{"Degree"}, MultipleRequirement(
    child="/", requireFilled={"Degree", "Function"}), {"Filled"}]
header = [instrument, hr, note]
fingerings = PotentiallyNumberedFields("Fingering",
                                        4, 
                                        numbered_field=numbered_field,
                                        classes="Definition")

fingering = addBoilerplate(fingerings)
