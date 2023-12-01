from pathlib import Path


SUB_TABLE = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def map_chunk(string):
    # Map or identity.
    return SUB_TABLE.get(string, string)


def get_calibration_value(line):
    import re
    expression = (
        r'(?=(one|two|three|four|five|six|seven|eight|nine|\d))'
    )
    chunks = [
        re_match.group(1)
        for re_match in re.finditer(expression, line)
    ]
    chunks = [map_chunk(chunk) for chunk in chunks]

    if len(chunks) == 1:
        return int(''.join(chunks * 2))

    first_chunk, *_, last_chunk = chunks

    return int(first_chunk + last_chunk)


def main():
    data_directory = Path(__file__).parent / 'data'
    data_file_path = data_directory / '1.txt'
    data_string = data_file_path.read_text()

    input_lines = data_string.splitlines()

    print(
        sum(
            get_calibration_value(line)
            for line in input_lines
        )
    )


if __name__ == '__main__':
    main()
