"""EXP-C06-03: is a restricted anchored spectrum special to left-distributivity? (all laws a(bc) = t, (ab)c = t)"""

import itertools
import time

from systems.magma import MagmaSAT, fill, n_leaves, parse, shapes, to_str

META = {
    "id": "EXP-C06-03",
    "cycle": "C06",
    "title": "Anchored spectra of all laws x(yz) = t and (xy)z = t with t of 3-4 leaves over {x,y,z}",
    "agent": "Mathematical Skeptic",
    "question": "Among all laws whose left side is x(yz) or (xy)z and whose right side is any term with 3 or 4 "
                "leaves using exactly the variables x, y, z, which admit a successor-anchored model (x*0 = x+1 "
                "mod N) for which N <= 6?",
    "hypothesis": "H-C06-2 (bold): every such law other than left-distributivity has anchored spectrum {1} or "
                  "{1,...,6}; a restricted non-trivial spectrum is special to LD.",
    "assumptions": ["sizes N = 1..6; laws with a restricted spectrum are re-run for N = 7, 8",
                    "SAT conflict budget 2,000,000 per instance; UNKNOWN is recorded, never guessed",
                    "laws are taken up to renaming of variables (left side normalised to x(yz) or (xy)z)"],
    "methodology": "Enumerate right sides (2 shapes x 6 labelings for 3 leaves, 5 shapes x 36 surjective "
                   "labelings for 4 leaves), drop t equal to the left side, solve MagmaSAT(N, law, anchor) for "
                   "N = 1..6, classify spectra, extend restricted ones to N = 8.",
    "falsification": "Any law other than x(yz) = (xy)(xz) with a spectrum strictly between {1} and {1..6}.",
}

LHS = ["x(yz)", "(xy)z"]
VARS = ["x", "y", "z"]


def anchor(n):
    return lambda S: [[S.v[x, 0, (x + 1) % n]] for x in range(n)]


def right_sides():
    out = []
    for k in (2, 3):  # internal nodes: 3 or 4 leaves
        for sh in shapes(k):
            m = n_leaves(sh)
            for lab in itertools.product(VARS, repeat=m):
                if set(lab) == set(VARS):
                    out.append(fill(sh, lab))
    return out


def spectrum(law, sizes, budget=2_000_000):
    res = {}
    for N in sizes:
        status, _ = MagmaSAT(N, [law], extra=anchor(N)).solve(conf_budget=budget)
        res[N] = status
    return res


def run():
    t0 = time.perf_counter()
    rows = []
    rhs = right_sides()
    for lhs_s in LHS:
        lhs = parse(lhs_s)
        for t in rhs:
            if t == lhs:
                continue
            law = (lhs, t)
            sp = spectrum(law, range(1, 7))
            rows.append({"law": f"{lhs_s} = {to_str(t)}", "spectrum": sp, "_law": law})
    unknown = [r["law"] for r in rows if "UNKNOWN" in r["spectrum"].values()]
    for r in rows:
        sat = [N for N, s in r["spectrum"].items() if s == "SAT"]
        r["sat"] = sat
        if sat == [1]:
            r["class"] = "trivial only"
        elif sat == list(range(1, 7)):
            r["class"] = "all N <= 6"
        else:
            r["class"] = "restricted"
            r["extended"] = spectrum(r["_law"], [7, 8])
    for r in rows:
        del r["_law"]
    classes = {}
    for r in rows:
        classes.setdefault(r["class"], []).append(r["law"])
    restricted = [{"law": r["law"], "sat_le6": r["sat"], "N7_8": r.get("extended")} for r in rows
                  if r["class"] == "restricted"]
    return {
        "n_laws": len(rows),
        "class_counts": {k: len(v) for k, v in classes.items()},
        "restricted": restricted,
        "unknown": unknown,
        "all_complete": not unknown,
        "rows": rows,
        "timings": {"total_s": round(time.perf_counter() - t0, 1)},
        "summary": [f"{len(rows)} laws: " + ", ".join(f"{k}: {len(v)}" for k, v in classes.items()),
                    f"restricted spectra: {restricted}", f"UNKNOWN instances: {len(unknown)}"],
    }
