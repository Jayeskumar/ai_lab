"""Targeted (extreme-conjugate) counterexample search for C08 claims, driving c08_extreme.

Usage: python3 c08_targeted.py <part>   parts: thresholds | quadratic
  thresholds: the sequences quoted in CLM-C08-05 / CLM-C08-04, every non-dominant root, shifts 0..14
  quadratic : all quadratic Pisot rows (both signs of beta) of c08_checks.quadratic_family, shifts 0..16
Writes out/c08_targeted_<part>.json.  Build first: gcc -O2 -o c08_extreme c08_extreme.c -lm
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from c08_checks import quadratic_family, head  # noqa: E402  (own module)

HERE = Path(__file__).resolve().parent
BIN = str(HERE / "c08_extreme")


def run(coeffs, init, rho, smin, smax, N, M, ND, C=300):
    args = [BIN, str(len(coeffs))] + [str(c) for c in coeffs] + [str(x) for x in init] + \
           [repr(float(rho.real)), repr(float(rho.imag)), str(smin), str(smax), str(N), str(M), str(ND), str(C)]
    out = subprocess.run(args, capture_output=True, text=True, check=True).stdout.strip().split("\n")
    res = {}
    for line in out:
        p = line.split()
        s = int(p[0])
        if p[1] == "CERT":
            res[s] = {"status": "CERT", "triple": [int(x) for x in p[2:5]]}
        elif p[1] == "CAND":
            res[s] = {"status": "CAND", "pair": [int(x) for x in p[2:4]]}
        else:
            res[s] = {"status": "NOFAIL", "pairs": int(p[2])}
    return res


def nondominant_roots(coeffs):
    r = np.roots([1] + [-c for c in coeffs])
    r = sorted(r, key=lambda z: -abs(z))[1:]
    out = []
    for z in r:                      # one representative per conjugate pair
        if z.imag < -1e-12:
            continue
        out.append(z)
    return out


SEQS = {
    "Fibonacci 1,2": ([1, 1], [1, 2]),
    "Pell 1,2": ([2, 1], [1, 2]),
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
    for name, (c, g) in SEQS.items():
        t0 = time.time()
        merged = {}
        for rho in nondominant_roots(c):
            nd = 2 if abs(rho.imag) < 1e-12 else 16
            res = run(c, g, rho, 0, 14, 400000, 150 if nd == 2 else 40, nd)
            for s, r in res.items():
                if s not in merged or (merged[s]["status"] == "NOFAIL" and r["status"] != "NOFAIL"):
                    merged[s] = r
        cert = sorted(s for s, r in merged.items() if r["status"] == "CERT")
        nofail = sorted(s for s, r in merged.items() if r["status"] == "NOFAIL")
        out[name] = {"head": head(c, g), "certified_failures": cert, "no_failure_found": nofail,
                     "largest_certified_failure": max(cert) if cert else None,
                     "triples": {str(s): merged[s].get("triple") for s in cert},
                     "seconds": round(time.time() - t0, 1)}
        print(name, "fail", cert, "nofail", nofail, flush=True)
    return out


def part_quadratic():
    rows, viol = [], []
    for sign in (+1, -1):
        for (p, q, g1, beta, alpha) in quadratic_family(sign):
            rho = complex(beta, 0.0)
            res = run([p, q], [1, g1], rho, 0, 16, 100000, 100, 2)
            cert = sorted(s for s, r in res.items() if r["status"] == "CERT")
            cand = sorted(s for s, r in res.items() if r["status"] == "CAND")
            nof = sorted(s for s, r in res.items() if r["status"] == "NOFAIL")
            up = all(not (s1 < s2) for s1 in nof for s2 in cert)
            row = {"p": p, "q": q, "g1": g1, "beta": round(beta, 6), "canonical": g1 in (p, p + 1),
                   "certified_failures": cert, "candidates_without_c": cand, "no_failure_found": nof,
                   "upward_closed_0_16": up}
            rows.append(row)
            if not up:
                viol.append(row)
    pos = [r for r in rows if r["beta"] > 0]
    neg = [r for r in rows if r["beta"] < 0]
    return {"n_rows": len(rows), "n_pos": len(pos), "n_neg": len(neg),
            "non_upward_pos": [r for r in viol if r["beta"] > 0],
            "non_upward_neg": [r for r in viol if r["beta"] < 0],
            "non_upward_canonical": [r for r in viol if r["canonical"]],
            "rows": rows}


PARTS = {"thresholds": part_thresholds, "quadratic": part_quadratic}

if __name__ == "__main__":
    part = sys.argv[1]
    t0 = time.time()
    res = PARTS[part]()
    res = {"part": part, "result": res, "wall_seconds": round(time.time() - t0, 1)}
    (HERE / "out" / f"c08_targeted_{part}.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res, default=str)[:3000])
