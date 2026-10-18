"""Skeptic check: CLM-C13-11 identifications (root sets of the 11 polynomials vs direct arithmetic definitions),
N <= 2000; plus the example laws and the 'up to exceptional primes' wording.  Own code, no systems/."""
import json, os, sys
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c13_lib import read_law, affine_system_of

NM = 2000
def rootset(p):            # p: coefficients low first
    out = []
    for N in range(1, NM + 1):
        a = np.arange(N, dtype=object)
        v = sum(c * a**i for i, c in enumerate(p))
        if any(int(x) % N == 0 for x in v):
            out.append(N)
    return out

def squares(N):
    return {(x * x) % N for x in range(N)}
def is_sq(c, N): return (c % N) in squares(N)
def fourth(c, N): return (c % N) in {pow(x, 4, N) for x in range(N)}
def pf(N): return list(sp.factorint(N).keys())

defs = {
 "2a+1 odd": ((1, 2), lambda N: N % 2 == 1),
 "3a+1 3∤N": ((1, 3), lambda N: N % 3 != 0),
 "a^2+1  -1 square": ((1, 0, 1), lambda N: is_sq(-1, N)),
 "a^2-2a-1  2 square": ((-1, -2, 1), lambda N: is_sq(2, N)),
 "a^2+2a-2  3 square": ((-2, 2, 1), lambda N: is_sq(3, N)),
 "a^2+a+1  x^2+x+1 has a root": ((1, 1, 1), lambda N: any((x*x + x + 1) % N == 0 for x in range(N))),
 "a^2-a-1  golden": ((-1, -1, 1), lambda N: any((x*x - x - 1) % N == 0 for x in range(N))),
 "2a^2+2a+1  all p ≡ 1 mod 4": ((1, 2, 2), lambda N: all(p % 4 == 1 for p in pf(N))),
 "2a^2-1  all p ≡ ±1 mod 8": ((-1, 0, 2), lambda N: all(p % 8 in (1, 7) for p in pf(N))),
 "a^4+1  -1 fourth power": ((1, 0, 0, 0, 1), lambda N: fourth(-1, N)),
 "a^4-a^2+1  all p ≡ 1 mod 12": ((1, 0, -1, 0, 1), lambda N: all(p % 12 == 1 for p in pf(N))),
}
res = {}
for name, (p, f) in defs.items():
    rs = set(rootset(p))
    direct = {N for N in range(1, NM + 1) if f(N)}
    diff = sorted(rs ^ direct)
    res[name] = {"n_in_set": len(rs), "differences": diff[:10]}
    print(f"{name:40s} |set|={len(rs):4d} differences (N<={NM}): {diff[:10]}")
ex = {"x(xx)=y(xy)": None, "(xx)(xy)=(yy)(yx)": None, "x=x((xx)x)": None, "((xx)x)x=((yy)y)y": None,
      "x=x(x(xx))": None, "x(xy)=y(yx)": None, "x((xy)y)=y((xx)x)": None}
for L in ex:
    ex[L] = sorted(affine_system_of(*read_law(L)))
    print("affine system of", L, ":", ex[L])
res["examples"] = ex
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "c13_identifications.json"), "w"), indent=1)
