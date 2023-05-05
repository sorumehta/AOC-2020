import argparse
import os.path
import re

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


def check_val(key: str, val: str) -> bool:
    if val is None:
        return False
    isValid = False
    if key == 'ecl':
        isValid = val in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    elif key == 'pid':
        isValid = val.isdigit() and len(val) == 9
    elif key == 'eyr':
        isValid = val.isdigit() and len(val) == 4 and (2020 <= int(val) <= 2030)
    elif key == 'hcl':
        isValid = re.match('^#[0-9a-f]{6}$', val)
    elif key == 'byr':
        isValid = val.isdigit() and len(val) == 4 and (1920 <= int(val) <= 2002)
    elif key == 'iyr':
        isValid = val.isdigit() and len(val) == 4 and (2010 <= int(val) <= 2020)
    elif key == 'hgt':
        if val.endswith('cm'):
            val = int(val.rstrip('cm'))
            isValid = 150 <= val <= 193
        elif val.endswith('in'):
            val = int(val.rstrip('in'))
            isValid = 59 <= val <= 76
    return isValid


def compute(s: str) -> int:
    passports = parse_input(s)
    valid_attrs = ['ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt']
    n_valid = 0
    for passPort in passports:
        isValid = True
        for valid_key in valid_attrs:
            val_to_check = passPort.get(valid_key)
            if not check_val(valid_key, val_to_check):
                isValid = False
        if isValid:
            n_valid += 1
    return n_valid


INPUT_S = '''\
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f
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
