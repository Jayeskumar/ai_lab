"""Numerical sanity check of the skeptic's proof of CLM-C02-04 (sum b = m never terminates from all
unary starts).

Proof sketch being checked.  Reduce to an aperiodic rule (g = gcd supp b = 1).  Let A be the J x J
nonnegative matrix of the linearised window map, (A x)_i = x_{i+1} + (b_i/m) x_1 (x_{J+1} = 0).
Its graph has edges i+1 -> i and 1 -> i (b_i > 0); every cycle passes through 1 and the cycle
lengths are {i : b_i > 0}, so A is irreducible with period g = 1, i.e. primitive: A^N > 0 for some N.
Since floor(x_1/m) >= x_1/m - 1, F(x) >= A x - b componentwise, and as A >= 0 is monotone,
F^N(x) >= A^N x - C with C = sum_{j<N} A^j b.  Hence for t >= t* = max_i (T_i + C_i)/(A^N b)_i the
window F^N(t b) dominates T, and by Lemma 4 the derivation from any n in [t m, (t+1) m) is infinite.

This script: for every aperiodic rule with m <= 6, J <= 6 computes N, C, t* exactly (Fractions),
then simulates the true integer window map from t*b, (t*+1)b, ..., (t*+5)b and checks that
F^N(t b) >= T and F^N(t b) >= t A^N b - C.
"""
import itertools
import json
import os
from fractions import Fraction
from math import ceil, gcd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def matmul(A, B):
    n, k, p = len(A), len(B), len(B[0])
    return [[sum(A[i][l] * B[l][j] for l in range(k)) for j in range(p)] for i in range(n)]


def F(x, m, b):
    s = x[0] // m
    J = len(b)
    return [(x[i + 1] if i + 1 < J else 0) + s * b[i] for i in range(J)]


def check(m, b):
    J = len(b)
    T = [sum(b[i:]) for i in range(J)]
    A = [[Fraction(0)] * J for _ in range(J)]
    for i in range(J):
        A[i][0] += Fraction(b[i], m)
        if i + 1 < J:
            A[i][i + 1] += 1
    P = [[Fraction(int(i == j)) for j in range(J)] for i in range(J)]
    bv = [[Fraction(x)] for x in b]
    C = [[Fraction(0)] for _ in range(J)]
    N = 0
    while True:
        if all(P[i][j] > 0 for i in range(J) for j in range(J)):
            break
        C = [[C[i][0] + matmul(P, bv)[i][0]] for i in range(J)]
        P = matmul(A, P)
        N += 1
        if N > 10 * J * J:
            return {"m": m, "b": b, "error": "A not primitive"}
    ANb = [r[0] for r in matmul(P, bv)]
    tstar = max(ceil((T[i] + C[i][0]) / ANb[i]) for i in range(J))
    tstar = max(tstar, 1)
    ok = True
    for t in range(tstar, tstar + 6):
        x = [t * v for v in b]
        for _ in range(N):
            x = F(x, m, b)
        lower = [t * ANb[i] - C[i][0] for i in range(J)]
        if not (all(x[i] >= T[i] for i in range(J)) and all(x[i] >= lower[i] for i in range(J))):
            ok = False
    return {"m": m, "b": list(b), "N": N, "t_star": tstar, "ok": ok}


def main():
    rows = []
    for m in range(1, 7):
        for J in range(1, 7):
            for b in itertools.product(range(m + 1), repeat=J):
                if b[-1] == 0 or sum(b) != m:
                    continue
                g = 0
                for j, bj in enumerate(b, start=1):
                    if bj:
                        g = gcd(g, j)
                if g != 1:
                    continue
                rows.append(check(m, b))
    bad = [r for r in rows if not r.get("ok")]
    worst = max(rows, key=lambda r: r.get("t_star", 0))
    json.dump({"rules": len(rows), "failures": bad, "max_t_star": worst}, open(os.path.join(OUT, "c02_glider_proof_check.json"), "w"), indent=1)
    print(f"aperiodic sum b = m rules (m<=6, J<=6): {len(rows)}; proof-bound t* verified by simulation: "
          f"{len(rows) - len(bad)} ok, {len(bad)} failures; largest t* = {worst['t_star']} at m={worst['m']} "
          f"b={worst['b']} (N={worst['N']})")


if __name__ == "__main__":
    main()
