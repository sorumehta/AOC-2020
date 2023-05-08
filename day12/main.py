import argparse
import os.path
from typing import NamedTuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Instruction(NamedTuple):
    d: str
    n: int


def parse_input(s: str):
    instructions: list[Instruction] = []
    for line in s.splitlines():
        d = line[0]
        n = int(line[1:])
        instructions.append(Instruction(d, n))
    return instructions


EAST = 0
SOUTH = 1
WEST = 2
NORTH = 3


def compute(s: str) -> int:
    all_instructions = parse_input(s)

    x = 0
    y = 0
    way = (10, 1)

    def rotateVector(direction_enum: int, vector: tuple[int, int]):
        rotation_matrices = [((1, 0), (0, 1)), ((0, 1), (-1, 0)), ((-1, 0), (0, -1)), ((0, -1), (1, 0))]  # E, S, W, N
        matrix = rotation_matrices[direction_enum]
        new_vector_x = vector[0]*matrix[0][0] + vector[1]*matrix[0][1]
        new_vector_y = vector[0] * matrix[1][0] + vector[1] * matrix[1][1]
        return new_vector_x, new_vector_y

    def deltaPosition(direction_enum: int, n: int):
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # E, S, W, N
        return n * directions[direction_enum][0], n * directions[direction_enum][1]

    for inst in all_instructions:
        if inst.d in ['N', 'S', 'E', 'W']:
            direction = {'N': NORTH, 'S': SOUTH, 'E': EAST, 'W': WEST}[inst.d]
            pos_delta = deltaPosition(direction, inst.n)
            way = (way[0] + pos_delta[0], way[1] + pos_delta[1])
        elif inst.d == 'F':
            x += way[0] * inst.n
            y += way[1] * inst.n
        elif inst.d == 'L':
            d= 0
            n_rotations = inst.n // 90
            d = (4 + d - n_rotations) % 4
            way = rotateVector(d, way)

        elif inst.d == 'R':
            d= 0
            n_rotations = inst.n // 90
            d = (4 + d + n_rotations) % 4
            way = rotateVector(d, way)

    return abs(x) + abs(y)


INPUT_S = '''\
F10
N3
F7
R90
F11
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 286),
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
