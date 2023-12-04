from pathlib import Path


def main():
    data_directory = Path(__file__).parent / 'data'
    data_file_path = data_directory / '1.txt'
    data_string = data_file_path.read_text()
    input_lines = data_string.splitlines()

    char_2d_array = [list(line) for line in input_lines]

    from scipy import ndimage
    import numpy as np
    grid = np.array(char_2d_array)

    # Find locations of each type of cell.
    is_numeric_mask = np.logical_and(grid >= '0', grid <= '9')
    is_null_mask = (grid == '.')
    is_symbol_mask = np.logical_not(
        np.logical_or(
            is_numeric_mask,
            is_null_mask
        )
    )

    # A square 3x3 structuring element finds 8-neighbours for each
    #  symbol.
    structuring_element = ndimage.generate_binary_structure(2, 2)
    symbol_neighbour_mask = ndimage.binary_dilation(
        is_symbol_mask, structure=structuring_element
    )

    # A part of a number, which is also a neighbour to a symbol
    candidate_positions_mask = np.logical_and(
        symbol_neighbour_mask,
        is_numeric_mask
    )

    # Dilate in a horizontal line for every part of a number found as to be
    #  a neighbour of a symbol (or neighbour of a neighbour of...) in
    #  future rounds. Stop when the mask no longer grows.
    line_structuring_element = np.array([[1, 1, 1]])
    while True:
        row_dilated_candidate_positions_mask = ndimage.binary_dilation(
            candidate_positions_mask,
            line_structuring_element
        )
        expanded_candidate_positions_mask = np.logical_and(
            row_dilated_candidate_positions_mask,
            is_numeric_mask
        )
        if np.all(
                candidate_positions_mask == expanded_candidate_positions_mask):
            break
        else:
            candidate_positions_mask = expanded_candidate_positions_mask

    # Only grab cells which sit inside the mask, grow the grid so that
    #  when we turn it back into a string you don't get wraparound numbers
    #  being concatenated.
    masked_grid = np.copy(grid)
    masked_grid[np.logical_not(candidate_positions_mask)] = '.'
    padded_grid = np.pad(masked_grid, 1, constant_values='.')

    string_with_only_valid_numbers = ''.join(padded_grid.flatten().tolist())

    # Find numbers and sum.
    import re
    integers = [
        int(entry)
        for entry in re.findall(r'\d+', string_with_only_valid_numbers)
    ]

    print(sum(integers))


if __name__ == '__main__':
    main()
