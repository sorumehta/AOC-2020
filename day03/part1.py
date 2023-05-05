import argparse
import os.path
from typing import List, Tuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(s: str) -> List[List[int]]:
    area_map = []
    for line in s.splitlines():
        row_map = []
        for char in line:
            if char == '.':
                row_map.append(0)
            elif char == '#':
                row_map.append(1)
            else:
                raise Exception(f"unexpected input: {char}")
        area_map.append(row_map)
    return area_map


def getNextPosition(pos: Tuple[int, int], row_delta, col_delta, n_rows, n_cols) -> Tuple[int, int]:
    new_row = pos[0] + row_delta
    new_col = pos[1] + col_delta
    assert new_row <= n_rows
    return new_row, new_col % n_cols


def compute(s: str) -> int:
    areaMap = parse_input(s)
    n_trees = 0
    position = (0, 0)
    while position[0] < len(areaMap):
        if areaMap[position[0]][position[1]] == 1:
            n_trees += 1
        position = getNextPosition(position, 1, 3, len(areaMap), len(areaMap[0]))
    return n_trees


INPUT_S = '''\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 7),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    parser.add_argument('--parse-input', action='store_true', help='Print the output of parse_input function')
    args = parser.parse_args()
    if args.parse_input:
        print(parse_input(INPUT_S))
    else:
        with open(args.data_file) as f, timing():
            print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
