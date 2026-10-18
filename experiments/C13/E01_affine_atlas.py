"""EXP-C13-01: the atlas of affine anchored spectra - which integer sets do single laws cut out?"""

import time
from collections import defaultdict
from math import gcd

import sympy as sp

from lab import oeis
from systems.anchored import (affine_roots, affine_spectrum, affine_system, enumerate_laws, factorize,
                              law_from_key, law_str, pstr)

META = {
    "id": "EXP-C13-01",
    "cycle": "C13",
    "title": "Atlas of affine anchored spectra for all laws with at most 4 leaves per side (and 2-variable laws "
             "with at most 5)",
    "agent": "Mathematical Explorer",
    "question": "For every law s = t over {x,y,z} with at most 4 leaves per side (up to renaming and exchange of "
                "sides), and every law over {x,y} with at most 5 leaves per side, which sets of N admit an affine "
                "anchored model x*y = x + a*y + 1 (mod N)? Which arithmetic sets occur?",
    "hypothesis": "H-C13-3: affine spectra are exactly the sets {N : a fixed polynomial system has a root mod N}; "
                  "they are divisor-closed and closed under coprime products, every finite one is the set of "
                  "divisors of a single integer, and the infinite ones are governed by the Q-gcd of the system "
                  "(a classical quadratic/cubic residue condition plus finitely many exceptional primes).",
    "assumptions": ["laws up to renaming of variables and exchange of sides; s != t",
                    "affine spectra computed through prime powers <= 200 (CRT); finite spectra computed exactly "
                    "from a resultant bound", "OEIS lookups of every infinite spectrum (terms <= 200)"],
    "methodology": "Evaluate both sides as linear forms with coefficients in Z[a]; the law's affine system is the set "
                   "of coefficient differences. Group laws by system, then systems by spectrum. For each system "
                   "compute the gcd over Q[a]; if it is constant, bound the spectrum by the gcd of the pairwise "
                   "resultants R and find the largest prime powers dividing R that admit a common root; otherwise "
                   "record the gcd polynomial. Look up every infinite spectrum in the OEIS and record the hits.",
    "falsification": "A finite affine spectrum that is not the set of divisors of its maximum, or a spectrum that is "
                     "not divisor-closed, would contradict the (proved) Theorem 1 of proofs/paper/C13.md and reveal "
                     "an implementation error.",
}

A = sp.Symbol("a")


def _sp(p):
    return sp.Poly(list(reversed(p)), A, domain="ZZ")


def classify(system):
    if not system:
        return {"kind": "all", "gcd": "0"}
    polys = [_sp(p) for p in system]
    g = polys[0]
    for q in polys[1:]:
        g = sp.gcd(g, q)
    if g.degree() >= 1:
        prim = g.primitive()[1]
        return {"kind": "infinite", "gcd": str(prim.as_expr()), "disc": int(sp.discriminant(prim.as_expr(), A))
                if prim.degree() >= 2 else None}
    # coprime over Q: bound by resultants
    R = 0
    consts = [abs(int(p.as_expr())) for p in polys if p.degree() <= 0]
    for c in consts:
        R = gcd(R, c)
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            if polys[i].degree() >= 1 and polys[j].degree() >= 1:
                r = int(sp.resultant(polys[i].as_expr(), polys[j].as_expr(), A))
                if r:
                    R = gcd(R, abs(r))
    if R == 0:  # no coprime pair: use generic integer combinations of the others (the ideal is still (1) over Q)
        nonconst = [q for q in polys if q.degree() >= 1]
        for shift in range(1, 6):
            comb = sum(((i + shift) * q.as_expr() for i, q in enumerate(nonconst[1:])), sp.Integer(0))
            r = int(sp.resultant(nonconst[0].as_expr(), sp.expand(comb), A)) if comb != 0 else 0
            if r:
                R = abs(r)
                break
    L = 1
    for p, e in factorize(R).items() if R > 1 else []:
        best = 0
        for k in range(1, e + 1):
            if affine_roots(system, p ** k):
                best = k
            else:
                break
        L *= p ** best
    return {"kind": "finite", "gcd": "1", "bound_R": R, "L": L, "R_found": R != 0}


