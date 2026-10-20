"""Historian check (2026-10-20): re-verify, cheaply, the model claims quoted from external sources in
reviews/historian_spectra_2026.md.  Nothing here is new mathematics; it only checks that the tables and linear
models that the sources state really satisfy the laws, so that the report does not repeat a mis-transcription.

Usage:  python3 -I reviews/historian_checks/spectra/check_sources.py [EQ677_DB_DIR]

EQ677_DB_DIR (optional) holds files db_<n>_<k>.txt copied from
https://raw.githubusercontent.com/memoryleak47/eq677/main/db/<n>/<k> (whitespace-separated Cayley tables,
row = left operand).  They are read as numbers only (untrusted data).  CPU: well under a second per check.
"""

import os
import re
import sys

# ---------------------------------------------------------------- laws  x = t(x, y),  m(a, b) = a * b
LAWS = {
    467: lambda m, x, y: m(y, m(x, m(x, m(y, y)))),
    501: lambda m, x, y: m(y, m(y, m(x, m(x, y)))),
    670: lambda m, x, y: m(y, m(x, m(m(x, y), y))),
    677: lambda m, x, y: m(y, m(x, m(m(y, x), y))),
    704: lambda m, x, y: m(y, m(y, m(m(x, x), y))),
    883: lambda m, x, y: m(y, m(m(x, y), m(y, y))),
    907: lambda m, x, y: m(y, m(m(y, x), m(x, y))),
    1076: lambda m, x, y: m(y, m(m(x, m(x, y)), y)),
    1083: lambda m, x, y: m(y, m(m(x, m(y, x)), y)),
    1110: lambda m, x, y: m(y, m(m(y, m(x, x)), y)),
    1279: lambda m, x, y: m(y, m(m(m(x, x), y), y)),
    1286: lambda m, x, y: m(y, m(m(m(x, y), x), y)),
    1313: lambda m, x, y: m(y, m(m(m(y, x), x), y)),
    1516: lambda m, x, y: m(m(y, y), m(x, m(x, y))),
    1719: lambda m, x, y: m(m(y, y), m(m(x, x), y)),
}
LAW255 = lambda m, x: m(m(m(x, x), x), x)  # x = ((xx)x)x


def holds(table, law):
    n = len(table)
    m = lambda a, b: table[a][b]
    return all(law(m, x, y) == x for x in range(n) for y in range(n))


def transpose(t):
    return [list(r) for r in zip(*t)]


def is_latin(t):
    n = len(t)
    rows = all(sorted(r) == list(range(n)) for r in t)
    cols = all(sorted(c) == list(range(n)) for c in zip(*t))
    return rows, cols


# ---------------------------------------------------------------- linear models  a*x + b*y  over Z/p
def linear_ok(law, p, a, b):
    """Symbolic check: every term is c_x*x + c_y*y (mod p); the law holds iff t = 1*x + 0*y."""
    m = lambda u, v: ((a * u[0] + b * v[0]) % p, (a * u[1] + b * v[1]) % p)
    return law(m, (1, 0), (0, 1)) == (1, 0)


def primes(lo, hi):
    return [q for q in range(lo, hi + 1) if q > 1 and all(q % d for d in range(2, int(q ** 0.5) + 1))]


