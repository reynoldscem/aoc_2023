from pathlib import Path
from math import prod
import re


def get_section_length(time, distance):
    from math import sqrt, ceil, floor
    upper, lower = (
        (-0.5 * (-time - sqrt(time**2 - 4 * distance))),
        (-0.5 * (-time + sqrt(time**2 - 4 * distance)))
    )
    if upper.is_integer():
        return int(upper - lower) - 1

    return int(upper) - int(lower)


def main():
    data_directory = Path(__file__).parent / 'data'
    data_file_path = data_directory / '1.txt'
    data_string = data_file_path.read_text()
    input_sections = data_string.split('\n')

    print(len(input_sections))

    time_line, distance_line, *_ = input_sections

    time = int(''.join(re.findall(r'\d+', time_line)))
    distance = int(''.join(re.findall(r'\d+', distance_line)))

    print(time, distance)

    print(get_section_length(time, distance))


if __name__ == '__main__':
    main()
