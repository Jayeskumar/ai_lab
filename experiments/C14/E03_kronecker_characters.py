"""EXP-C14-03: which local products are linearised by the Kronecker product (characters)?"""

import random

import numpy as np
import sympy as sp

from systems.graph_products import (CELLS, E, A, N, character_matrix, is_associative, is_commutative,
                                    kronecker_characters, name_of, product, seidel, show)

META = {
    "id": "EXP-C14-03",
    "cycle": "C14",
    "title": "Multiplicative and additive Kronecker characters of local graph products",
    "agent": "Formal Verifier",
    "question": "For which local products is there a matrix functor M_c(G) = c_E I + c_A A + c_N (J - I - A) "
                "(c_A != c_N) with M_c(G*H) = M_c(G) (x) M_c(H) (multiplicative character) or "
                "M_c(G*H) = M_c(G) (x) I + I (x) M_c(H) (additive character) for all graphs?",
    "hypothesis": "H-C14-5 (derived by hand, Theorem 4/5 of proofs/paper/C14.md): exactly six products have a "
                  "multiplicative character - direct (c=(0,1,0)), strong (1,1,0), co-normal (1,0,1), symmetric "
                  "difference (1,-1,1), EA AE AA NN (1,1,-1) and the complement-dual of the direct product (0,0,1); "
                  "exactly two have an additive character - Cartesian (0,1,0) and its complement-dual (0,0,1). "
                  "H-C14-6 (bold): every commutative associative local product except the empty and complete "
                  "products has a character of one of the two kinds.",
    "assumptions": ["characters solved exactly over C with sympy (independent of the hand case analysis)",
                    "numerical confirmation on 30 seeded random pairs of graphs with 1-5 vertices per product"],
    "methodology": "Cell decomposition: A(G*H) = sum over cells in S of R_r1(G) (x) R_r2(H), R_E = I, R_A = A, "
                   "R_N = J - I - A, with disjoint supports, all realised by P3 x P3; the functional equations reduce "
                   "to polynomial equations in (c_E, c_A, c_N), solved by sympy for each of the 256 codes.",
    "falsification": "A product outside the predicted lists with a solution, a predicted product without one, or a "
                     "numerical failure of M_c(G*H) = M_c(G) (x) M_c(H).",
    "seed": 1414,
}


def solve_characters(code, additive=False):
    cE, cA, cN = sp.symbols("cE cA cN")
    c = {E: cE, A: cA, N: cN}
    S = set((a, b) for i, (a, b) in enumerate(CELLS) if code >> i & 1)
    eqs = []
    if additive:
        eqs.append(sp.Eq(2 * cE, cE))
        for r, s in CELLS:
            lhs = (c[r] if s == E else 0) + (c[s] if r == E else 0)
            eqs.append(sp.Eq(lhs, cA if (r, s) in S else cN))
    else:
        eqs.append(sp.Eq(cE * cE, cE))
        for r, s in CELLS:
            eqs.append(sp.Eq(c[r] * c[s], cA if (r, s) in S else cN))
    sols = sp.solve(eqs, [cE, cA, cN], dict=True)
    out = []
    for so in sols:
        vals = tuple(sp.nsimplify(so.get(x, x)) for x in (cE, cA, cN))
        if any(v.free_symbols for v in vals):  # a one-parameter family: normalise the free symbol to 1
            free = set().union(*(v.free_symbols for v in vals))
            norm = tuple(sp.nsimplify(v.subs({f: 1 for f in free})) for v in vals)
            if norm[1] != norm[2]:
                out.append(tuple(int(v) for v in norm) + ("scalable",))
        elif vals[1] != vals[2]:
            out.append(tuple(int(v) if v.is_integer else str(v) for v in vals))
    return out


def rand_graph(rng, n):
    G = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.5:
                G[i, j] = G[j, i] = 1
    return G


def run():
    rng = random.Random(META["seed"])
    pairs = [(rand_graph(rng, rng.randint(1, 5)), rand_graph(rng, rng.randint(1, 5))) for _ in range(30)]
    mult, add, mismatch_enum = {}, {}, []
    numeric_fail = []
    for code in range(256):
        m = solve_characters(code)
        a = solve_characters(code, additive=True)
        if m:
            mult[code] = m
        if a:
            add[code] = a
        if sorted(tuple(x) for x in m) != sorted(kronecker_characters(code)):
            mismatch_enum.append(code)
        for c in m:
            if any(isinstance(x, str) for x in c):
                continue
            for G, H in pairs:
                lhs = character_matrix(product(code, G, H), c)
                rhs = np.kron(character_matrix(G, c), character_matrix(H, c))
                if not np.allclose(lhs, rhs):
                    numeric_fail.append((code, "mult"))
                    break
        for c in a:
            c = c[:3]
            for G, H in pairs:
                lhs = character_matrix(product(code, G, H), c)
                MG, MH = character_matrix(G, c), character_matrix(H, c)
                rhs = np.kron(MG, np.eye(H.shape[0])) + np.kron(np.eye(G.shape[0]), MH)
                if not np.allclose(lhs, rhs):
                    numeric_fail.append((code, "add"))
                    break
    comm_assoc = [c for c in range(256) if is_associative(c) and is_commutative(c)]
    uncovered = [c for c in comm_assoc if c not in mult and c not in add]
    char_not_assoc = [c for c in set(mult) | set(add) if not (is_associative(c) and is_commutative(c))]
    # spectral corollary for the symmetric difference: eigenvalues of S + I multiply
    xor = 85
    spec_fail = 0
    for G, H in pairs:
        ev = np.sort(np.linalg.eigvalsh(seidel(product(xor, G, H)).astype(float)) + 1)
        eg = np.linalg.eigvalsh(seidel(G).astype(float)) + 1
        eh = np.linalg.eigvalsh(seidel(H).astype(float)) + 1
        pred = np.sort(np.outer(eg, eh).ravel())
        spec_fail += not np.allclose(ev, pred, atol=1e-8)
    label = lambda c: name_of(c) or show(c)
    return {
        "multiplicative": {label(c): v for c, v in mult.items()},
        "additive": {label(c): v for c, v in add.items()},
        "sympy_vs_enumeration_mismatches": mismatch_enum,
        "numeric_failures": numeric_fail,
        "commutative_associative": [label(c) for c in comm_assoc],
        "commutative_associative_without_character": [label(c) for c in uncovered],
        "products_with_character_not_comm_assoc": char_not_assoc,
        "xor_seidel_spectrum_failures": spec_fail,
        "summary": [f"multiplicative characters: {{{', '.join(f'{label(c)}: {v}' for c, v in mult.items())}}}",
                    f"additive characters: {{{', '.join(f'{label(c)}: {v}' for c, v in add.items())}}}",
                    f"commutative associative products without a character: {[label(c) for c in uncovered]}",
                    f"sympy/enumeration mismatches {len(mismatch_enum)}, numeric failures {len(numeric_fail)}, "
                    f"XOR Seidel-spectrum failures {spec_fail}/30"],
    }
