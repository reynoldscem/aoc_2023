from pathlib import Path

CUBE_COUNTS = {
    'red': 12,
    'green': 13,
    'blue': 14
}


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
    def possible(self):
        for this_round in self.rounds:
            for colour, max_count in CUBE_COUNTS.items():
                if this_round[colour] > max_count:
                    return False
        return True


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
    possible_games = [game for game in games if game.possible]
    id_sum = sum(game.game_id for game in possible_games)

    print(id_sum)


if __name__ == '__main__':
    main()
