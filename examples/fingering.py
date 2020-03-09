from ..generators import *

instrument = [{"Instrument name"}, {"Instrument image"}]
note = [{"Degree"}, MultipleRequirement(
    child="/", requireFilled={"Degree", "Function"}), {"Filled"}]
header = [instrument, hr, note]
fingerings = PotentiallyNumberedFields("Fingering", 3, classes="Definition")

fingering = [header, hr, fingerings]
