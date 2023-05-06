import argparse
import os.path
from typing import List, Set, Optional
import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(s: str):
    grps: List[List[str]] = []
    for grp in s.split('\n\n'):
        grps.append(grp.splitlines())
    return grps


def compute(s: str) -> int:
    groups = parse_input(s)
    total_yes = 0
    for grp in groups:
        all_yes: Optional[Set] = None
        for ind_yes in grp:
            if all_yes is None:
                all_yes = set(list(ind_yes))
            else:
                all_yes = all_yes.intersection(set(list(ind_yes)))
        total_yes += len(all_yes)
    return total_yes


INPUT_S = '''\
abc

a
b
c

ab
ac

a
a
a
a

b
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 6),
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
