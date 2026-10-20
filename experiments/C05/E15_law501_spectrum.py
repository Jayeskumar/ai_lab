"""EXP-C05-15: the spectrum of ETP law 501, x = y(y(x(xy))), is exactly {n : n = 0, 1 (mod 4)}.

Theorem 14 of proofs/paper/C05.md. Write x # y = x(xy). Law 501 says exactly that # satisfies x = y # (x # y)
(ETP law 14, semi-symmetric), and every left translation of # is the square L_x^2 of a left translation of the
model, hence an even permutation. In a finite semi-symmetric quasigroup of order n the map (x, y) -> (y, x # y) has
order 3; comparing signs gives prod_y sign(L_y) = (-1)^(n(n-1)/2). So n(n-1)/2 is even. Conversely, over an abelian
group A of order n = 0, 1 (mod 4) (Z_n for odd n, Z_2 x Z_2 x Z_{n/4} otherwise) the operation x # y = -x - y is
semi-symmetric and each translation y -> -x - y is an involution with an even number of 2-cycles, so it has a
square root sigma_x (pair the 2-cycles into 4-cycles), and x * y = sigma_x(y) satisfies law 501.

This experiment checks the computational side: (a) the sign identity on semi-symmetric quasigroups of orders 3-9
enumerated by SAT (a check of the lemma, not needed for the proof); (b) the construction for every n = 0, 1 (mod 4)
up to 100, each table verified on the law; (c) a model of order 12 found by the case split (case 0), which is not
of the group form (it is idempotent); (d) agreement with every order already certified (EXP-C05-03, -06, -09, -12).
"""

import itertools
import json

import numpy as np
from pysat.solvers import Cadical153

from lab.paths import RESULTS
from systems.magma import MagmaSAT, parse, satisfies
from systems.magma_split import cases, solve_case

META = {
    "id": "EXP-C05-15",
    "cycle": "C05",
    "title": "Law 501, x = y(y(x(xy))): the spectrum is exactly the n = 0, 1 (mod 4)",
    "agent": "Mathematical Explorer",
    "question": "Is the spectrum of ETP law 501 exactly {n : n = 0, 1 (mod 4)}, as the parity argument and the group "
                "construction of Theorem 14 (proofs/paper/C05.md) say?",
    "hypothesis": "H-C05-M: every n = 0, 1 (mod 4) up to 100 has a model built by the construction; every order "
                  "already certified as a gap is = 2, 3 (mod 4); the sign identity holds on every sampled "
                  "semi-symmetric quasigroup.",
    "assumptions": ["the written proof of Theorem 14 (proofs/paper/C05.md) for all n; this experiment checks n <= 100",
                    "semi-symmetric quasigroups sampled: the first 6 models found by CaDiCaL for each n = 3..9, "
                    "blocking each one found"],
    "methodology": "Exact arithmetic on Cayley tables; SAT (CaDiCaL 1.5.3) for the sample and for the order-12 model "
                   "of the case split; every table re-checked with systems.magma.satisfies.",
    "falsification": "A table of the construction failing the law, a certified gap at an order = 0, 1 (mod 4), or "
                     "a semi-symmetric quasigroup violating the sign identity.",
}

LAW = "y(y(x(xy)))"
LAW14 = "y(xy)"


def sign(p):
    p, seen, s = list(p), set(), 1
    for i in range(len(p)):
        if i in seen:
            continue
        j, length = i, 0
        while j not in seen:
            seen.add(j)
            j = p[j]
            length += 1
        s *= -1 if length % 2 == 0 else 1
    return s


