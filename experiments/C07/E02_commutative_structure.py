"""EXP-C07-02: structure and OEIS status of the commutative mex operations."""

import json

import numpy as np

from lab import oeis
from systems.mex import all_specs, closed_below, identity_elements, is_commutative, spec_name, table

META = {
    "id": "EXP-C07-02",
    "cycle": "C07",
    "title": "Commutative mex operations: identities, zeros, value growth and OEIS status of their sequences",
    "agent": "Historian",
    "question": "Do the non-associative commutative mex operations have recognisable structure (identity "
                "elements, absorbing elements, linear growth, known sequences)?",
    "hypothesis": "H-C07-3: every commutative mex operation has 0 as an absorbing element or an identity, and its "
                  "diagonal f(n,n) is a known OEIS sequence.",
    "assumptions": ["tables for a, b < 96; OEIS lookups cached in cache/oeis; constant, identity-like and "
                    "arithmetic-progression sequences are not looked up"],
    "methodology": "For each distinct commutative operation (first spec of each group, as in EXP-C07-01): "
                   "absorbing/identity checks on [0,96)^2, growth of f(n,n) and max f(a,b) for a,b < n, "
                   "OEIS novelty checks of the diagonal and of rows 1-3 (first 40 terms).",
    "falsification": "A commutative operation in which 0 is neither absorbing nor an identity, or a diagonal "
                     "without OEIS match.",
}

N = 96


def trivial(seq):
    s = list(seq)
    if len(set(s)) <= 2:
        return True
    d = [b - a for a, b in zip(s, s[1:])]
    return len(set(d)) == 1


def run():
    seen, rows = set(), []
    for spec in all_specs():
        T = table(spec, N)
        if not is_commutative(T):
            continue
        key = T[:64, :64].tobytes()
        if key in seen:
            continue
        seen.add(key)
        name = spec_name(spec)
        zero_absorbing = bool((T[0, :] == 0).all())
        zero_identity = bool((T[0, :] == np.arange(N)).all())
        diag = [int(T[i, i]) for i in range(N)]
        growth = [int(T[:n, :n].max()) for n in (8, 16, 32, 64, 96)]
        seqs = {"diag": diag[:40], "row1": T[1, :40].tolist(), "row2": T[2, :40].tolist(),
                "row3": T[3, :40].tolist()}
        lookups = {}
        for k, s in seqs.items():
            if trivial(s):
                lookups[k] = "trivial"
                continue
            r = oeis.novelty_check(s)
            lookups[k] = {"status": r["status"], "hits": [h["anumber"] + " " + h["name"][:80] for h in
                                                          r.get("hits", [])[:3]]}
        rows.append({"spec": name, "zero_absorbing": zero_absorbing, "zero_identity": zero_identity,
                     "identities": identity_elements(T, 16) if closed_below(T, 16) else None,
                     "max_value_growth": growth, "diag": diag[:24], "row2": T[2, :24].tolist(),
                     "oeis": lookups})
    no_match = [(r["spec"], k) for r in rows for k, v in r["oeis"].items()
                if isinstance(v, dict) and v["status"] == "NO MATCH"]
    neither = [r["spec"] for r in rows if not (r["zero_absorbing"] or r["zero_identity"])]
    return {
        "n_commutative": len(rows),
        "rows": rows,
        "zero_neither_absorbing_nor_identity": neither,
        "sequences_without_oeis_match": no_match,
        "summary": [f"{len(rows)} commutative operations; 0 neither absorbing nor identity in {len(neither)}: {neither}",
                    f"sequences without OEIS match: {len(no_match)} {no_match[:12]}"],
    }
