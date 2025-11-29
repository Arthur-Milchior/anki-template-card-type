from ...generators import *


def scale(octaveNumber=1, nbOctave=1, back=False, increase=True):
    """
    Ask the user to review scales over `nbOctave` octaves,
    starting at octave `octaveNumber`. Octaves are 1 2 3, named 0, 1 and 2 in fields
    `increase`: True if we start by the octave increasing,
    `back` whether to go both increasing and decreasing.
    """
    # arrows: which arrow to show and in which order
    # Suffix -- End of partitionFields name

    # Values changing depending on which sides it goes
    print(f"scale({octaveNumber=}, {nbOctave=}, {back=}, {increase=})")
    start_number = octaveNumber - 1
    end_number = octaveNumber + nbOctave - 1
    start_string = str(start_number)
    end_string = str(end_number)
    start_field = {start_string}
    end_field = {end_string}
    start_text = SUB(start_string)
    end_text = SUP(end_string)
    start = FilledOrEmpty(
        str(start_number),
        start_field,
        start_text
    )
    end = FilledOrEmpty(
        str(end_number),
        end_field,
        end_text
    )

    increasingImage = Image(f"_increasing_arrow.png")
    decreasingImage = Image(f"_decreasing_arrow.png")
    decreasingAlternate = [
        Field(f"{i}\\{i-1}", isMandatory=True) for i in range(end_number, start_number, -1)]
    increasingAlternate = [
        Field(f"{i}/{i+1}", isMandatory=True) for i in range(start_number, end_number)]
    print(f"  increasingAlternate=")
    for i in increasingAlternate:
        print("    " + str(i))
    print(f"  decreasingAlternate=")
    for d in decreasingAlternate:
        print("    " + str(d))
    if back:
        if increase:
            fieldName = f"{start_number}/{end_number}\\{start_number}"
            alternates = increasingAlternate+decreasingAlternate
            arrow = [start, increasingImage, end, decreasingImage, start]
        else:
            alternates = decreasingAlternate+increasingAlternate
            fieldName = f"{end_number}\\{start_number}/{end_number}"
            arrow = [end, decreasingImage, start, increasingImage, end]
    else:
        if increase:
            alternates = increasingAlternate
            fieldName = f"{start_number}/{end_number}"
            arrow = [start, increasingImage, end]
        else:
            alternates = decreasingAlternate
            fieldName = f"{end_number}\\{start_number}"
            arrow = [end, decreasingImage, start]
    print(f"{alternates=}")
    partitionFields = FilledOrEmpty(fieldName,
                          {fieldName},
                          [alternateField for alternateField in alternates])
    print(f"{partitionFields=}")

    octaveNumbers = [str(i)
                     for i in range(octaveNumber, octaveNumber+nbOctave)]
    octaveNumbersReverse = octaveNumbers[::-1]
    octaves = "".join(octaveNumbers)
    mandatoryFields = [f"{i}/{i+1}" for i in range(start_number, end_number)]
    if not back:
        mandatoryFields.append("Practice single direction")
    forbiddenFields = []
    if nbOctave == 1:
        forbiddenFields.append("Hide single octave")


    nbOctaveText = f"""{nbOctave} octave{"s" if nbOctave>1 else ""}"""

    content = [Answer([partitionFields, hr]),
               {"Instrument"},
               Filled("Position", ["Position ", {"Position"}, " "]),
               Filled("Tonic", [{"Tonic"}, " "]),
               FilledOrEmpty("Mode Notation", [{"Mode Notation"}, " "], Filled("Mode Name", [{"Mode Name"}, " "])),
               Filled("Specific", [{"Specific"}, " "]),
               Filled("Name", [br, {"Name"}]),
               hr,
               arrow,
               # nbOctaveText
               ]
    print(f"{mandatoryFields=}")
    print(f"{forbiddenFields=}")
    return MultipleRequirement(
        child=content,
        requireFilled=mandatoryFields,
        requireEmpty=forbiddenFields
    )
