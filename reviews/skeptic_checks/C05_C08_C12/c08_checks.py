"""Skeptic checks for cycle C08 (circle products), driving the independent C checker c08_assoc.

Usage: python3 c08_checks.py <part>   parts: knuth | thresholds | posbeta | negbeta | nonpisot
Writes out/c08_<part>.json.  Build first: gcc -O2 -o c08_assoc c08_assoc.c
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
BIN = str(HERE / "c08_assoc")


def run(coeffs, init, smin, smax, N, T, R, seed=12345):
    d = len(coeffs)
    assert len(init) == d
    args = [BIN, str(d)] + [str(c) for c in coeffs] + [str(x) for x in init] + \
           [str(smin), str(smax), str(N), str(T), str(R), str(seed)]
    out = subprocess.run(args, capture_output=True, text=True, check=True).stdout.split("\n")
    res = {}
    for line in out:
        if not line.strip():
            continue
        if line.startswith("ERROR"):
            raise RuntimeError(line)
        parts = line.split()
        s = int(parts[0])
        if parts[1] == "PASS":
            res[s] = {"pass": True, "tested": int(parts[2]), "skipped": int(parts[3])}
        else:
            res[s] = {"pass": False, "triple": [int(x) for x in parts[2:5]]}
    return res


def head(coeffs, init, n=8):
    G = list(init)
    while len(G) < n:
        G.append(sum(c * G[-1 - i] for i, c in enumerate(coeffs)))
    return G


def roots(coeffs):
    return np.roots([1] + [-c for c in coeffs])


def shifts_pass(res):
    return sorted(s for s, r in res.items() if r["pass"])


def upward_closed(passing, smax):
    return bool(passing) and passing == list(range(passing[0], smax + 1))


def part_knuth():
    # Theorem 1 sanity + counterexamples for s = 0, 1 (G-indexing), strong tests
    res = run([1, 1], [1, 2], 0, 24, 60, 200000, 10**9, seed=1)
    return {"fibonacci_s0_24": {str(k): v for k, v in res.items()}}


SEQS_THRESH = {
    "Fibonacci 1,2": ([1, 1], [1, 2]),
    "Pell 1,2 (2,1)": ([2, 1], [1, 2]),
    "(2,2) 1,2": ([2, 2], [1, 2]),
    "tribonacci 1,2,4": ([1, 1, 1], [1, 2, 4]),
    "4-bonacci 1,2,4,8": ([1, 1, 1, 1], [1, 2, 4, 8]),
    "G(k+1)=G(k)+G(k-2) 1,2,3": ([1, 0, 1], [1, 2, 3]),
    "(3,3) 1,5": ([3, 3], [1, 5]),
    "G(k+1)=G(k)+G(k-3) 1,2,3,4": ([1, 0, 0, 1], [1, 2, 3, 4]),
    "1,3,4,7,11 (1,1) G1=3": ([1, 1], [1, 3]),
    "1,4,5,9,14 (1,1) G1=4": ([1, 1], [1, 4]),
}


def part_thresholds():
    out = {}
    for name, (c, g) in SEQS_THRESH.items():
        t0 = time.time()
        res = run(c, g, 0, 24, 40, 100000, 10**6, seed=7)
        p = shifts_pass(res)
        out[name] = {"head": head(c, g), "passing_shifts": p,
                     "failures": {str(s): r["triple"] for s, r in res.items() if not r["pass"]},
                     "min_tested_among_passing": min((res[s]["tested"] for s in p), default=None),
                     "seconds": round(time.time() - t0, 1)}
        print(name, p, flush=True)
    return out


def quadratic_family(sign):
    """Quadratic Pisot recurrences G_{k+1} = p G_k + q G_{k-1} with real conjugate beta of the given sign."""
    fam = []
    for p in range(1, 9):
        for q in range(-8, 9):
            if q == 0:
                continue
            disc = p * p + 4 * q
            if disc <= 0:
                continue
            r = sorted(np.roots([1, -p, -q]).real, key=abs)
            beta, alpha = r[0], r[1]
            if not (alpha > 1 and 1e-9 < abs(beta) < 1 - 1e-9):
                continue
            if (beta > 0) != (sign > 0):
                continue
            if int(round(disc ** 0.5)) ** 2 == disc and False:
                pass
            for g1 in range(2, 13):
                G = head([p, q], [1, g1], 12)
                if any(b <= a for a, b in zip(G, G[1:])):
                    continue
                if G[1] * G[1] == G[0] * G[2] and G[2] * G[2] == G[1] * G[3]:
                    continue      # geometric
                fam.append((p, q, g1, float(beta), float(alpha)))
    return fam


def part_beta(sign, smax, label):
    fam = quadratic_family(sign)
    rows, viol = [], []
    for (p, q, g1, beta, alpha) in fam:
        # keep products inside 2^122: inputs up to R, shifts up to smax
        R = 10**5 if alpha < 4 else 10**4
        res = run([p, q], [1, g1], 0, smax, 25, 20000, R, seed=p * 1000 + (q + 10) * 31 + g1)
        ps = shifts_pass(res)
        up = upward_closed(ps, smax)
        skipped_max = max((res[s]["skipped"] for s in ps), default=0)
        row = {"p": p, "q": q, "g1": g1, "beta": round(beta, 6), "head": head([p, q], [1, g1], 7),
               "passing_shifts": ps, "upward_closed": up, "max_skipped": skipped_max,
               "fail_triples": {str(s): r["triple"] for s, r in res.items() if not r["pass"]}}
        rows.append(row)
        if ps and not up:
            viol.append(row)
    return {"family": label, "n_sequences": len(rows), "n_non_upward_closed": len(viol),
            "n_without_passing_shift": sum(not r["passing_shifts"] for r in rows),
            "non_upward_closed": [{k: r[k] for k in ("p", "q", "g1", "beta", "head", "passing_shifts")} for r in viol],
            "rows": rows}


def part_posbeta():
    return part_beta(+1, 16, "beta > 0")


def part_negbeta():
    return part_beta(-1, 16, "beta < 0")


NONPISOT = {
    "(1,2) 1,3": ([1, 2], [1, 3]), "(1,2) 1,4": ([1, 2], [1, 4]), "(1,2) 1,5": ([1, 2], [1, 5]),
    "(1,3) 1,2": ([1, 3], [1, 2]), "(1,3) 1,3": ([1, 3], [1, 3]), "(1,3) 1,4": ([1, 3], [1, 4]),
    "(1,3) 1,5": ([1, 3], [1, 5]),
    "(2,3) 1,2": ([2, 3], [1, 2]), "(2,3) 1,4": ([2, 3], [1, 4]), "(2,3) 1,5": ([2, 3], [1, 5]),
    # new ones (not in the lab's set)
    "Mersenne 2^(k+1)-1 (3,-2) 1,3": ([3, -2], [1, 3]),
    "(3,-2) 1,4": ([3, -2], [1, 4]),
    "(1,1,2) 1,2,3 (roots 2, cube roots of 1)": ([1, 1, 2], [1, 2, 3]),
    "(1,4) 1,2": ([1, 4], [1, 2]), "(2,4) 1,3": ([2, 4], [1, 3]), "(1,6) 1,2": ([1, 6], [1, 2]),
    "(2,8) 1,3": ([2, 8], [1, 3]), "(0,2,?) G_{k+1}=2G_{k-1}+... (1,2,1) 1,2,3": ([1, 2, 1], [1, 2, 3]),
    "(4,-3) 1,2 (roots 3,1)": ([4, -3], [1, 2]),
    "(1,1,1,2) 1,2,4,8": ([1, 1, 1, 2], [1, 2, 4, 8]),
}


def part_nonpisot():
    out = {}
    for name, (c, g) in NONPISOT.items():
        rts = roots(c)
        mods = sorted(abs(rts))
        res = run(c, g, 0, 25, 30, 50000, 10**5, seed=99)
        ps = shifts_pass(res)
        out[name] = {"head": head(c, g), "root_moduli": [round(float(m), 6) for m in mods],
                     "passing_shifts": ps,
                     "min_tested_among_passing": min((res[s]["tested"] for s in ps), default=None)}
        print(name, ps, flush=True)
    return out


PARTS = {"knuth": part_knuth, "thresholds": part_thresholds, "posbeta": part_posbeta,
         "negbeta": part_negbeta, "nonpisot": part_nonpisot}

if __name__ == "__main__":
    part = sys.argv[1]
    t0 = time.time()
    res = PARTS[part]()
    res = {"part": part, "result": res, "wall_seconds": round(time.time() - t0, 1)}
    (OUT / f"c08_{part}.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res, default=str)[:4000])
