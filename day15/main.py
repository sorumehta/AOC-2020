import argparse
import os.path
from typing import List

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(s: str) -> List[int]:
    return [int(num) for num in s.split(',')]


def compute(s: str) -> int:
    numbers = parse_input(s)
    spoken_record: dict[int, list[int]] = {}
    end_num = 30000000
    last_spoken = numbers[0]
    for n_turn in range(end_num):
        if n_turn < len(numbers):
            spoken_record[last_spoken] = [n_turn]
            last_spoken = numbers[n_turn]
        else:
            # first derive the number to speak based on last spoken, then insert the last_spoken
            # the reason is, if we insert last_spoken first, then it will always be found in record
            if last_spoken in spoken_record:
                num_to_speak = n_turn - spoken_record[last_spoken][-1]
                spoken_record[last_spoken].append(n_turn)
            else:
                num_to_speak = 0
                spoken_record[last_spoken] = [n_turn]
            last_spoken = num_to_speak
    return last_spoken


INPUT_S = '''\
3,1,2
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 1836),
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
