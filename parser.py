import re
import sys

def tokenise(line):
    r = r'[a-zA-Z]+|[+-]?\s*[0-9]+|\s+|[+-]|[<>]?='
    return [re.sub(r'\s+', '', token) for token in re.findall(r, line) if token.strip()]

def get_names_coeff(tokens):
    vars = []
    coef = []
    if not re.fullmatch(r'[+-]?[0-9]+', tokens[0]):
        tokens.insert(0, '1')
    for i in range(1, len(tokens)):
        if re.fullmatch(r'[a-zA-Z]+', tokens[i]):
            vars.append(tokens[i])
            if re.fullmatch(r'[+-]?[0-9]+', tokens[i-1]):
                coef.append(int(tokens[i-1]))
            elif tokens[i-1] == '-':
                coef.append(-1)
            else:
                coef.append(1)

    return vars, coef

def parse_lp(lp):
    """Parses input LP string into c, A, b form"""
    lines = [line for line in reversed(lp.split('\n')) if line.strip()]
    obj_t = tokenise(lines.pop())
    # either MAximise or MInimise
    obj_sign = None
    if obj_t[0].lower().startswith('ma'):
        obj_sign = 1
    elif obj_t[0].lower().startswith('mi'):
        obj_sign = -1
    else:
        sys.exit(f'Unrecognisable function objective "{obj_t[0]}"')

    variables, coef = get_names_coeff(obj_t[1:])
    c = [n * obj_sign for n in coef]
    A = []
    b = []

    # subject to, s.t, Subject To, S.t ...
    if re.fullmatch(r'[sS]\w*\b[\s.][tT].*', lines[-1]):
        lines.pop()

    for tokens in map(tokenise, lines):
        A.append([0]*len(variables))
        sign = 1
        equality = False
        match tokens[-2]:
            case '<=':
                pass
            case '>=':
                sign = -1
            case '=':
                equality = True
            case _:
                sys.exit(f'Unrecognisable constraint (in)equality "{tokens[-2]}"')
        for va, co in zip(*get_names_coeff(tokens)):
            A[-1][variables.index(va)] = co * sign
        b.append(int(tokens[-1]) * sign)
        if equality:
            A.append([-n * sign for n in A[-1]])
            b.append(-b[-1] * sign)

    return c, A, b
