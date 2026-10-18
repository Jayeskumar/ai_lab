"""EXP-C08-02: Pisot structure of the base sequence versus associativity of circle products."""

import random

import numpy as np

from lab.seqtools import berlekamp_massey
from systems.circle import BaseSequence

from experiments.C08.E01_associativity_atlas import families

META = {
    "id": "EXP-C08-02",
    "cycle": "C08",
    "title": "Circle-product associativity versus the Pisot property of the minimal recurrence",
    "agent": "Mathematical Explorer",
    "question": "What distinguishes base sequences whose circle products become associative?",
    "hypothesis": "H-C08-2: if the minimal recurrence of G has a characteristic root beta != alpha (dominant) with "
                  "|beta| >= 1, then o_s is non-associative for every shift s. H-C08-3: if it is Pisot (all other "
                  "roots inside the unit circle), o_s is associative for all sufficiently large s.",
    "assumptions": ["minimal recurrence from Berlekamp-Massey on 24 terms (verified on 40)", "shifts s = 0..8",
                    "exhaustive triples in [1,16]^3 plus 1500 random triples in [1,3000]^3 per (G, s)"],
    "methodology": "Classify each base sequence (geometric / Pisot / non-Pisot) by the roots of its minimal "
                   "polynomial; test associativity per shift; report the set of associative shifts.",
    "falsification": "A non-Pisot sequence with an associative shift, or a Pisot sequence failing at all large "
                     "shifts tested.",
    "seed": 8,
}


def classify(G: BaseSequence):
    G.extend(40)
    c = berlekamp_massey(G.G[:24])
    ok = all(sum(c[i] * G.G[n - 1 - i] for i in range(len(c))) == G.G[n] for n in range(len(c), 41))
    poly = [1] + [-float(x) for x in c]                      # x^d - c1 x^(d-1) - ...
    roots = np.roots(poly)
    mods = sorted(abs(r) for r in roots)
    alpha = max(mods)
    others = mods[:-1]
    if len(c) == 1:
        kind = "geometric"
    elif all(m < 1 - 1e-9 for m in others):
        kind = "Pisot"
    else:
        kind = "non-Pisot"
    return {"minimal_recurrence": [str(x) for x in c], "verified_on_40_terms": ok, "dominant_root": round(alpha, 6),
            "other_root_moduli": [round(m, 6) for m in others], "kind": kind}


def assoc_shifts(G, rng, smax=8):
    res = {}
    for s in range(0, smax + 1):
        bad = None
        for a in range(1, 17):
            for b in range(1, 17):
                ab = G.circle(a, b, s)
                for c in range(1, 17):
                    if G.circle(ab, c, s) != G.circle(a, G.circle(b, c, s), s):
                        bad = (a, b, c)
                        break
                if bad:
                    break
            if bad:
                break
        if bad is None:
            for _ in range(1500):
                a, b, c = (rng.randint(1, 3000) for _ in range(3))
                if G.circle(G.circle(a, b, s), c, s) != G.circle(a, G.circle(b, c, s), s):
                    bad = (a, b, c)
                    break
        res[s] = bad
    return res


def run():
    rng = random.Random(META["seed"])
    seqs = families() + [
        BaseSequence("Pell 1,2,5 (2,1)", [1, 2, 5], (2, 1)),
        BaseSequence("G(k+1)=G(k)+G(k-3); 1,2,3,4", [1, 2, 3, 4], (1, 0, 0, 1)),
        BaseSequence("G(k+1)=2G(k)-G(k-1)+G(k-2) (non-Pisot?); 1,2,4", [1, 2, 4], (2, -1, 1)),
        BaseSequence("G(k+1)=G(k)+G(k-1)+2G(k-2); 1,2,4", [1, 2, 4], (1, 1, 2)),
    ]
    rows, h2_bad, h3_bad = [], [], []
    for G in seqs:
        info = classify(G)
        shifts = assoc_shifts(G, rng)
        good = [s for s, bad in shifts.items() if bad is None]
        row = {"G": G.name, "head": G.G[:8], **info, "associative_shifts": good,
               "first_failures": {str(s): bad for s, bad in shifts.items() if bad}}
        rows.append(row)
        if info["kind"] == "non-Pisot" and good:
            h2_bad.append(row)
        if info["kind"] == "Pisot" and not any(s in good for s in (6, 7, 8)):
            h3_bad.append(row)
    return {
        "rows": rows,
        "h2_violations": [(r["G"], r["associative_shifts"]) for r in h2_bad],
        "h3_violations": [(r["G"], r["associative_shifts"]) for r in h3_bad],
        "summary": [
            f"{len(rows)} base sequences: " + ", ".join(f"{k}: {sum(r['kind'] == k for r in rows)}"
                                                       for k in ("geometric", "Pisot", "non-Pisot")),
            f"H-C08-2 violations (non-Pisot with an associative shift): {len(h2_bad)}",
            f"H-C08-3 violations (Pisot, no associative shift among s = 6..8): {len(h3_bad)}",
        ],
    }
