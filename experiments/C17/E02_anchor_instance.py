"""EXP-C17-02: for anchored magmas, when does checking a law only at z = 0 decide the law?"""

import itertools

import numpy as np

from systems.law_testing import naive
from systems.magma import MagmaSAT, fill, n_leaves, parse, satisfies, shapes, to_str

META = {
    "id": "EXP-C17-02",
    "cycle": "C17",
    "title": "The anchor instance of a law: when is the O(n^2) check at z = 0 a decision procedure?",
    "agent": "Mathematical Skeptic",
    "question": "For anchored magmas (x*0 = x+1 mod N), the instance of a three-variable law with z = 0 can be checked "
                "with O(N^2) probes. For which laws of the C06 family does it imply the full law?",
    "hypothesis": "H-C17-2 (bold): for every law of the C06 family (x(yz) = t or (xy)z = t, t with 3-4 leaves over "
                  "x, y, z), every anchored magma satisfying the z = 0 instance satisfies the law (N <= 5).",
    "assumptions": ["N = 2..5 for the census; left-distributivity additionally for N = 2..10",
                    "models of {anchor, z = 0 instance} enumerated completely when there are at most "
                    "3000 of them; where the enumeration is capped, a SAT query asks directly for an anchored "
                    "model of the instance that violates the law (conflict budget 10^6)"],
    "methodology": "For each of the 382 laws: substitute z := 0 in both sides, enumerate the anchored models of that "
                   "two-variable identity with MagmaSAT, and test the full law on each model; a law is "
                   "'insufficient' as soon as one violating model is found at some N, 'decides' when no violating "
                   "model exists at any N = 2..5. (Revised after the Skeptic's review: the first version counted a "
                   "law with a capped enumeration at one N as undecided even when a violation had been found at "
                   "another N.)",
    "falsification": "Any law with an anchored model of its z = 0 instance that violates the law.",
}

VARS = ["x", "y", "z"]


def laws():
    rhs = []
    for k in (2, 3):
        for sh in shapes(k):
            for lab in itertools.product(VARS, repeat=n_leaves(sh)):
                if set(lab) == set(VARS):
                    rhs.append(fill(sh, lab))
    out = []
    for l in ("x(yz)", "(xy)z"):
        lt = parse(l)
        for t in rhs:
            if t != lt:
                out.append((f"{l} = {to_str(t)}", (lt, t)))
    return out


def subst0(t):
    if isinstance(t, str):
        return "0" if t == "z" else t
    return (subst0(t[0]), subst0(t[1]))


class AnchorSAT(MagmaSAT):
    """MagmaSAT whose identities may contain the constant '0'."""

    def _encode(self, t, asg):
        if t == "0":
            return 0
        return super()._encode(t, asg)

    def _key(self, t, asg):
        return (to_str(t), tuple(sorted(asg.items())))


def anchor(n):
    return lambda S: [[S.v[x, 0, (x + 1) % n]] for x in range(n)]


def value(T, t, asg):
    """Value of a term whose leaves are variables or the constant '0'."""
    if isinstance(t, str):
        return 0 if t == "0" else asg[t]
    return int(T[value(T, t[0], asg), value(T, t[1], asg)])


def holds(T, s, t, names):
    N = T.shape[0]
    return all(value(T, s, dict(zip(names, v))) == value(T, t, dict(zip(names, v)))
               for v in itertools.product(range(N), repeat=len(names)))


def violating_model(s, t, inst, N, budget=10 ** 6):
    """SAT query: an anchored model of the z = 0 instance that violates the full law s = t."""
    sat = AnchorSAT(N, [inst], extra=anchor(N))
    sel = []
    for sigma in itertools.product(range(N), repeat=3):
        asg = dict(zip(VARS, sigma))
        ls, lt = sat._encode(s, asg), sat._encode(t, asg)
        d = sat.pool.id(("violation",) + sigma)
        sel.append(d)
        for c in range(N):                 # d -> the two sides do not both take the value c
            if (isinstance(ls, int) and ls != c) or (isinstance(lt, int) and lt != c):
                continue
            sat.clauses.append([-d] + ([] if isinstance(ls, int) else [-ls[c]]) +
                               ([] if isinstance(lt, int) else [-lt[c]]))
    sat.clauses.append(sel)
    status, T = sat.solve(conf_budget=budget)
    if status == "SAT":
        assert holds(T, inst[0], inst[1], ["x", "y"]) and not holds(T, s, t, VARS), "SAT answer is not a violating model"
        assert all(T[x, 0] == (x + 1) % N for x in range(N))
    return status, T


