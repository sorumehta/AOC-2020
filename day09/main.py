import argparse
import os.path
from typing import List
import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(s: str) -> List[int]:
    return [int(line) for line in s.splitlines()]


def twoSum(numbers: list[int], target: int):
    sortedNums = sorted(numbers)
    low = 0
    high = len(numbers) - 1
    while low < high:
        if sortedNums[low] + sortedNums[high] == target:
            return 1
        elif sortedNums[low] + sortedNums[high] < target:
            low += 1
        else:
            high -= 1
    return -1


def compute(s: str) -> int:
    numbers = parse_input(s)
    len_prev_range = 25
    invalid_num = 0
    for i in range(len_prev_range+1, len(numbers)):
        if twoSum(numbers[i-len_prev_range:i], numbers[i]) == -1:
            invalid_num = numbers[i]
            break
    low = 0
    high = 0
    window_sum = numbers[high]
    while high < len(numbers):
        if window_sum > invalid_num:
            while window_sum > invalid_num:
                window_sum -= numbers[low]
                low += 1
                if low > high:
                    high = low
                    window_sum = numbers[high]
        elif window_sum < invalid_num:
            high += 1
            window_sum += numbers[high]
        else:
            return max(numbers[low:high+1]) + min(numbers[low:high+1])


INPUT_S = '''\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 62),
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
