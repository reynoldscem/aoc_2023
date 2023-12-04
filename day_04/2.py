from collections import Counter
from pathlib import Path
import re


class Card:
    def __init__(self, line):
        card_index_substring, rest = line.split(':')
        winning_numbers_substring, played_numbers_substring = rest.split('|')

        self.index = int(re.search(r'\d+', card_index_substring).group())
        self.winning_numbers = self.get_numbers(winning_numbers_substring)
        self.played_numbers = self.get_numbers(played_numbers_substring)

    @property
    def match_count(self):
        intersection = self.winning_numbers.intersection(self.played_numbers)

        return len(intersection)

    @property
    def wins_cards(self):
        return list(range(self.index + 1, self.index + self.match_count + 1))

    @staticmethod
    def get_numbers(numbers_string):
        return set(map(int, re.findall(r'\d+', numbers_string)))


class CardCollection:
    def __init__(self, lines):
        cards = [Card(line) for line in lines]
        self.cards = {
            card.index: card
            for card in cards
        }
        self.max_index = max(self.cards.keys())
        self.card_counts = Counter(self.cards.keys())

    def play(self):
        for index, card in self.cards.items():
            this_card_count = self.card_counts[index]

            for card_index in card.wins_cards:
                try:
                    self.card_counts[card_index] += this_card_count
                except KeyError:
                    pass

    @property
    def card_count(self):
        return sum(self.card_counts.values())


def main():
    data_directory = Path(__file__).parent / 'data'
    data_file_path = data_directory / '1.txt'
    data_string = data_file_path.read_text()
    input_lines = data_string.splitlines()

    card_collection = CardCollection(input_lines)
    card_collection.play()
    print(card_collection.card_count)


if __name__ == '__main__':
    main()
