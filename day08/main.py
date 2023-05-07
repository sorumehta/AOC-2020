import argparse
import os.path
from typing import NamedTuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Instruction(NamedTuple):
    op: str
    arg: int


def parse_input(s: str):
    code: list[Instruction] = []
    for line in s.splitlines():
        opc, n_s = line.split()
        n = int(n_s)
        code.append(Instruction(opc, n))
    return code

def compute_code(code:  list[Instruction]):
    visited: set[int] = set()
    acc = 0
    ptr = 0
    while (ptr not in visited) and (ptr < len(code)):
        visited.add(ptr)
        inst = code[ptr]
        if inst.op == 'nop':
            ptr += 1
        elif inst.op == 'acc':
            acc += inst.arg
            ptr += 1
        elif inst.op == 'jmp':
            ptr += inst.arg
    return acc, ptr


def compute(s: str) -> int:
    code = parse_input(s)
    flip = {'nop': 'jmp', 'jmp': 'nop'}
    for idx, inst in enumerate(code):
        if inst.op in list(flip.keys()):
            new_code = code[:]
            new_code[idx] = Instruction(flip[inst.op], inst.arg)
            acc, ptr = compute_code(new_code)
            if ptr >= len(code):
                print(f"changing {inst.op} to {flip[inst.op]} at idx {idx} worked")
                return acc
    return 0

INPUT_S = '''\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 8),
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
