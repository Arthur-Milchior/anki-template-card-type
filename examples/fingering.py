from ..generators.imports import *

instrument = [{"Instrument name"}, {"Instrument image"}]
note = [{"Degree"},MultipleRequirement(child="/", requireFilled={"Degree","Function"}),{"Filled"}]
header = [instrument, hr,note]
fingerings = PotentiallyNumberedFields("Fingering",3)

fingering = [header,hr,fingerings]
