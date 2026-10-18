"""EXP-C05-07: linear models x*y = a x + b y over finite fields GF(q) for the open ETP laws.

Why. The Skeptic's review of C05 (reviews/skeptic_C05_C08_C12.md) refuted CLM-C05-09 with models of order 16 of
laws 677 and 1313 that are linear over GF(16). EXP-C05-05 had only tested affine models over Z_n, whose additive
group is cyclic; GF(p^k) with k > 1 was never searched. This experiment searches every prime power q <= 128.

For x*y = a x + b y, a term t(x, y) evaluates to alpha x + beta y with alpha, beta polynomials in a, b; the law
x = t holds iff alpha = 1 and beta = 0 in GF(q). Each model found is also re-checked on its full q x q table with
the generic evaluator of systems.magma.
"""

import itertools
import json

import numpy as np

from lab.paths import RESULTS
from systems.magma import parse, satisfies

from experiments.C05.E03_frontier_push import LAWS

META = {
    "id": "EXP-C05-07",
    "cycle": "C05",
    "title": "Linear models over finite fields GF(q), q <= 128, for the 15 open ETP laws",
    "agent": "Mathematical Explorer",
    "question": "For which prime powers q do the open laws of EXP-C05-03 have a linear model x*y = a x + b y over "
                "GF(q), and does this settle sizes that EXP-C05-03 left UNKNOWN or that CLM-C05-09 excluded?",
    "hypothesis": "H-C05-F: linear models over GF(p^k), k > 1, give spectrum members that the Z_n search of EXP-C05-05 "
                  "cannot see - among them even orders for laws whose small even orders are gaps.",
    "assumptions": ["GF(p^k) built as GF(p)[t]/(f) with the first monic irreducible f of degree k in "
                    "lexicographic order", "exhaustive over all (a, b) in GF(q)^2", "q <= 128"],
    "methodology": "Vectorised evaluation of (alpha, beta) for all (a, b); every model found is re-checked on its full "
                   "table; comparison with the SAT statuses of EXP-C05-03 and the certified gaps of CLM-C05-08.",
    "falsification": "A linear model at an order that EXP-C05-03 found UNSAT or that EXP-C05-06 certified as a gap "
                     "(would expose a bug); for H-C05-F, no linear model of any even order for 677 and 1313.",
}

CERTIFIED_GAPS = {501: [6, 7], 677: [6], 883: [6], 1076: [8], 1083: [5, 6]}   # CLM-C05-08


def prime_power(q):
    for p in range(2, q + 1):
        if q % p == 0:
            k, r = 0, q
            while r % p == 0:
                r //= p
                k += 1
            return (p, k) if r == 1 else None
    return None


def poly_rem(f, g, p):
    r = list(f)
    d = len(g) - 1
    for i in range(len(r) - 1, d - 1, -1):
        c = r[i]
        if c:
            for j in range(d + 1):
                r[i - d + j] = (r[i - d + j] - c * g[j]) % p
    return r[:d]


