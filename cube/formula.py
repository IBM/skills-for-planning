import copy

from cube.cube import Face

def _inverse_move(move):
    if '\'' in move:
        return move.strip('\'')
    else:
        return move+'\''

def _mirror_move(move, face=Face.R):
    table = {
        Face.R: {
            'L':   'R\'',
            'R':   'L\'',
            'U':   'U\'',
            'D':   'D\'',
            'F':   'F\'',
            'B':   'B\'',
            'L\'': 'R',
            'R\'': 'L',
            'U\'': 'U',
            'D\'': 'D',
            'F\'': 'F',
            'B\'': 'B',
        },
        Face.U: {
            'U':   'D\'',
            'D':   'U\'',
            'L':   'L\'',
            'R':   'R\'',
            'F':   'F\'',
            'B':   'B\'',
            'U\'': 'D',
            'D\'': 'U',
            'L\'': 'L',
            'R\'': 'R',
            'F\'': 'F',
            'B\'': 'B',
        },
        Face.F: {
            'F':   'B\'',
            'B':   'F\'',
            'L':   'L\'',
            'R':   'R\'',
            'U':   'U\'',
            'D':   'D\'',
            'F\'': 'B',
            'B\'': 'F',
            'L\'': 'L',
            'R\'': 'R',
            'U\'': 'U',
            'D\'': 'D',
        },
    }
    table[Face.L] = table[Face.R]
    table[Face.D] = table[Face.U]
    table[Face.B] = table[Face.F]
    return table[face][move]

def _rotate_move(move, axis, n=1):
    if n==0:
        return move
    table = {
        Face.U: {
            'U':   'U',
            'D':   'D',
            'U\'': 'U\'',
            'D\'': 'D\'',
            'F':   'L',
            'L':   'B',
            'B':   'R',
            'R':   'F',
            'F\'': 'L\'',
            'L\'': 'B\'',
            'B\'': 'R\'',
            'R\'': 'F\'',
        },
        Face.D: {
            'U':   'U',
            'D':   'D',
            'U\'': 'U\'',
            'D\'': 'D\'',
            'L':   'F',
            'F':   'R',
            'R':   'B',
            'B':   'L',
            'L\'': 'F\'',
            'F\'': 'R\'',
            'R\'': 'B\'',
            'B\'': 'L\'',
        },
        Face.R: {
            'R':     'R',
            'L':     'L',
            'R\'':   'R\'',
            'L\'':   'L\'',
            'U':     'B',
            'B':     'D',
            'D':     'F',
            'F':     'U',
            'U\'':   'B\'',
            'B\'':   'D\'',
            'D\'':   'F\'',
            'F\'':   'U\'',
        },
        Face.L: {
            'R':     'R',
            'L':     'L',
            'R\'':   'R\'',
            'L\'':   'L\'',
            'U':     'F',
            'F':     'D',
            'D':     'B',
            'B':     'U',
            'U\'':   'F\'',
            'F\'':   'D\'',
            'D\'':   'B\'',
            'B\'':   'U\'',
        },
        Face.F: {
            'F':     'F',
            'B':     'B',
            'F\'':   'F\'',
            'B\'':   'B\'',
            'R':     'D',
            'D':     'L',
            'L':     'U',
            'U':     'R',
            'R\'':   'D\'',
            'D\'':   'L\'',
            'L\'':   'U\'',
            'U\'':   'R\'',
        },
        Face.B: {
            'F':     'F',
            'B':     'B',
            'F\'':   'F\'',
            'B\'':   'B\'',
            'R':     'U',
            'U':     'L',
            'L':     'D',
            'D':     'R',
            'R\'':   'U\'',
            'U\'':   'L\'',
            'L\'':   'D\'',
            'D\'':   'R\'',
        }
    }
    for i in range(n):
        move = table[axis][move]
    return move

def inverse(formula):
    result = copy.copy(formula)
    result.reverse()
    for i, move in enumerate(result):
        result[i] = _inverse_move(move)
    return result


def mirror(formula, face=Face.R):
    """Flip a formula left/right to use opposite face(s)."""
    result = copy.copy(formula)
    for i, move in enumerate(result):
        result[i] = _mirror_move(move, face)
    return result

def rotate(formula, axis, n=1):
    """Rotate a formula clockwise around the specified cube face."""
    result = copy.copy(formula)
    for i, move in enumerate(result):
        result[i] = _rotate_move(move, axis, n)
    return result

def simplify(formula):
    s = ''.join(formula).strip()
    for move in 'FBLRUD':
        s = s.replace(move+'\'', move.lower())

    noops = ["Ff","Bb","Ll","Rr","Uu","Dd"]
    noops += [op[::-1] for op in noops]
    triples = [op*3 for op in 'FBLRUDfblrud']
    singles = [op for op in 'fblrudFBLRUD']
    outers = ["Ff","Bb","Ll","Rr","Uu","Dd",'fF', 'bB', 'lL', 'rR', 'uU', 'dD']
    inners = ['B','F','R','L','D','U']*2
    while True:
        s_prev = s
        # Noops: [F F'] -> []
        for noop in noops:
            s = s.replace(noop, '')
        # Triples: [F F F] -> [F']
        for op3, op1 in zip(triples, singles):
            s = s.replace(op3, op1)
        # Sandwiches: [F B F'] -> [B]; [L R R L'] -> [R R]
        for outer, inner in zip(outers, inners):
            sandwich1 = outer[0]+inner+outer[1]
            s = s.replace(sandwich1, inner)
            sandwich2 = outer[0]+inner.lower()+outer[1]
            s = s.replace(sandwich2, inner.lower())
            sandwich1 = outer[0]+inner*2+outer[1]
            s = s.replace(sandwich1, inner*2)
            sandwich2 = outer[0]+inner.lower()*2+outer[1]
            s = s.replace(sandwich2, inner.lower()*2)
        if s == s_prev:
            break
    simplified = [move if move in 'FBLRUD' else (move.upper()+'\'') for move in s]
    return simplified

def variations(formula):
    # Consider each possible orientation of the cube
    variations = []
    f0 = formula
    l0 = rotate(formula, Face.U, 1)
    b0 = rotate(formula, Face.U, 2)
    r0 = rotate(formula, Face.D, 1)
    u0 = rotate(formula, Face.L, 1)
    d0 = rotate(formula, Face.R, 1)
    formulas = [f0, l0, b0, r0, u0, d0]
    faces = [Face.F, Face.L, Face.B, Face.R, Face.D, Face.U]
    for n in range(4):
        for f, face in zip(formulas, faces):
            f = rotate(f, face, n)
            variations.append(f)

    variations += [mirror(x) for x in variations]# Add mirrored algs
    variations += [inverse(x) for x in variations]# Add inverse algs

    # Remove duplicate formulas
    variations = [' '.join(x) for x in variations]
    variations = list(set(variations))
    variations = [x.split() for x in variations]
    return variations
