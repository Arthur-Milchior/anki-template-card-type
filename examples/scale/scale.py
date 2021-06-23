from ...generators import *


def scale(octaveNumber=1, nbOctave=1, back=False, increase=True):
    # arrows: which arrow to show and in which order
    # Suffix -- End of field name

    # Values changing depending on which sides it goes
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
        f"{i-1}\\{i}" for i in range(end_number, start_number, -1)]
    increasingAlternate = [
        f"{i}/{i+1}" for i in range(start_number, end_number)]
    if back:
        if increase:
            fieldName = f"{start_number}/{end_number}\\{start_number}"
            alternates = increasingAlternate+decreasingAlternate
            suffix = "/\\"
            arrow = [start, increasingImage, end, decreasingImage, start]
        else:
            alternates = decreasingAlternate+increasingAlternate
            suffix = "\\/"
            fieldName = f"{end_number}\\{start_number}//{end_number}"
            arrow = [end, decreasingImage, start, increasingImage, end]
    else:
        if increase:
            alternates = increasingAlternate
            suffix = "/"
            fieldName = f"{start_number}/{end_number}"
            arrow = [start, increasingImage, end]
        else:
            suffix = "\\"
            alternates = decreasingAlternate
            fieldName = f"{end_number}\\{start_number}"
            arrow = [end, decreasingImage, start]

    field = FilledOrEmpty(fieldName,
                          {fieldName},
                          [{alternateField} for alternateField in alternates])

    octaveNumbers = [str(i)
                     for i in range(octaveNumber, octaveNumber+nbOctave)]
    octaveNumbersReverse = octaveNumbers[::-1]
    octaves = "".join(octaveNumbers)
    mandatoryFields = [f"{i}/{i+1}" for i in range(start_number, end_number)]

    nbOctaveText = f"""{nbOctave} octave{"s" if nbOctave>1 else ""}"""

    scales = (fieldName, field, [{mandatoryFieldName}
                                 for mandatoryFieldName in mandatoryFields])

    content = [Answer([scales, hr]),
               {"Instrument"}, {"Name"}, " ", {"Name2"}, hr,
               arrow,
               # nbOctaveText
               ]
    return MultipleRequirement(child=content, requireFilled=mandatoryFields)
