import argparse
import os.path
import re
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(s: str) -> list[tuple]:
    MEM_RE = re.compile(r'^mem\[(\d+)\] = (\d+)$')
    inputs: list[tuple] = []
    for line in s.splitlines():
        if line.startswith('mask'):
            _, _, mask_s = line.partition(' = ')
            inputs.append((mask_s,))
        else:
            match = MEM_RE.match(line)
            assert match
            target = int(match[1])
            number = int(match[2])
            inputs.append((target, number))
    return inputs


def add_leading_zeros(binary, total_len)->str:
    leading_zeros = ""
    if (total_len - len(binary)) > 0:
        leading_zeros = (total_len - len(binary))*'0'
    return leading_zeros+binary


def decimal_to_binary(dec: int, binary = "")->str:
    if dec > 0:
        binary = f"{dec%2}" + binary
        dec = dec // 2
        return decimal_to_binary(dec, binary)
    return add_leading_zeros(binary, 36)


def binary_to_decimal(binary: str, decimal = 0)->int:
    if len(binary) > 0:
        decimal = decimal * 2 + int(binary[0])
        return binary_to_decimal(binary[1:], decimal)
    return decimal


def apply_mask(binary: str, mask: str)->list[str]:
    binary_chars = list(binary)
    ones_idx = [pos for pos, char in enumerate(mask) if char == '1']
    X_idx = [pos for pos, char in enumerate(mask) if char == 'X']
    for idx in ones_idx:
        binary_chars[idx] = '1'
    for idx in X_idx:
        binary_chars[idx] = 'X'

    return binary_chars


def get_bits_combinations(length: int, combinations: list[list[int]], comb_so_far):
    if len(comb_so_far) == length:
        combinations.append(comb_so_far)
    else:
        for cand in [0,1]:
            get_bits_combinations(length, combinations, comb_so_far + [cand])


def apply_comb(mask: list[str], comb:  list[tuple[int, int]]) -> str:
    new_target = mask[:]
    for pos, val in comb:
        new_target[pos] = f"{val}"
    return "".join(new_target)


def compute(s: str) -> int:
    instructions = parse_input(s)
    memory: dict[int, int] = {}
    fluctuating_bits: list[list[tuple[int, int]]] = []
    current_mask = ""
    for inst in instructions:
        if len(inst) == 1:
            current_mask = inst[0]
            X_indices = [pos for pos, char in enumerate(current_mask) if char == 'X']
            results = []
            fluctuating_bits = []
            get_bits_combinations(len(X_indices), results, [])
            for perm in results:
                bit_comb: list[tuple[int, int]] = []
                assert len(perm) == len(X_indices)
                for i in range(len(perm)):
                    bit_comb.append((X_indices[i], perm[i]))
                fluctuating_bits.append(bit_comb)
        else:
            target, number = inst[0], inst[1]
            # apply mask on the target, to get a masked target containing X values
            masked_target = apply_mask(decimal_to_binary(target), current_mask)
            # each comb in address_combs should replace these X values with a valid bit
            for comb in fluctuating_bits:
                new_target = apply_comb(masked_target, comb)
                memory[binary_to_decimal(new_target)] = number
    sum_values = 0
    for addr, val in memory.items():
        sum_values += val

    return sum_values


INPUT_S = '''\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 208),
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
