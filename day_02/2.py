from pathlib import Path


class Game:
    def __init__(self, game_string):
        import re

        pattern = r'Game (\d+): (.*)'
        game_id_string, rest = re.search(pattern, game_string).groups()

        self.game_id = int(game_id_string)

        round_strings = rest.split(';')

        self.rounds = [
            Round(round_string)
            for round_string in round_strings
        ]

    @property
    def fewest_plausible_cubes(self):
        from collections import defaultdict
        fewest_cubes = defaultdict(int)

        for this_round in self.rounds:
            for colour, cube_count in this_round.colour_to_count.items():
                fewest_cubes[colour] = max(cube_count, fewest_cubes[colour])

        return fewest_cubes

    def power(self):
        from math import prod

        return prod(self.fewest_plausible_cubes.values())


class Round:
    def __init__(self, round_string):
        colour_drawcount_pairs = [
            entry.strip().split()[::-1]
            for entry in round_string.split(',')
        ]
        self.colour_to_count = {
            colour: int(drawcount_string)
            for colour, drawcount_string in colour_drawcount_pairs
        }

    def __getitem__(self, key):
        return self.colour_to_count.get(key, 0)


def main():
    data_directory = Path(__file__).parent / 'data'
    data_file_path = data_directory / '1.txt'
    data_string = data_file_path.read_text()
    input_lines = data_string.splitlines()

    games = [Game(line) for line in input_lines]

    power_sum = sum(
        game.power() for game in games
    )
    print(power_sum)


if __name__ == '__main__':
    main()