def run():
    rows = []
    for name, (s, t) in laws():
        inst = (subst0(s), subst0(t))
        res = {}
        for N in range(2, 6):
            tabs, complete = AnchorSAT(N, [inst], extra=anchor(N)).enumerate(limit=3000)
            if complete:
                viol = [T for T in tabs if not satisfies(T, (s, t))]
                res[N] = {"models_of_instance": len(tabs), "violating_full_law": len(viol)}
            else:
                status, T = violating_model(s, t, inst, N)
                res[N] = {"models_of_instance": "more than 3000", "violating_model_by_SAT": status,
                          "example": T.tolist() if status == "SAT" else None}
        insufficient = any(v.get("violating_full_law", 0) > 0 or v.get("violating_model_by_SAT") == "SAT"
                           for v in res.values())
        decided = all(v.get("violating_full_law") == 0 or v.get("violating_model_by_SAT") == "UNSAT"
                      for v in res.values())
        undecided = not insufficient and not decided
        rows.append({"law": name, "by_N": {str(k): v for k, v in res.items()}, "instance_decides": decided,
                     "instance_insufficient": insufficient, "not_decided": undecided})
    fails = [r["law"] for r in rows if r["instance_insufficient"]]
    ok = [r["law"] for r in rows if r["instance_decides"]]
    first_fail = {}
    for r in rows:
        if r["instance_insufficient"]:
            n0 = min(int(k) for k, v in r["by_N"].items()
                     if v.get("violating_full_law", 0) > 0 or v.get("violating_model_by_SAT") == "SAT")
            first_fail[n0] = first_fail.get(n0, 0) + 1
    assoc = next(r for r in rows if r["law"] == "x(yz) = (xy)z")
    ld = next(r for r in rows if r["law"] == "x(yz) = (xy)(xz)")
    s_ld, t_ld = parse("x(yz)"), parse("(xy)(xz)")
    inst_ld = (subst0(s_ld), subst0(t_ld))
    ld_ext = {}
    for N in range(2, 11):
        tabs, complete = AnchorSAT(N, [inst_ld], extra=anchor(N)).enumerate(limit=3000)
        ld_ext[str(N)] = {"models_of_instance": len(tabs), "complete": complete,
                          "violating_LD": sum(1 for T in tabs if not satisfies(T, (s_ld, t_ld)))}
    return {
        "n_laws": len(rows),
        "instance_decides": len(ok),
        "instance_insufficient": len(fails),
        "not_decided": sum(r["not_decided"] for r in rows),
        "first_violation_at_N": {str(k): v for k, v in sorted(first_fail.items())},
        "insufficient_laws": fails,
        "associativity": assoc,
        "left_distributivity": ld,
        "left_distributivity_instance_N_le_10": ld_ext,
        "rows": rows,
        "summary": [f"{len(rows)} laws, N = 2..5: z=0 instance decides the law for {len(ok)}, is insufficient for "
                    f"{len(fails)} (first violating model at N = " +
                    ", ".join(f"{k}: {v} laws" for k, v in sorted(first_fail.items())) +
                    f"), not decided for {sum(r['not_decided'] for r in rows)}",
                    f"associativity: {assoc['by_N']}",
                    "LD wrap-around instance x*(y+1) = (x*y)*(x+1), N = 2..10, models (violating LD): " +
                    ", ".join(f"{N}: {v['models_of_instance']} ({v['violating_LD']})" for N, v in ld_ext.items())],
    }
