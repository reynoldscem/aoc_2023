from pathlib import Path


def get_first_digit(string):
    import re

    return re.search(r'\d', string).group()


def get_calibration_value(line):
    return int(get_first_digit(line) + get_first_digit(line[::-1]))


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