def main():
    out = []
    # 1. linear models stated in the sources
    claims = [
        (677, 11, [(10, 2), (6, 6), (5, 7), (4, 8)], "I. Tencer, Zulip 'FINITE: 677 -> 255', 2024-12-05, msg 486395178"),
        (677, 13, [(9, 11)], "same message"),
        (677, 5, [(2, 4)], "T. Tao, same topic, 2024-12-05 (x*y = 2x - y on Z/5)"),
        (1286, 11, [(1, 7)], "ETP paper arXiv:2512.07087v2 Example 5.2; commentary/Equation1286.md"),
        (1286, 7, [(6, 2)], "commentary/Equation1286.md ('known to give the smallest model')"),
        (1516, 11, [(7, 5)], "A. Livne Bar-on, Zulip '1516 -> 255', 2024-11-05, msg 480658028"),
        (1516, 7, [(4, 1), (4, 5), (6, 2)], "A. Livne Bar-on, Zulip '1516 -> 255', 2024-11-04, msg 480530878"),
    ]
    for law, p, pairs, src in claims:
        res = [(a, b, linear_ok(LAWS[law], p, a, b)) for a, b in pairs]
        out.append(f"[linear] law {law} over Z/{p}: " + ", ".join(f"({a},{b})={'OK' if ok else 'FAIL'}" for a, b, ok in res)
                   + f"   <- {src}")

    # 2. idempotent linear models x*y = (1-b)x + b*y (Gunby-Mann 'ILP' roots) for the stated primes
    gm = [(670, 11, 6), (670, 29, 3), (1076, 47, 3), (1313, 5, 4), (1313, 19, 4), (467, 11, 5), (1516, 11, 5)]
    for law, p, b in gm:
        ok = linear_ok(LAWS[law], p, (1 - b) % p, b)
        out.append(f"[idempotent linear] law {law}, p={p}, b={b}: {'OK' if ok else 'FAIL'}"
                   "   <- B. Gunby-Mann, 'Spectra from clique decompositions of K_n' (Zulip, 2025-07-14)")

    # 3. for every law: primes p <= 50 with an idempotent linear model, and with any linear model
    for law in sorted(LAWS):
        idem = [p for p in primes(2, 50) if any(linear_ok(LAWS[law], p, (1 - b) % p, b) for b in range(p))]
        anyl = [p for p in primes(2, 50) if any(linear_ok(LAWS[law], p, a, b) for a in range(p) for b in range(p))]
        out.append(f"[scan p<=50] law {law}: idempotent linear at p in {idem}; some linear at p in {anyl}")

    # 4. small tables transcribed from Zulip messages (row = left operand)
    t677_9 = [[0, 2, 3, 5, 1, 7, 4, 8, 6], [1, 3, 4, 6, 7, 0, 2, 5, 8], [2, 8, 5, 1, 3, 4, 6, 0, 7],
              [3, 5, 6, 7, 4, 2, 8, 1, 0], [4, 6, 8, 0, 2, 3, 5, 7, 1], [5, 1, 7, 4, 6, 8, 0, 3, 2],
              [6, 7, 0, 2, 8, 5, 1, 4, 3], [7, 4, 2, 8, 0, 1, 3, 6, 5], [8, 0, 1, 3, 5, 6, 7, 2, 4]]
    raw1516_9 = """e e 7 0 1 2 3 4 5 6
0 0 1 4 2 7 6 e 3 5
1 1 6 2 5 3 0 7 e 4
2 2 5 7 3 6 4 1 0 e
3 3 e 6 0 4 7 5 2 1
4 4 2 e 7 1 5 0 6 3
5 5 4 3 e 0 2 6 1 7
6 6 0 5 4 e 1 3 7 2
7 7 3 1 6 5 e 2 4 0"""
    lab = {"e": 0, **{str(k): k + 1 for k in range(8)}}
    t1516_9 = [[lab[s] for s in line.split()[1:]] for line in raw1516_9.split("\n")]
    t1516_8 = [[0, 2, 3, 4, 5, 6, 7, 1], [4, 1, 6, 0, 7, 3, 5, 2], [5, 3, 2, 7, 0, 1, 4, 6], [6, 7, 4, 3, 1, 0, 2, 5],
               [7, 6, 1, 5, 4, 2, 0, 3], [1, 4, 7, 2, 6, 5, 3, 0], [2, 0, 5, 1, 3, 7, 6, 4], [3, 5, 0, 6, 2, 4, 1, 7]]
    # Andy Jiang (2024-11-04, msg 480474436): (a,b,c)*(d,e,f) = (a+b+e, d+e+f+a+c, e+f+b) mod 2
    vec = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    idx = {v: i for i, v in enumerate(vec)}

    def aj(u, v):
        a, b, c = u
        d, e, f = v
        return idx[((a + b + e) % 2, (d + e + f + a + c) % 2, (e + f + b) % 2)]

    t1516_8aj = [[aj(u, v) for v in vec] for u in vec]
    tables = [(677, t677_9, "J. Brox, Zulip 'FINITE: 677 -> 255', 2024-12-09, msg 486936665"),
              (1516, t1516_9, "A. Livne Bar-on, Zulip '1516 -> 255', 2024-11-05, msg 480658028 (order 9)"),
              (1516, t1516_8, "same message (order 8)"),
              (1516, t1516_8aj, "A. Jiang, Zulip '1516 -> 255', 2024-11-04, msg 480474436 (F_2^3 formula)")]
    for law, t, src in tables:
        out.append(f"[table] law {law}, order {len(t)}: rows-as-left {holds(t, LAWS[law])}, "
                   f"transposed {holds(transpose(t), LAWS[law])}, latin(rows, cols) {is_latin(t)}   <- {src}")

    # 5. the eq677 database files, if a directory is given
    if len(sys.argv) > 1:
        d = sys.argv[1]
        for f in sorted(os.listdir(d), key=lambda s: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s)]):
            mm = re.fullmatch(r"db_(\d+)_(\d+)\.txt", f)
            if not mm:
                continue
            nums = [int(x) for x in open(os.path.join(d, f)).read().split()]
            n = int(mm.group(1))
            if len(nums) != n * n:
                out.append(f"[eq677 db] {f}: {len(nums)} entries, expected {n * n} - skipped")
                continue
            t = [nums[i * n:(i + 1) * n] for i in range(n)]
            mul = lambda a, b: t[a][b]
            idem = all(t[x][x] == x for x in range(n))
            sat255 = all(LAW255(mul, x) == x for x in range(n))
            out.append(f"[eq677 db] db/{n}/{mm.group(2)}: law 677 {holds(t, LAWS[677])}, latin(rows, cols) "
                       f"{is_latin(t)}, idempotent {idem}, satisfies 255 {sat255}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
