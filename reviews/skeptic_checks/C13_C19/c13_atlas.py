"""Skeptic check C13-A: re-derive the affine atlas (EXP-C13-01) and test Theorem 1 (CLM-C13-01) and the
identifications of CLM-C13-11 with independent code (own enumeration, own affine evaluation, direct root
search for every N <= 200 instead of the CRT shortcut).  Uses sympy only as a polynomial-arithmetic library.

Output: out/c13_atlas.json and a printed summary."""
import json
import sys
import time
from collections import defaultdict
from math import gcd

import numpy as np
import sympy as sp

sys.path.insert(0, __import__("os").path.dirname(__file__))
from c13_lib import affine_system_of, laws_up_to_iso, peval, read_law, roots_mod  # noqa: E402

A = sp.Symbol("a")
NMAX = 200
Ns = np.arange(1, NMAX + 1, dtype=np.int64)


def direct_spectrum(system):
    """Sorted list of N <= NMAX having a common root (direct search over all a in [0, N))."""
    if not system:
        return list(range(1, NMAX + 1))
    ok = np.ones((NMAX, NMAX), dtype=bool)          # ok[N-1, a]
    for p in system:
        V = np.array([peval(p, a) for a in range(NMAX)], dtype=np.int64)
        ok &= (V[None, :] % Ns[:, None]) == 0
    mask = np.arange(NMAX)[None, :] < Ns[:, None]
    return [int(N) for N in Ns[(ok & mask).any(axis=1)]]


def topoly(p):
    return sp.Poly(list(reversed(p)), A, domain="ZZ")


def classify(system):
    polys = [topoly(p) for p in system]
    g = polys[0]
    for q in polys[1:]:
        g = sp.gcd(g, q)
    if g.degree() >= 1:
        return "infinite", g.primitive()[1]
    # an integer in the ideal: constants, resultants of pairs, resultants with integer combinations
    R = 0
    for q in polys:
        if q.degree() == 0:
            R = gcd(R, abs(int(q.as_expr())))
    nonconst = [q for q in polys if q.degree() >= 1]
    for i in range(len(nonconst)):
        for j in range(i + 1, len(nonconst)):
            r = int(sp.resultant(nonconst[i].as_expr(), nonconst[j].as_expr(), A))
            R = gcd(R, abs(r))
    tries = 0
    while R == 0 and tries < 20:
        tries += 1
        comb = sum(((k + 2 + tries) ** 2 + k) * q.as_expr() for k, q in enumerate(nonconst[1:]))
        r = int(sp.resultant(nonconst[0].as_expr(), sp.expand(comb), A))
        R = abs(r)
    return "finite", R


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def main():
    t0 = time.time()
    out = {}
    fams = {"3var_le4": (("x", "y", "z"), 4), "2var_le5": (("x", "y"), 5)}
    all_L = set()
    infinite_gcds = {}
    thm1_fail = []
    for fam, (vs, ml) in fams.items():
        laws = laws_up_to_iso(vs, ml)
        systems = defaultdict(list)
        for k, (s, t) in laws.items():
            systems[affine_system_of(s, t)].append(k)
        spectra = defaultdict(list)
        n_fin = n_inf = 0
        Ls = set()
        fin_examples = {}
        for sysm, ks in systems.items():
            spec = direct_spectrum(sysm)
            spectra[tuple(spec)].append(sysm)
            S = set(spec)
            # Theorem 1 (c): divisor-closed and coprime-product-closed (inside [1, NMAX])
            for N in spec:
                if any(d not in S for d in divisors(N)):
                    thm1_fail.append((fam, sorted(map(list, sysm)), "divisor", N))
            for N in spec:
                for M in spec:
                    if N * M <= NMAX and gcd(N, M) == 1 and N * M not in S:
                        thm1_fail.append((fam, sorted(map(list, sysm)), "crt", N, M))
            if not sysm:
                kind = "all"
            else:
                kind, data = classify(sysm)
            if kind == "finite":
                n_fin += 1
                R = data
                assert R != 0
                # L = product over p | R of the largest p^e (e <= v_p(R)) with a common root mod p^e
                L = 1
                for p, e in sp.factorint(R).items():
                    best = 0
                    for k in range(1, e + 1):
                        if roots_mod(sysm, p ** k):
                            best = k
                        else:
                            break
                    L *= p ** best
                # direct verification: spectrum within [1, NMAX] equals Div(L) there, every divisor of L
                # (also > NMAX) has a root, and no N in [1, NMAX] outside Div(L) has one
                divL = [d for d in divisors(L)]
                if [d for d in divL if d <= NMAX] != spec:
                    thm1_fail.append((fam, sorted(map(list, sysm)), "finite_not_divL", L, spec[:20]))
                if any(not roots_mod(sysm, d) for d in divL):
                    thm1_fail.append((fam, sorted(map(list, sysm)), "divisor_of_L_without_root", L))
                if R % L:
                    thm1_fail.append((fam, sorted(map(list, sysm)), "L_not_dividing_R", L, R))
                Ls.add(L)
                fin_examples.setdefault(L, ks[0])
            elif kind == "infinite":
                n_inf += 1
                G = data
                infinite_gcds.setdefault(str(G.as_expr()), set()).add(fam)
                # Schur: roots modulo some primes in (NMAX, 3000]
                cnt = 0
                for p in sp.primerange(NMAX + 1, 3000):
                    if roots_mod(sysm, p):
                        cnt += 1
                        if cnt >= 3:
                            break
                if cnt < 3:
                    thm1_fail.append((fam, sorted(map(list, sysm)), "infinite_but_few_primes", str(G.as_expr())))
        all_L |= Ls
        out[fam] = {"n_laws": len(laws), "n_systems": len(systems), "n_spectra": len(spectra),
                    "n_finite_systems": n_fin, "n_infinite_systems": n_inf,
                    "L_values": sorted(Ls)}
        print(fam, "laws", len(laws), "systems", len(systems), "distinct spectra (N<=200)", len(spectra),
              "finite systems", n_fin, "infinite systems", n_inf, "distinct L", len(Ls), "max L", max(Ls))
    out["all_L"] = sorted(all_L)
    out["n_distinct_L_total"] = len(all_L)
    out["theorem1_failures"] = thm1_fail[:50]
    out["n_theorem1_failures"] = len(thm1_fail)
    out["infinite_gcds"] = {k: sorted(v) for k, v in infinite_gcds.items()}
    print("distinct L over both families:", len(all_L), "max", max(all_L))
    print("Theorem 1 failures:", len(thm1_fail), thm1_fail[:5])
    out["elapsed_s"] = round(time.time() - t0, 1)
    json.dump(out, open(__import__("os").path.join(__import__("os").path.dirname(__file__), "out", "c13_atlas.json"),
                        "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