def irreducible(p, k):
    """First monic irreducible polynomial of degree k over GF(p), coefficients from low to high degree."""
    for low in itertools.product(range(p), repeat=k):
        f = list(low) + [1]
        if f[0] == 0:
            continue
        if all(any(poly_rem(f, list(g) + [1], p))
               for d in range(1, k // 2 + 1) for g in itertools.product(range(p), repeat=d)):
            return f
    raise ValueError("no irreducible polynomial")


def field_tables(q):
    p, k = prime_power(q)
    if k == 1:
        r = np.arange(q)
        return np.add.outer(r, r) % q, np.multiply.outer(r, r) % q, [0, 1]
    f = irreducible(p, k)
    digits = [[(x // p ** i) % p for i in range(k)] for x in range(q)]
    num = lambda v: sum(c * p ** i for i, c in enumerate(v))
    add = np.zeros((q, q), dtype=np.int64)
    mul = np.zeros((q, q), dtype=np.int64)
    for x in range(q):
        for y in range(q):
            add[x, y] = num([(u + v) % p for u, v in zip(digits[x], digits[y])])
            prod = [0] * (2 * k - 1)
            for i, u in enumerate(digits[x]):
                for j, v in enumerate(digits[y]):
                    prod[i + j] = (prod[i + j] + u * v) % p
            mul[x, y] = num(poly_rem(prod, f, p) + [0] * (k - len(poly_rem(prod, f, p))))
    return add, mul, f


def coefficients(t, add, mul, a, b):
    if isinstance(t, str):
        one, zero = np.ones_like(a), np.zeros_like(a)
        return (one, zero) if t == "x" else (zero, one)
    left, right = t
    al1, be1 = coefficients(left, add, mul, a, b)
    al2, be2 = coefficients(right, add, mul, a, b)
    return add[mul[a, al1], mul[b, al2]], add[mul[a, be1], mul[b, be2]]


def run():
    qs = [q for q in range(2, 129) if prime_power(q)]
    fields = {q: field_tables(q) for q in qs}
    e03 = {r["etp_number"]: r for r in json.load(open(RESULTS / "EXP-C05-03.json"))["results"]["rows"]}
    rows, conflicts, settled, tables = [], [], [], {}
    for num, (t, notes_in, notes_out, phrase) in LAWS.items():
        term = parse(t)
        law = (term, "x")
        orders, examples = [], {}
        for q in qs:
            add, mul, f = fields[q]
            a, b = (m.ravel() for m in np.meshgrid(np.arange(q), np.arange(q), indexing="ij"))
            al, be = coefficients(term, add, mul, a, b)
            hits = np.nonzero((al == 1) & (be == 0))[0]
            if len(hits) == 0:
                continue
            A, B = int(a[hits[0]]), int(b[hits[0]])
            T = add[mul[A][:, None], mul[B][None, :]]          # T[x, y] = A x + B y
            assert satisfies(T, law), (num, q)
            orders.append(q)
            examples[str(q)] = {"a": A, "b": B, "models": int(len(hits)), "modulus_poly": f}
            if (q == 16 and num in (677, 1313)) or (q == 9 and num == 670):
                tables[f"{num}@{q}"] = T.tolist()
        status = e03[num]["status_n_2_10"]
        for q in orders:
            if q <= 10 and status.get(str(q)) == "UNSAT":
                conflicts.append((num, q, "EXP-C05-03 UNSAT"))
            if q in CERTIFIED_GAPS.get(num, []):
                conflicts.append((num, q, "certified gap"))
            if q in notes_out:
                conflicts.append((num, q, "notes: not in spectrum"))
            if q <= 10 and status.get(str(q)) == "UNKNOWN":
                settled.append((num, q, "also stated in the notes" if q in notes_in else "not stated in the notes"))
        rows.append({"etp_number": num, "law": f"x = {t}", "linear_model_orders": orders, "examples": examples,
                     "even_orders": [q for q in orders if q % 2 == 0]})
    even = {r["etp_number"]: r["even_orders"][:4] for r in rows}
    return {
        "orders_tested": qs,
        "rows": rows,
        "conflicts": conflicts,
        "settled_unknowns_n_le_10": settled,
        "tables": tables,
        "summary": [
            f"{len(LAWS)} laws, {len(qs)} prime powers q <= 128; conflicts with SAT, certified gaps or the notes: "
            f"{len(conflicts)}",
            "smallest even orders with a linear model: " + "; ".join(f"{k}: {v}" for k, v in even.items()),
            "sizes n <= 10 left UNKNOWN by EXP-C05-03 and settled here: " +
            (", ".join(f"law {k} at n = {q} ({why})" for k, q, why in settled) or "none"),
            "laws 677 and 1313: linear models of orders " +
            "; ".join(f"{r['etp_number']}: {r['linear_model_orders'][:12]}" for r in rows
                      if r["etp_number"] in (677, 1313)),
        ],
    }
