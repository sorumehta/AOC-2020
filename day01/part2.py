import argparse
import os.path
from typing import List

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(s: str) -> List[int]:
    return [int(line) for line in s.splitlines()]


def compute(s: str) -> int:
    target = 2020
    numbers = parse_input(s)
    sortedNums = sorted(numbers)
    low = 0
    for higher in range(low + 2, len(numbers)):
        low = 0
        high = higher - 1
        while low < high:
            if sortedNums[low] + sortedNums[high] + sortedNums[higher] == target:
                return sortedNums[low] * sortedNums[high] * sortedNums[higher]
            elif sortedNums[low] + sortedNums[high] + sortedNums[higher] < target:
                low += 1
            else:
                high -= 1
    return -1


INPUT_S = '''\
1721
979
366
299
675
1456
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 241861950),
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
