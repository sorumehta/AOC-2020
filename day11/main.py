import argparse
import os.path
from typing import List, Tuple, NamedTuple, TypedDict
import copy
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

FLOOR = 0
EMPTY = 1
OCCUPIED = 2


def parse_input(s: str) -> List[List[int]]:
    seats: List[List[int]] = []
    for line in s.splitlines():
        row: List[int] = []
        for c in line:
            if c == '.':
                row.append(FLOOR)
            elif c == 'L':
                row.append(EMPTY)
        seats.append(row)
    return seats


class AdjacentRows(TypedDict):
    topRow: List[Tuple[int, int]]
    bottomRow: List[Tuple[int, int]]
    leftRow: List[Tuple[int, int]]
    rightRow: List[Tuple[int, int]]
    topLeftRow: List[Tuple[int, int]]
    topRightRow: List[Tuple[int, int]]
    bottomLeftRow: List[Tuple[int, int]]
    bottomRightRow: List[Tuple[int, int]]


def getAllAdjacentRows(i: int, j: int, n_rows: int, n_cols: int):
    topRow = list(reversed([(k, j) for k in range(i)]))
    topLeftRow = list(reversed([(k, j - i + k) for k in range(i) if 0 <= j - i + k < n_cols]))
    topRightRow = list(reversed([(k,j + i - k) for k in range(i) if 0 <= j + i - k < n_cols]))

    bottomRow = [(k,j) for k in range(i + 1, n_rows)]
    bottomLeftRow = [(k,j - (k - i)) for k in range(i + 1, n_rows) if 0 <= j - (k - i) < n_cols]
    bottomRightRow = [(k, j + (k - i)) for k in range(i + 1, n_rows) if 0 <= j + (k - i) < n_cols]

    leftRow = list(reversed([(i, k) for k in range(j)]))
    rightRow = [(i, k) for k in range(j + 1, n_cols)]

    return AdjacentRows(topRow=topRow, bottomRow=bottomRow, leftRow=leftRow, rightRow=rightRow,
                      topLeftRow=topLeftRow, topRightRow=topRightRow, bottomLeftRow=bottomLeftRow,
                      bottomRightRow=bottomRightRow)


def doesSeatGetOccupied(currSeats: List[List[int]], i: int, j: int) -> bool:
    n_rows = len(currSeats)
    n_cols = len(currSeats[0])
    isAdjacentSeatOccupied = False
    adjacentRows = getAllAdjacentRows(i, j, n_rows, n_cols)
    for rowType in list(adjacentRows.keys()):
        for pos in adjacentRows[rowType]:
            if currSeats[pos[0]][pos[1]] != FLOOR:
                if currSeats[pos[0]][pos[1]] == OCCUPIED:
                    isAdjacentSeatOccupied = True
                break
    return not isAdjacentSeatOccupied


def doesSeatGetEmpty(currSeats: List[List[int]], i: int, j: int) -> bool:
    n_rows = len(currSeats)
    n_cols = len(currSeats[0])
    moreThan4SeatsOccupied = False
    numSeatsOccupied = 0
    adjacentRows = getAllAdjacentRows(i, j, n_rows, n_cols)
    for rowType in list(adjacentRows.keys()):
        for pos in adjacentRows[rowType]:
            if currSeats[pos[0]][pos[1]] != FLOOR:
                if currSeats[pos[0]][pos[1]] == OCCUPIED:
                    numSeatsOccupied += 1
                break
    if numSeatsOccupied > 4:
        moreThan4SeatsOccupied = True
    return moreThan4SeatsOccupied


def actOnSeat(currSeats: List[List[int]], i: int, j: int) -> int:
    if currSeats[i][j] == EMPTY and doesSeatGetOccupied(currSeats, i, j):
        return OCCUPIED
    elif currSeats[i][j] == OCCUPIED and doesSeatGetEmpty(currSeats, i, j):
        return EMPTY
    return currSeats[i][j]


def compute(s: str) -> int:
    currSeats = parse_input(s)
    newSeats: List[List[int]] = []
    for row in currSeats:
        newSeats.append([FLOOR for i in range(len(row))])

    roundNo = 0
    lastRoundSeats = None
    while lastRoundSeats != newSeats:
        roundNo += 1
        # print(f"starting {roundNo=}")
        for i in range(len(currSeats)):
            for j in range(len(currSeats[0])):
                newSeats[i][j] = actOnSeat(currSeats, i, j)
        lastRoundSeats = copy.deepcopy(currSeats)
        currSeats = copy.deepcopy(newSeats)
    numOccupied = sum([row.count(OCCUPIED) for row in currSeats])
    return numOccupied


INPUT_S = '''\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 26),
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
