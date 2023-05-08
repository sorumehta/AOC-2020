import argparse
import math
import os.path
from typing import List
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(s: str) -> List[int]:
    return [int(line) for line in s.splitlines()]


def get_candidates(arr, pos, solution) -> list[int]:
    candidates = []
    last_idx = arr.index(solution[-1]) if solution else 0
    last_sol_el = arr[last_idx]
    for el in arr[last_idx+1:]:
        if el - last_sol_el <= 3:
            candidates.append(el)
        elif el - last_sol_el > 3:
            break
    return candidates


def compute_combinations(arr: list[int], pos: int, solution: list[int]) -> int:
    if solution and solution[-1] == arr[-1]:
        return 1
    candidates = get_candidates(arr, pos, solution)
    arrangements = 0
    for cand in candidates:
        arrangements += compute_combinations(arr, pos+1, solution + [cand])
    return arrangements


def next_contiguous_chunk(arr, search_start_idx):
    i = search_start_idx
    while i < len(arr) - 1:
        if arr[i+1] - arr[i] == 1:
            start = i
            while i < len(arr) and arr[i+1] - arr[i] == 1:
                i += 1
            return start, i
        i += 1
    return None, None


# Since we have a restriction of the next number being at most 3 higher than previous one,
# and we know that the numbers are continouosly increasing, we can count arrangements by removing
# the last three numbers in the list, and doing same for the remaining list, and so on.
def combs(n: int):
    dp = [0 for i in range(n+1)]
    for i in range(n+1):
        if i == 0:
            dp[i] = 1
        elif i == 1:
            dp[i] = 1
        elif i == 2:
            dp[i] = 2
        else:
            dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
    return dp[n]


def compute(s: str) -> int:
    numbers = parse_input(s)
    sorted_nums = [0] + sorted(numbers)
    sorted_nums.append(sorted_nums[-1]+3)
    combinations = 1
    i = 0
    while i < len(sorted_nums):
        start, end = next_contiguous_chunk(sorted_nums, i)
        if start is not None:
            combinations *= combs(end - start)
            i = end + 1
        else:
            break
    return combinations


INPUT_S = '''\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 19208),
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
