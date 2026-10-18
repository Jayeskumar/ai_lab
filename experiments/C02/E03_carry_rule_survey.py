"""EXP-C02-03: survey of carry rules m[k] -> sum_j b_j [k+j]: termination, gliders, emergent bases."""

import itertools

from systems.exchange import digits_msd_first, positive_root, stabilize_carry

META = {
    "id": "EXP-C02-03",
    "cycle": "C02",
    "title": "Carry-rule survey: termination criterion, glider certificates and emergent bases",
    "agent": "Mathematical Explorer",
    "question": "Which carry rules turn unary numerals into finite normal forms, what is the emergent base, "
                "and are the resulting representations ordered like ordinary numerals?",
    "hypothesis": "H-C02-1: the rule terminates from every unary start iff sum_j b_j < m (emergent base r > 1, "
                  "r the positive root of sum_j b_j r^j = m); otherwise some start produces a periodic glider. "
                  "H-C02-2: for terminating rules, n < n' implies rep(n) < rep(n') in radix order.",
    "assumptions": ["m in {2,3,4}, b_j in {0..3}, J <= 3 (last coefficient nonzero): 189 rules",
                    "unary starts n <= 200; representations for n <= 3000"],
    "methodology": "Batch-firing upward sweep. After level k is processed the future depends only on the "
                   "window (c_{k+1}, ..., c_{k+J}), and the window map is monotone; a window W with an entry >= m "
                   "that is later dominated componentwise (periodic glider if equal) certifies infinitely many "
                   "firings. Radix order = compare length, then digits from the top.",
    "falsification": "A rule with sum b < m and an infinite derivation, a rule with sum b >= m terminating from "
                     "all n <= 200 with no glider, or a radix-order inversion.",
}


def sweep(n, m, b, max_levels=3000):
    """Return ('stable', config) or ('glider', info) or ('unknown', info)."""
    J = len(b)
    c = [n] + [0] * (J + 1)
    seen = {}
    k = 0
    while True:
        if k + J + 1 > len(c):
            c += [0] * (k + J + 1 - len(c))
        if c[k] >= m:
            t = c[k] // m
            c[k] -= t * m
            for j, bj in enumerate(b, start=1):
                c[k + j] += t * bj
        window = tuple(c[k + 1:k + 1 + J])
        if not any(window):
            return "stable", tuple(c[:k + 1])
        if all(x < m for x in window) and not any(c[k + 1 + J:]):
            # remaining levels are already stable
            out = c[:k + 1 + J]
            while out and out[-1] == 0:
                out.pop()
            return "stable", tuple(out)
        if window in seen:
            return "glider", {"window": window, "first_level": seen[window], "period": k - seen[window],
                              "kind": "periodic"}
        # monotone pumping certificate: an earlier window W with an entry >= m and W <= current window
        for w_old, k_old in seen.items():
            if max(w_old) >= m and all(a <= x for a, x in zip(w_old, window)):
                return "glider", {"window": w_old, "dominated_by": window, "first_level": k_old,
                                  "period": k - k_old, "kind": "pumping"}
        seen[window] = k
        k += 1
        if k > max_levels:
            return "unknown", {"window": window, "level": k}


def radix_less(a, b):
    return (len(a), a) < (len(b), b)


def run():
    rules = []
    for m in (2, 3, 4):
        for J in (1, 2, 3):
            for b in itertools.product(range(4), repeat=J):
                if b[-1] == 0:
                    continue
                rules.append((m, b))
    rows = []
    h1_violations, h2_violations = [], []
    for m, b in rules:
        s = sum(b)
        r = positive_root(m, b)
        outcome = {"stable": 0, "glider": 0, "unknown": 0}
        first_glider = None
        for n in range(1, 201):
            kind, info = sweep(n, m, b)
            outcome[kind] += 1
            if kind == "glider" and first_glider is None:
                first_glider = {"n": n, **info}
        terminating = outcome["stable"] == 200
        row = {"m": m, "b": list(b), "sum_b": s, "base_r": float(r), "outcome_n_1_200": outcome,
               "first_glider": first_glider}
        if (s < m) != terminating or (s >= m and first_glider is None):
            h1_violations.append(row)
        if terminating:
            reps = []
            for n in range(0, 3001):
                c, f, t = stabilize_carry((n,), m, b)
                reps.append(c)
            inv = [n for n in range(3000) if not radix_less(tuple(reversed(reps[n])), tuple(reversed(reps[n + 1])))]
            lengths = sorted({len(x) for x in reps[1:]})
            missing_lengths = [L for L in range(1, max(lengths) + 1) if L not in lengths]
            row.update({"radix_inversions": inv[:5], "n_radix_inversions": len(inv),
                        "first_reps": [digits_msd_first(x) for x in reps[:16]],
                        "lengths_never_used": missing_lengths[:20]})
            if inv:
                h2_violations.append({"m": m, "b": list(b), "first": inv[:3]})
        rows.append(row)
    term = [r for r in rows if r["outcome_n_1_200"]["stable"] == 200]
    return {
        "n_rules": len(rows),
        "rows": rows,
        "n_terminating": len(term),
        "h1_violations": h1_violations,
        "h2_violations": h2_violations,
        "summary": [
            f"{len(rows)} carry rules; {len(term)} terminate from all unary n <= 200, all with sum b < m; "
            f"H-C02-1 violations: {len(h1_violations)}",
            f"every non-terminating rule has a certificate (periodic glider or monotone pumping): "
            f"{all(r['first_glider'] is not None for r in rows if r['sum_b'] >= r['m'])}",
            f"H-C02-2 (radix monotonicity) violations among terminating rules: {len(h2_violations)}",
        ],
    }
