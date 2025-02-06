#!/usr/bin/env python3
import sys
from simplex import simplex
from parser import parse_lp

if len(sys.argv) != 2:
    print(f'Usage:\tpython {sys.argv[0]} path/to/lp/file')
    sys.exit(1)

with open(sys.argv[1], 'r') as infile:
    lp = infile.read()
    c, A, b = parse_lp(lp)
    print(f'{c=}')
    print('A=')
    for row in A:
        print(*row)
    print(f'{b=}')
    simplex(c, A, b)
