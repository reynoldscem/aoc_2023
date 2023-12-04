from pathlib import Path
import re


class Card:
    def __init__(self, line):
        card_index_substring, rest = line.split(':')
        winning_numbers_substring, played_numbers_substring = rest.split('|')

        self.index = int(re.search(r'\d+', card_index_substring).group())
        self.winning_numbers = self.get_numbers(winning_numbers_substring)
        self.played_numbers = self.get_numbers(played_numbers_substring)

        # print(self.winning_numbers)
        # print(self.played_numbers)
        # print()

    @property
    def points(self):
        intersection = self.winning_numbers.intersection(self.played_numbers)

        if intersection:
            score = 2 ** (len(intersection) - 1)
        else:
            score = 0

        # print(score)

        return score

    @staticmethod
    def get_numbers(numbers_string):
        return set(map(int, re.findall(r'\d+', numbers_string)))


def main():
    data_directory = Path(__file__).parent / 'data'
    data_file_path = data_directory / '1.txt'
    data_string = data_file_path.read_text()
    input_lines = data_string.splitlines()

    print(
        sum(
            Card(line).points
            for line in input_lines
        )
    )


if __name__ == '__main__':
    main()
