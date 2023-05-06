import argparse
import os.path
from typing import List, Tuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(s: str) -> List[str]:
    return [line for line in s.splitlines()]


def binarySearch(max_high: int, seatCode: str, idx: int, low_char: str, high_char: str) -> Tuple[int, int]:
    low = 0
    high = max_high
    while low < high:
        mid = int((low + high) / 2)
        c = seatCode[idx]
        if c == low_char:
            high = mid
        elif c == high_char:
            low = mid + 1
        idx += 1
    return low, idx


def compute(s: str) -> int:
    seat_codes = parse_input(s)
    n_rows = 128
    n_cols = 8
    occupied_seats: List[bool] = [False for i in range(n_rows*n_cols)]
    for seatCode in seat_codes:
        idx = 0
        row_num, idx = binarySearch(n_rows-1, seatCode, idx, 'F', 'B')
        col_num, idx = binarySearch(n_cols-1, seatCode, idx, 'L', 'R')
        seat_id = row_num * n_cols + col_num
        occupied_seats[seat_id] = True

    mid_seat = int(n_rows*n_cols/2)
    for delta_idx in range(int(n_rows*n_cols/2)):
        test_seat_ids = [mid_seat - delta_idx, mid_seat + delta_idx]
        for test_seat in test_seat_ids:
            if not occupied_seats[test_seat]:
                if occupied_seats[test_seat+1] and occupied_seats[test_seat-1]:
                    return test_seat
    return 0


INPUT_S = '''\
FBFBBFFRLR
BFFFBBFRRR
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 567),
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
