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
                    "3000 of them; otherwise the law is reported as 'too many models' (not decided)"],
    "methodology": "For each of the 382 laws: substitute z := 0 in both sides, enumerate the anchored models of that "
                   "two-variable identity with MagmaSAT, and test the full law on each model.",
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


def run():
    rows = []
    for name, (s, t) in laws():
        inst = (subst0(s), subst0(t))
        res = {}
        for N in range(2, 6):
            tabs, complete = AnchorSAT(N, [inst], extra=anchor(N)).enumerate(limit=3000)
            if not complete:
                res[N] = "too many models"
                continue
            viol = [T for T in tabs if not satisfies(T, (s, t))]
            res[N] = {"models_of_instance": len(tabs), "violating_full_law": len(viol)}
        decided = all(isinstance(v, dict) and v["violating_full_law"] == 0 for v in res.values())
        undecided = any(v == "too many models" for v in res.values())
        rows.append({"law": name, "by_N": {str(k): v for k, v in res.items()}, "instance_decides": decided,
                     "not_decided_by_enumeration": undecided})
    fails = [r["law"] for r in rows if not r["instance_decides"] and not r["not_decided_by_enumeration"]]
    ok = [r["law"] for r in rows if r["instance_decides"]]
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
        "too_many_models": sum(r["not_decided_by_enumeration"] for r in rows),
        "examples_insufficient": fails[:20],
        "associativity": assoc,
        "left_distributivity": ld,
        "left_distributivity_instance_N_le_10": ld_ext,
        "rows": rows,
        "summary": [f"{len(rows)} laws, N = 2..5: z=0 instance decides the law for {len(ok)}, is insufficient for "
                    f"{len(fails)}, undecided (too many models) for {sum(r['not_decided_by_enumeration'] for r in rows)}",
                    f"associativity: {assoc['by_N']}",
                    "LD wrap-around instance x*(y+1) = (x*y)*(x+1), N = 2..10, models (violating LD): " +
                    ", ".join(f"{N}: {v['models_of_instance']} ({v['violating_LD']})" for N, v in ld_ext.items())],
    }
