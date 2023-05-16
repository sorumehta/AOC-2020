import math
import argparse
import os.path
from typing import List, Tuple, Optional

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def parse_input(s: str) -> Tuple[int, List[Optional[int]]]:
    inputList = s.splitlines()
    busIds = []
    for id in inputList[1].split(','):
        if id != 'x':
            busIds.append(int(id))
        else:
            busIds.append(None)
    return int(inputList[0]), busIds


def next_factor(number: int, start_from: int, early_stop: int = None):
    for i in range(start_from + 1, start_from + number + 1):
        if i % number == 0:
            return i
        if early_stop and i > early_stop:
            break
    return None


def get_earliest_timestamp(all_busIds):
    busIds = list(filter(lambda x: x is not None, all_busIds))
    max_busId = max(busIds)
    max_busId_idx = all_busIds.index(max_busId)
    max_bus_depart_time = 1
    while True:
        max_bus_depart_time = next_factor(max_busId, max_bus_depart_time)
        found_ideal_schedule = True
        for idx, busId in enumerate(all_busIds):
            if idx == max_busId_idx or busId is None:
                continue
            ideal_depart_time = max_bus_depart_time + idx - max_busId_idx
            if ideal_depart_time % busId != 0:
                found_ideal_schedule = False
                break
        if found_ideal_schedule:
            return max_bus_depart_time - max_busId_idx


def lcm_multiple(nums: list[int]):
    lcm_res = 1
    for n in nums:
        lcm_res = lcm(lcm_res, n)
    return lcm_res


def compute(s: str) -> int:
    _, all_busIds = parse_input(s)
    busIds = list(filter(lambda x: x is not None, all_busIds))
    all_busIds_subset = []
    total_valid_ids_in_subset = 0
    for id in all_busIds:
        all_busIds_subset.append(id)
        if id is not None:
            total_valid_ids_in_subset += 1
            if total_valid_ids_in_subset > len(busIds) / 2:
                break
    print(f"{all_busIds_subset=}")
    earliest_timestamp_subset = get_earliest_timestamp(all_busIds_subset)
    print(f"{earliest_timestamp_subset=}")
    busIds_subset = list(filter(lambda x: x is not None, all_busIds_subset))
    lcm_subset = lcm_multiple(busIds_subset)
    remaining_bus_ids: list[tuple[int, int]] = []
    for idx, busId in enumerate(all_busIds):
        if idx < len(all_busIds_subset) or busId is None:
            continue
        remaining_bus_ids.append((idx, busId))
    test_timestamp = earliest_timestamp_subset
    while True:
        test_timestamp += lcm_subset
        found_ideal_schedule = True
        for idx, busId in remaining_bus_ids:
            ideal_depart_time = test_timestamp + idx
            if ideal_depart_time % busId != 0:
                found_ideal_schedule = False
                break
        if found_ideal_schedule:
            return test_timestamp


INPUT_S = '''\
939
67,7,x,59,61
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 1261476),
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
