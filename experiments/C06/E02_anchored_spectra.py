"""EXP-C06-02: which identities admit successor-anchored models, and how many? (SAT, independent of Laver's recursion)"""

import time

from systems.magma import MagmaSAT, parse

META = {
    "id": "EXP-C06-02",
    "cycle": "C06",
    "title": "Spectra and model counts of successor-anchored magmas for invented identities",
    "agent": "Mathematical Inventor",
    "question": "If left-distributivity is replaced by another composition law, which sizes N admit a magma with "
                "x * 0 = x + 1 (mod N), and how many are there?",
    "hypothesis": "H-C06-1: LD + anchor has exactly one model for N in {1,2,4,8} and none otherwise (N <= 10). "
                  "H-C06-2 (bold, inventor): restricted 'power-of-two' spectra are special to left-distributivity; "
                  "other balanced 3-variable laws give either every N or no N > 1.",
    "assumptions": ["sizes N = 1..10 (LD, RD up to 10; others up to 8)", "complete enumeration with blocking "
                    "clauses (limit 2000 models)", "anchor fixes the whole column 0"],
    "methodology": "MagmaSAT (exact encoding from C05) with unit clauses v[x,0,x+1]; count all models (anchored "
                   "structures have no non-trivial anchored isomorphisms, so tables = classes); record spectrum and "
                   "counts; independent of Laver's recursion.",
    "falsification": "An LD-anchored model for N not a power of two, two models for a power of two, or a "
                     "non-LD law with a restricted non-trivial spectrum.",
}

LAWS = {
    "LD  x(yz)=(xy)(xz)": "x(yz)=(xy)(xz)",
    "RD  (xy)z=(xz)(yz)": "(xy)z=(xz)(yz)",
    "assoc  x(yz)=(xy)z": "x(yz)=(xy)z",
    "left-permutable  x(yz)=y(xz)": "x(yz)=y(xz)",
    "right-permutable  (xy)z=(xz)y": "(xy)z=(xz)y",
    "x(yz)=(xy)(yz)": "x(yz)=(xy)(yz)",
    "x(yz)=(xz)(yz)": "x(yz)=(xz)(yz)",
    "(xy)z=(xy)(xz)": "(xy)z=(xy)(xz)",
    "x(yz)=(yx)(zx)": "x(yz)=(yx)(zx)",
    "x(xy)=xy": "x(xy)=xy",
    "x(yx)=xy": "x(yx)=xy",
    "(xy)y=xy": "(xy)y=xy",
}


def anchor(n):
    return lambda S: [[S.v[x, 0, (x + 1) % n]] for x in range(n)]


def run():
    rows, timings = {}, {}
    for name, law in LAWS.items():
        s, t = law.split("=")
        ident = [(parse(s), parse(t))]
        maxN = 10 if name.startswith(("LD", "RD")) else 8
        counts = {}
        t0 = time.perf_counter()
        for N in range(1, maxN + 1):
            # Anchored tables are counted directly: an isomorphism of anchored structures must fix 0 and
            # commute with the successor x -> x*0, hence is the identity, so no isomorphism reduction applies.
            tables, complete = MagmaSAT(N, ident, extra=anchor(N)).enumerate(limit=2000)
            counts[str(N)] = {"models": len(tables), "complete": complete,
                              "first": tables[0].tolist() if tables and N <= 4 else None}
        timings[name] = round(time.perf_counter() - t0, 2)
        spectrum = [int(N) for N, c in counts.items() if c["models"] > 0]
        rows[name] = {"spectrum": spectrum, "counts": {N: c["models"] for N, c in counts.items()},
                      "all_complete": all(c["complete"] for c in counts.values()), "examples": counts}
    ld = rows["LD  x(yz)=(xy)(xz)"]["counts"]
    return {
        "rows": rows,
        "timings": timings,
        "summary": [f"LD anchored model counts N=1..10: {ld}"] +
                   [f"{k}: spectrum {v['spectrum']} counts {v['counts']}" for k, v in rows.items()],
    }
