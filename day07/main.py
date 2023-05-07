import argparse
import os.path
from functools import reduce
from typing import NamedTuple
import collections
import pytest
import re
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PATTERN = re.compile('^([^ ]+ [^ ]+) bags contain (.*)$')
BAG_RE = re.compile(r'(\d+) ([^ ]+ [^ ]+)')


class BagInfo(NamedTuple):
    col: str
    num: int


def parse_input(s: str):
    childs = collections.defaultdict(list)
    colors = set()
    for line in s.splitlines():
        match = PATTERN.match(line)
        assert match
        k = match[1]
        colors.add(k)
        targets = [(int(n), tp) for n, tp in BAG_RE.findall(match[2])]
        for num, color in targets:
            childs[k].append(BagInfo(col=color, num=num))
    return childs, list(colors)


def dfs(graph: collections.defaultdict[str, list[BagInfo]],
        node: str) -> int:
    return reduce(lambda acc, child: acc + child.num + child.num * dfs(graph, child.col),
                  graph[node], 0)


def compute(s: str) -> int:
    parents, colors = parse_input(s)
    visited = {}
    for col in colors:
        visited[col] = False
    start = 'shiny gold'
    n_outermost_parents = dfs(parents, start)
    return n_outermost_parents


INPUT_S = '''\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 32),
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
