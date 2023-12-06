from pathlib import Path
import re


class RangeMap:
    def __init__(self):
        self.range_pairs = []

    def add_range_pair(self, dest_start, source_start, range_length):
        self.range_pairs.append(
            (
                range(source_start, source_start + range_length),
                range(dest_start, dest_start + range_length)
            )
        )

    def __getitem__(self, key):
        for source_range, dest_range in self.range_pairs:
            if key in source_range:
                return (key - source_range.start) + dest_range.start
        return key

    @classmethod
    def make_from_string(cls, string):
        map_object = cls()
        lines = string.splitlines()
        for line in lines[1:]:
            numbers = list(map(int, re.findall(r'\d+', line)))
            map_object.add_range_pair(*numbers)

        return map_object


def get_all_seeds(seed_numbers):
    for base, length in zip(seed_numbers[::2], seed_numbers[1::2]):
        yield range(base, base + length)


def map_seed(maps, seed):
    value = seed
    for this_map in maps:
        value = this_map[value]

    return value


def main():
    data_directory = Path(__file__).parent / 'data'
    data_file_path = data_directory / '1.txt'
    data_string = data_file_path.read_text()
    input_sections = data_string.split('\n\n')

    seeds_section, *map_sections = input_sections

    seed_numbers = list(map(int, re.findall(r'\d+', seeds_section)))
    from itertools import chain
    seeds = chain.from_iterable(get_all_seeds(seed_numbers))
    maps = [
        RangeMap.make_from_string(map_string)
        for map_string in map_sections
    ]
    print('Start work!')
    from joblib import Parallel, delayed
    mapped_seeds = Parallel(
        n_jobs=11, return_as='generator', verbose=50
    )(
        delayed(map_seed)(maps, seed)
        for seed in seeds
    )

    print(min(mapped_seeds))


if __name__ == '__main__':
    main()