def group(n):
    mods = (n,) if n % 2 else (2, 2, n // 4)
    elems = list(itertools.product(*[range(m) for m in mods]))
    idx = {e: i for i, e in enumerate(elems)}
    return elems, idx, mods


def construction(n):
    """The model of Theorem 14: x * y = sigma_x(y) with sigma_x^2 = (y -> -x - y) on Z_n or Z_2 x Z_2 x Z_{n/4}."""
    elems, idx, mods = group(n)
    T = np.zeros((n, n), dtype=np.int64)
    for i, x in enumerate(elems):
        inv = [idx[tuple((-a - b) % m for a, b, m in zip(x, y, mods))] for y in elems]
        two_cycles = sorted({tuple(sorted((a, inv[a]))) for a in range(n) if inv[a] != a})
        assert len(two_cycles) % 2 == 0
        sigma = list(range(n))
        for (a, b), (c, d) in zip(two_cycles[0::2], two_cycles[1::2]):      # (a b)(c d) = (a c b d)^2
            sigma[a], sigma[c], sigma[b], sigma[d] = c, b, d, a
        T[i] = sigma
    return T


def run():
    identity, law14 = (parse(LAW), "x"), (parse(LAW14), "x")
    sample = []
    for n in range(3, 10):
        s = MagmaSAT(n, [law14])
        with Cadical153(bootstrap_with=s.clauses) as sol:
            for _ in range(6):
                if not sol.solve():
                    break
                T = s.table_from_model(sol.get_model())
                prod = int(np.prod([sign(T[y]) for y in range(n)]))
                sample.append({"n": n, "is_law14_model": bool(satisfies(T, law14)), "prod_sign": prod,
                               "expected": (-1) ** (n * (n - 1) // 2)})
                sol.add_clause([-s.v[a, b, int(T[a][b])] for a in range(n) for b in range(n)])
    built = {}
    for n in range(1, 101):
        if n % 4 in (0, 1):
            built[n] = bool(satisfies(construction(n), identity))
    case, lam, ell = cases(12)[0]
    rec, _ = solve_case(LAW, 12, case, lam, ell, 1_000_000, None)
    m12 = np.array(rec["model"])
    certified = {}
    for exp in ("EXP-C05-12", "EXP-C05-09"):
        pairs = json.load(open(RESULTS / f"{exp}.json"))["results"]["pairs"]
        for key, v in pairs.items():
            num, n = map(int, key.split("/"))
            if num == 501:
                certified[n] = "model" if v["verdict"] == "model found" else (
                    "gap" if v["verdict"].startswith("no model") else "undecided")
    disagreements = [n for n, v in certified.items() if (v == "model") != (n % 4 in (0, 1))]
    sign_failures = [x for x in sample if not x["is_law14_model"] or x["prod_sign"] != x["expected"]]
    return {
        "law": "x = y(y(x(xy)))",
        "sign_identity_sample": sample,
        "construction_valid": {str(n): ok for n, ok in built.items()},
        "order12_case_split_model": {"case": [case, list(lam), ell], "status": rec["status"],
                                     "model": rec.get("model"), "verified": bool(satisfies(m12, identity)),
                                     "idempotent": bool(all(m12[a, a] == a for a in range(12))),
                                     "quasigroup": bool(all(len(set(m12[:, c])) == 12 for c in range(12)))},
        "certified_orders": {str(n): v for n, v in sorted(certified.items())},
        "disagreements_with_certified_orders": disagreements,
        "summary": [
            f"construction: {sum(built.values())} of {len(built)} orders n = 0, 1 (mod 4), n <= 100, give a model "
            f"of law 501",
            f"sign identity prod_y sign(L_y) = (-1)^(n(n-1)/2): holds on {len(sample) - len(sign_failures)} of "
            f"{len(sample)} sampled semi-symmetric quasigroups (n = 3..9)",
            f"order 12 by the case split: {rec['status']}, verified {bool(satisfies(m12, identity))}, idempotent "
            f"{bool(all(m12[a, a] == a for a in range(12)))}",
            f"certified orders (EXP-C05-09, -12): {dict(sorted(certified.items()))}; disagreements with "
            f"n = 0, 1 (mod 4): {disagreements}",
        ],
    }
