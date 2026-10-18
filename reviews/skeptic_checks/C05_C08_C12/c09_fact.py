"""Skeptic check for CLM-C09-02/06/08: exact factorisation statistics of Knuth's circle semigroup.

Products from the Zeckendorf definition (no shadow formula); factorisation sets WITHOUT truncation;
length sets by an exact sumset DP.  Also checks the length bound |nu'(n)| < |psi|^r of CLM-C09-06
for the maximal length r, in exact arithmetic.
Usage: python3 c09_fact.py [M]   (default M = 200000) -> out/c09_fact.json
"""
import json
import sys
import time
from math import isqrt
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"
M = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000

FIB = [0, 1]
while len(FIB) < 120:
    FIB.append(FIB[-1] + FIB[-2])


def zeck(n):
    """Zeckendorf index set (Mathlib indexing, indices >= 2)."""
    out = []
    k = len(FIB) - 1
    while n:
        while FIB[k] > n:
            k -= 1
        out.append(k)
        n -= FIB[k]
        k -= 2
    return out


def circ(a, b):
    za, zb = zeck(a), zeck(b)
    return sum(FIB[k + l] for k in za for l in zb)


def sign_X_minus_Y_sqrt5(X, Y):
    if Y == 0:
        return (X > 0) - (X < 0)
    if X >= 0 and Y < 0:
        return 1
    if X <= 0 and Y > 0:
        return -1
    d = X * X - 5 * Y * Y
    s = (d > 0) - (d < 0)
    return s if X > 0 else -s


def main():
    t0 = time.time()
    reps = {}
    for a in range(1, isqrt(M) + 1):
        for b in range(a, M // a + 1):     # a o b >= a b
            p = circ(a, b)
            if p <= M:
                reps.setdefault(p, []).append((a, b))
    fact = {}
    lens = {}
    for n in range(1, M + 1):
        if n not in reps:
            fact[n] = {(n,)}
            lens[n] = {1}
            continue
        fs, ls = set(), set()
        for a, b in reps[n]:
            for fa in fact[a]:
                for fb in fact[b]:
                    fs.add(tuple(sorted(fa + fb)))
            ls |= {x + y for x in lens[a] for y in lens[b]}
        fact[n] = fs
        lens[n] = ls
    multi = [n for n in range(1, M + 1) if len(fact[n]) > 1]
    difflen = [n for n in range(1, M + 1) if len(lens[n]) > 1]
    consistent = all({len(f) for f in fact[n]} == lens[n] for n in range(1, M + 1))
    el = max((max(lens[n]) / min(lens[n]), n) for n in range(1, M + 1))
    el_all = sorted({n for n in range(1, M + 1) if max(lens[n]) / min(lens[n]) == el[0]})
    maxfac = max(len(fact[n]) for n in range(1, M + 1))
    maxlen = max(max(lens[n]) for n in range(1, M + 1))
    # length bound: |nu'(n)| < |psi|^r for r = max length, exactly.  nu'(n) = (A - n sqrt5)/2, A = 2 n* + n.
    # |psi|^r = ((sqrt5 - 1)/2)^r = (P_r sqrt5 - Q_r)/2^r  with integers from expanding.
    viol = []
    for n in range(1, M + 1):
        r = max(lens[n])
        ns = sum(FIB[k - 1] for k in zeck(n))
        A = 2 * ns + n
        # ((sqrt5-1)/2)^r = (u + v sqrt5)/2^r ; compute (u, v) by repeated multiplication
        u, v = 1, 0
        for _ in range(r):
            u, v = (-u + 5 * v), (u - v)      # (u + v s)(-1 + s) = -u + 5v + (u - v) s
        # condition: |A - n s|/2 < (u + v s)/2^r  <=>  2^(r-1) |A - n s| < u + v s
        two = 2 ** (r - 1)
        # case split on sign of A - n s
        sg = sign_X_minus_Y_sqrt5(A, n)
        if sg >= 0:   # two*(A - n s) < u + v s  <=>  (two*A - u) - (two*n + v) s < 0
            ok = sign_X_minus_Y_sqrt5(two * A - u, two * n + v) < 0
        else:         # two*(n s - A) < u + v s  <=>  (-two*A - u) - (v - two*n) s < 0
            ok = sign_X_minus_Y_sqrt5(-two * A - u, v - two * n) < 0
        if not ok:
            viol.append([n, r])
    res = {
        "M": M,
        "n_with_at_least_two_factorisations": len(multi),
        "first_multi": multi[0], "first_multi_factorisations": sorted(map(list, fact[multi[0]])),
        "n_with_factorisations_of_different_lengths": len(difflen),
        "max_elasticity": el[0], "max_elasticity_attained_at": el_all[:10],
        "max_number_of_factorisations": maxfac,
        "max_factorisation_length": maxlen,
        "length_set_DP_consistent_with_factorisation_sets": consistent,
        "length_bound_violations": viol[:10],
        "seconds": round(time.time() - t0, 1),
    }
    (OUT / "c09_fact.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res))


if __name__ == "__main__":
    main()
