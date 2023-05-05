import argparse
import os.path
from typing import List, NamedTuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PassPattern = NamedTuple("PassPattern", [('first', int), ('second', int), ('val', str)])
InputType = NamedTuple("InputType", [("pattern", PassPattern), ("password", str)])


def parse_input(s: str) -> List[InputType]:
    inputs: List[InputType] = []
    for line in s.splitlines():
        lineArr = line.split()
        part1, part2, part3 = lineArr[0], lineArr[1], lineArr[2]
        least_s, _, most_s = part1.partition('-')
        inputs.append(InputType(PassPattern(int(least_s) - 1, int(most_s) - 1, part2[0]), part3))
    return inputs


def compute(s: str) -> int:
    passwords_data = parse_input(s)
    n_valid = 0
    for pass_data in passwords_data:
        first_c, second_c = pass_data.password[pass_data.pattern.first], pass_data.password[pass_data.pattern.second]
        first_matches = first_c == pass_data.pattern.val
        second_matches = second_c == pass_data.pattern.val
        if first_matches and second_matches:
            continue
        elif (not first_matches) and (not second_matches):
            continue
        else:
            n_valid += 1

    return n_valid


INPUT_S = '''\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 1),
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
