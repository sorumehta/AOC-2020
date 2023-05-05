import argparse
import os.path
import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(s: str):
    passports: list[dict[str, str]] = []
    for data in s.split('\n\n'):
        passport = {}
        keyVals = data.split()
        for key_val in keyVals:
            key, _, val = key_val.partition(':')
            passport[key] = val
        passports.append(passport)
    return passports


def compute(s: str) -> int:
    passports = parse_input(s)
    valid_set = {'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'}
    n_valid = 0
    for passPort in passports:
        test_set = set(passPort.keys())
        if not valid_set.issubset(test_set):
            continue
    return n_valid


INPUT_S = '''\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 2),
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