def run():
    t0 = time.perf_counter()
    families = {"3var_le4": enumerate_laws(("x", "y", "z"), 4), "2var_le5": enumerate_laws(("x", "y"), 5)}
    out = {}
    all_spectra = {}
    no_bound = [0]
    for fam, laws in families.items():
        groups = defaultdict(list)
        for k in laws:
            groups[affine_system(law_from_key(k))].append(k)
        spec = defaultdict(list)
        for sysm, ks in groups.items():
            spec[tuple(affine_spectrum(sysm, 200))].append((sysm, ks))
        rows = []
        for sp_, items in sorted(spec.items(), key=lambda kv: -sum(len(k) for _, k in kv[1])):
            sysm, ks = items[0]
            cls = [classify(sm) for sm, _ in items]
            no_bound[0] += sum(1 for c in cls if c["kind"] == "finite" and not c["R_found"])
            cl = dict(cls[0])
            kinds = sorted({c["kind"] for c in cls})
            if cl["kind"] == "finite":
                cl["L"] = max(c["L"] for c in cls)
            n_laws = sum(len(k) for _, k in items)
            rows.append({"spectrum_le200": list(sp_), "n_laws": n_laws, "n_systems": len(items),
                         "example": law_str(ks[0]), "examples": [law_str(k) for k in ks[:5]],
                         "system": [pstr(p) for p in sysm], **cl, "kinds": kinds,
                         "gcds": sorted({c["gcd"] for c in cls})[:12]})
            all_spectra.setdefault(sp_, []).append((fam, rows[-1]))
        out[fam] = {"n_laws": len(laws), "n_systems": len(groups), "n_spectra": len(rows), "rows": rows}
    # OEIS for infinite spectra (union over families)
    lookups = {}
    for sp_, occ in all_spectra.items():
        kind = occ[0][1]["kind"]
        if kind == "infinite" and len(sp_) >= 8:
            r = oeis.novelty_check(list(sp_)[:40])
            lookups[",".join(map(str, sp_[:12]))] = {"status": r.get("status"), "hits": r.get("hits", [])[:4],
                                                    "gcd": occ[0][1]["gcd"], "example": occ[0][1]["example"]}
    finite_bad = [r["example"] for f in out.values() for r in f["rows"] if r["kind"] == "finite" and
                  sorted(r["spectrum_le200"]) != [d for d in range(1, min(r["L"], 200) + 1) if r["L"] % d == 0]]
    mixed = [r["example"] for f in out.values() for r in f["rows"] if "finite" in r["kinds"] and len(r["kinds"]) > 1]
    finite_ok = not finite_bad
    summ = []
    for fam, d in out.items():
        summ.append(f"{fam}: {d['n_laws']} laws, {d['n_systems']} affine systems, {d['n_spectra']} distinct spectra")
        summ.append(f"{fam} finite spectra: " + "; ".join(f"Div({r['L']}) x{r['n_laws']}" for r in d["rows"]
                                                         if r["kind"] == "finite"))
        summ.append(f"{fam} infinite: " + "; ".join(f"{'/'.join(r['gcds'][:3])} x{r['n_laws']}" for r in d["rows"]
                                                   if r["kind"] != "finite"))
    summ.append(f"finite systems without an integer bound R (should be 0): {no_bound[0]}")
    summ.append(f"every finite spectrum is Div(L) for L = lcm: {finite_ok} {finite_bad[:3]}; "
                f"spectra mixing finite and infinite systems: {len(mixed)}")
    summ.append("OEIS: " + "; ".join(f"[{v['gcd']}] {v['status']} {[h['anumber'] for h in v['hits']]}"
                                     for v in lookups.values()))
    return {"families": out, "oeis": lookups, "finite_spectra_are_divisor_sets": finite_ok,
            "finite_counterexamples": finite_bad, "mixed_kind_spectra": mixed, "finite_without_bound": no_bound[0],
            "runtime_s": round(time.perf_counter() - t0, 1), "summary": summ}
