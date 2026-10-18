"""Skeptic checks for cycle C02 (independent re-implementations; systems/exchange.py is NOT used
except in part D2, which re-runs the lab's own survey code to test reproducibility).

Usage: python c02_checks.py [parts]   parts from A B C D E F G H (default: all)
Results: out/c02_<part>.json and a one-line summary per part on stdout.
"""
import itertools
import json
import os
import random
import sys
import time
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)


def trim(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


def save(name, obj):
    json.dump(obj, open(os.path.join(OUT, f"c02_{name}.json"), "w"), indent=1, default=str)


# ============================================================== carry-rule primitives (own code)
def fire(c, k, m, b):
    d = list(c) + [0] * max(0, k + len(b) + 1 - len(c))
    d[k] -= m
    for j, bj in enumerate(b, start=1):
        d[k + j] += bj
    return trim(d)


def successors(c, m, b):
    return [(k, fire(c, k, m, b)) for k, x in enumerate(c) if x >= m]


def layers(c0, m, b, max_depth, max_states=200_000):
    """BFS by number of firings.  For carry rules the firing vector (hence the depth) of a reachable
    state is determined by the state (triangular system), so layers are well defined."""
    layer = {trim(c0)}
    out = [layer]
    seen = set(layer)
    for _ in range(max_depth):
        nxt = set()
        for c in layer:
            for _, d in successors(c, m, b):
                nxt.add(d)
        if not nxt:
            break
        if len(seen) + len(nxt) > max_states:
            return out, True
        seen |= nxt
        out.append(nxt)
        layer = nxt
    return out, False


def outcome_set(c0, m, b):
    """Set of (endpoint, length, firing vector) over ALL maximal derivations (memoised DFS);
    only for terminating situations."""
    memo = {}
    sys.setrecursionlimit(100000)

    def go(c):
        if c in memo:
            return memo[c]
        succ = successors(c, m, b)
        if not succ:
            res = frozenset([(c, 0, ())])
        else:
            acc = set()
            for k, d in succ:
                for end, L, fv in go(d):
                    f = list(fv) + [0] * max(0, k + 1 - len(fv))
                    f[k] += 1
                    acc.add((end, L + 1, trim(f)))
            res = frozenset(acc)
        memo[c] = res
        return res

    return go(trim(c0)), len(memo)


def sweep_unary(n, m, b, max_levels=100000):
    """Own upward sweep from n tokens at level 0. Returns ('stable', config) or ('dominates_T', level)."""
    J = len(b)
    T = [sum(b[i:]) for i in range(J)]
    c = [n] + [0] * (J + 2)
    k = 0
    while k < max_levels:
        if len(c) < k + J + 2:
            c += [0] * (k + J + 2 - len(c))
        t = c[k] // m
        if t:
            c[k] -= t * m
            for j, bj in enumerate(b, start=1):
                c[k + j] += t * bj
        W = c[k + 1:k + 1 + J]
        if sum(b) == m and all(W[i] >= T[i] for i in range(J)):
            return "dominates_T", k
        if all(x < m for x in W):
            return "stable", trim(c)
        k += 1
    return "unknown", k


def reduce_rule(b):
    g = 0
    for j, bj in enumerate(b, start=1):
        if bj:
            g = gcd(g, j)
    return g, tuple(b[g * i - 1] for i in range(1, len(b) // g + 1))


# ============================================================== A: integer bases (CLM-C02-01)
def part_A():
    bad, cases, maxstates = [], 0, 0
    for base, nmax in ((2, 64), (3, 60), (4, 60), (5, 60), (6, 60), (7, 50)):
        for n in range(0, nmax + 1):
            outs, nstates = outcome_set((n,), base, (1,))
            maxstates = max(maxstates, nstates)
            digits, x = [], n
            while x:
                digits.append(x % base)
                x //= base
            expected = (trim(digits), (n - sum(digits)) // (base - 1))
            cases += 1
            ends = {(e, L) for e, L, _ in outs}
            if ends != {expected} or len({fv for _, _, fv in outs}) != 1:
                bad.append({"b": base, "n": n, "outcomes": len(outs)})
    res = {"cases": cases, "failures": bad, "largest_state_space": maxstates}
    save("A_integer_bases", res)
    return f"A (CLM-C02-01): {cases} exhaustive (all derivations) cases b=2..7, n<=64: failures {len(bad)}; " \
           f"largest state space {maxstates}"


# ============================================================== B: abelian property (CLM-C02-02)
def part_B():
    rng = random.Random(12345)
    viol, n_term, n_open, tested = [], 0, 0, 0
    for _ in range(1500):
        m = rng.randint(1, 5)
        J = rng.randint(1, 3)
        b = [rng.randint(0, 4) for _ in range(J)]
        if b[-1] == 0:
            b[-1] = 1
        c0 = trim([rng.randint(0, 3 * m + 2) for _ in range(rng.randint(1, 4))])
        lay, capped = layers(c0, m, tuple(b), max_depth=40, max_states=4_000)
        tested += 1
        sinks = [(d, c) for d, L in enumerate(lay) for c in L if not successors(c, m, tuple(b))]
        if sinks:
            n_term += 1
            depths = {d for d, _ in sinks}
            Ld = max(depths)
            # theorem: unique sink, it is the whole last layer, and no other layer contains a sink
            if len(sinks) != 1 or lay[Ld] != {sinks[0][1]} or len(lay) != Ld + 1:
                viol.append({"m": m, "b": b, "c0": c0, "sinks": len(sinks)})
        else:
            n_open += 1
    # firing-vector uniqueness on terminating random cases (B < m), all derivations enumerated
    fv_bad, fv_tested = [], 0
    for _ in range(400):
        m = rng.randint(2, 5)
        J = rng.randint(1, 3)
        while True:
            b = [rng.randint(0, m - 1) for _ in range(J)]
            if b[-1] and sum(b) < m:
                break
        c0 = trim([rng.randint(0, 3 * m) for _ in range(rng.randint(1, 3))])
        outs, _ = outcome_set(c0, m, tuple(b))
        fv_tested += 1
        if len(outs) != 1:
            fv_bad.append({"m": m, "b": b, "c0": c0, "outcomes": len(outs)})
    res = {"random_cases": tested, "reached_a_sink": n_term, "no_sink_within_cap": n_open,
           "violations": viol, "firing_vector_cases": fv_tested, "firing_vector_violations": fv_bad}
    save("B_abelian", res)
    return f"B (CLM-C02-02): {tested} random rules/configs (m=1..5, any B, non-unary starts): " \
           f"{n_term} terminating, violations of uniqueness/equal length {len(viol)}; " \
           f"{fv_tested} B<m cases with all derivations enumerated: non-unique (end,length,firing vector) {len(fv_bad)}"


# ============================================================== C/D helpers: rigorous root bounds
def root_bracket(m, b, iters=80):
    """Fractions lo < r < hi for the positive root of sum b_j x^j = m."""
    f = lambda x: sum(bj * x ** j for j, bj in enumerate(b, start=1)) - m
    lo, hi = Fraction(0), Fraction(1)
    while f(hi) <= 0:
        if f(hi) == 0:
            return hi, hi
        hi *= 2
    for _ in range(iters):
        mid = (lo + hi) / 2
        v = f(mid)
        if v == 0:
            return mid, mid
        if v < 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


SURVEY = [(m, b) for m in (2, 3, 4) for J in (1, 2, 3) for b in itertools.product(range(4), repeat=J)
          if b[-1] != 0]


def part_C():
    """Termination dichotomy (CLM-C02-03): consistency of the B > m threshold with sweeps."""
    rows, bad = [], []
    for m, b in SURVEY:
        B = sum(b)
        if B <= m:
            continue
        lo, hi = root_bracket(m, b)
        assert hi < 1
        thr = (m - 1) / (1 - hi)            # >= (m-1)/(1-r)
        nstar = int(thr) + 1
        # no unary start n >= n* may stabilise; record the largest stabilising n below
        last_stable = 0
        for n in range(1, nstar + 30):
            kind, _ = sweep_unary(n, m, b, max_levels=600)
            if kind == "stable":
                last_stable = n
                if n >= nstar:
                    bad.append({"m": m, "b": b, "n": n})
        rows.append({"m": m, "b": list(b), "r_upper": float(hi), "n_star": nstar, "largest_stabilising_n": last_stable})
    # (a): random B < m configurations: derivation length = (tokens_in - tokens_out)/(m - B)
    rng = random.Random(7)
    a_bad = 0
    for _ in range(500):
        m = rng.randint(2, 6)
        J = rng.randint(1, 3)
        while True:
            b = [rng.randint(0, m - 1) for _ in range(J)]
            if b[-1] and sum(b) < m:
                break
        c0 = trim([rng.randint(0, 14) for _ in range(rng.randint(1, 3))])
        outs, _ = outcome_set(c0, m, tuple(b))
        for end, L, _ in outs:
            if L * (m - sum(b)) != sum(c0) - sum(end):
                a_bad += 1
    res = {"rules_B_gt_m": len(rows), "violations_b": bad, "rows": rows, "violations_a": a_bad}
    save("C_dichotomy", res)
    return f"C (CLM-C02-03): {len(rows)} surveyed rules with B>m: a unary start n >= n* that stabilises: " \
           f"{len(bad)} (max n* = {max(r['n_star'] for r in rows)}); 500 random B<m cases: length != " \
           f"token loss/(m-B): {a_bad}"


# ============================================================== D: CLM-C02-05 certificates
def part_D():
    rows, fails = [], []
    for m, b in SURVEY:
        B = sum(b)
        if B < m:
            rows.append({"m": m, "b": list(b), "cert": "Thm3(a)"})
            continue
        if B > m:
            lo, hi = root_bracket(m, b)
            nstar = int((m - 1) / (1 - hi)) + 1
            rows.append({"m": m, "b": list(b), "cert": "Thm3(b)", "n": nstar})
            if nstar > 200:
                fails.append(rows[-1])
            continue
        g, bred = reduce_rule(b)
        found = None
        for t in range(1, 201):
            kind, lev = sweep_unary(t * m, m, bred)
            if kind == "dominates_T":
                found = t * m
                break
        rows.append({"m": m, "b": list(b), "g": g, "reduced_b": list(bred), "cert": "Lemma4 window>=T",
                     "n": found})
        if found is None or found > 200:
            fails.append(rows[-1])
    nB = {"<": sum(sum(b) < m for m, b in SURVEY), "=": sum(sum(b) == m for m, b in SURVEY),
          ">": sum(sum(b) > m for m, b in SURVEY)}
    # D2: reproducibility of the stored EXP-C02-03 (code-hash mismatch) by re-running the lab's code
    sys.path.insert(0, "/home/user/ai_lab")
    from experiments.C02 import E03_carry_rule_survey as E03
    fresh = E03.run()
    stored = json.load(open("/home/user/ai_lab/results/EXP-C02-03.json"))["results"]
    same_rows = json.loads(json.dumps(fresh["rows"])) == stored["rows"]
    res = {"counts_by_sign_of_B_minus_m": nB, "certificate_failures": fails, "rows": rows,
           "rerun_lab_E03_rows_identical_to_stored_json": same_rows,
           "rerun_summary": fresh["summary"], "stored_summary": stored["summary"],
           "max_certificate_n": max(r.get("n") or 0 for r in rows)}
    save("D_certificates", res)
    return f"D (CLM-C02-05): rules by sign(B-m) {nB}; independent certificates found for all " \
           f"{nB['='] + nB['>']} non-terminating rules with n<=200: {not fails} (max n used " \
           f"{res['max_certificate_n']}); lab E03 re-run reproduces stored rows: {same_rows}"


# ============================================================== E: uniqueness (CLM-C02-07)
def part_E():
    import mpmath as mp
    import sympy as sp
    mp.mp.dps = 60
    y = sp.Symbol("y")

    def analyse(m, b, Lcap=200_000):
        g, bred = reduce_rule(b)
        Pt = sp.Poly(sum(bi * y ** (i + 1) for i, bi in enumerate(bred)) - m, y)
        content = gcd(m, *bred)
        facs = sp.factor_list(Pt.as_expr())[1]
        irreducible = len(facs) == 1 and facs[0][1] == 1
        # rho = r^g is the positive root of P~ ; find the factor vanishing at rho
        lo, hi = root_bracket(m, bred, iters=200)
        rho = mp.mpf(lo.numerator) / lo.denominator
        mpoly = None
        for f, _ in facs:
            fp = sp.Poly(f, y)
            if abs(mp.polyval([mp.mpf(int(cf)) for cf in fp.all_coeffs()], rho)) < mp.mpf(10) ** -40:
                mpoly = fp
        L = 1
        while m ** (L + 1) <= Lcap:
            L += 1
        # float64 pre-screen (tolerance far above rounding error, so no true collision is missed),
        # then EXACT confirmation: Delta(y) must be divisible by the minimal polynomial of rho
        import numpy as np
        rho_f = float(rho)
        digs = np.array(list(itertools.product(range(m), repeat=L)), dtype=np.int64)
        vals = digs @ np.array([rho_f ** i for i in range(L)])
        order = np.argsort(vals, kind="stable")
        sv = vals[order]
        cand = np.nonzero(np.diff(sv) <= 1e-9 * np.maximum(1.0, np.abs(sv[1:])))[0]
        coll, example, checked = 0, None, 0
        for i in cand:
            if coll >= 25:          # enough exact confirmations for a non-unique rule
                break
            d1, d2 = digs[order[i]], digs[order[i + 1]]
            delta = sp.Poly(sum(int(a - c) * y ** j for j, (a, c) in enumerate(zip(d1, d2))), y)
            checked += 1
            if delta.rem(mpoly).is_zero:
                coll += 1
                if example is None:
                    example = [trim(d1.tolist()), trim(d2.tolist())]
        return {"m": m, "b": list(b), "g": g, "P_tilde": str(Pt.as_expr()), "content": content,
                "primitive": content == 1, "irreducible": irreducible, "levels_on_gN": L,
                "exact_collisions": coll, "float_candidates": int(len(cand)), "example": example}

    rows = []
    for m in range(2, 8):
        for J in (1, 2, 3, 4):
            for b in itertools.product(range(m), repeat=J):
                if b[-1] == 0 or sum(b) >= m:
                    continue
                if m >= 6 and J == 4:
                    continue
                rows.append(analyse(m, b, Lcap=200_000))
    pi = [r for r in rows if r["primitive"] and r["irreducible"]]
    npr = [r for r in rows if not r["primitive"]]
    pred = [r for r in rows if r["primitive"] and not r["irreducible"]]
    viol_thm = [r for r in pi if r["exact_collisions"]]
    viol_conv = [r for r in npr if not r["exact_collisions"]]
    # converse outside B < m: non-primitive, B > m, no collision
    extra = [analyse(2, (4,)), analyse(2, (0, 4)), analyse(3, (6,)), analyse(2, (3,)), analyse(2, (1, 2))]
    res = {"rules_B_lt_m": len(rows), "primitive_irreducible": len(pi), "non_primitive": len(npr),
           "primitive_reducible": [(r["m"], r["b"], r["P_tilde"], r["exact_collisions"]) for r in pred],
           "theorem_violations": viol_thm, "converse_violations_B_lt_m": viol_conv,
           "outside_B_lt_m": extra}
    save("E_uniqueness", res)
    return f"E (CLM-C02-07): {len(rows)} rules with B<m, m<=7: primitive+irreducible {len(pi)} " \
           f"(collisions: {len(viol_thm)} rules), non-primitive {len(npr)} (without collision: {len(viol_conv)}), " \
           f"primitive reducible {len(pred)} (with collisions: {sum(1 for r in pred if r['exact_collisions'])}); " \
           f"B>m non-primitive (2;4),(2;0,4),(3;6) collisions: " \
           f"{[e['exact_collisions'] for e in extra[:3]]}"


# ============================================================== F: radix order (CLM-C02-08)
def part_F():
    def add_token_and_stabilise(c, m, b):
        """Add one token at level 0 and stabilise with a LIFO stack of unstable levels
        (a different firing order from the upward sweep)."""
        c = list(c) + [0] * (len(b) + 2)
        c[0] += 1
        stack = [0]
        while stack:
            k = stack.pop()
            if c[k] < m:
                continue
            t = c[k] // m
            c[k] -= t * m
            if len(c) < k + len(b) + 2:
                c += [0] * (k + len(b) + 2 - len(c))
            for j, bj in enumerate(b, start=1):
                if bj:
                    c[k + j] += t * bj
                    if c[k + j] >= m:
                        stack.append(k + j)
        return trim(c)

    rules, inv, cross_bad = 0, [], 0
    for m in range(2, 9):
        for J in (1, 2, 3, 4):
            for b in itertools.product(range(m), repeat=J):
                if b[-1] == 0 or sum(b) >= m:
                    continue
                if m >= 7 and J == 4:
                    continue
                rules += 1
                c = ()
                prev = c
                for n in range(1, 1501):
                    c = add_token_and_stabilise(c, m, b)
                    a, d = tuple(reversed(prev)), tuple(reversed(c))
                    if not ((len(a), a) < (len(d), d)):
                        inv.append({"m": m, "b": b, "n": n})
                        break
                    prev = c
                if sweep_unary(1500, m, b)[1] != c:
                    cross_bad += 1
    res = {"rules": rules, "inversions": inv, "sweep_vs_incremental_mismatch": cross_bad}
    save("F_radix", res)
    return f"F (CLM-C02-08): {rules} rules with B<m (m<=8, J<=4), n<=1500, LIFO stabilisation: " \
           f"radix inversions {len(inv)}; incremental vs sweep rep(1500) mismatches {cross_bad}"


# ============================================================== G, H: Fibonacci exchange system
def fib_w(n):
    w = [1, 2]
    while len(w) < n:
        w.append(w[-1] + w[-2])
    return w[:n]


def fib_succ(c):
    c = list(c)
    out = []
    n = len(c)
    for k in range(n):
        if c[k] >= 1 and k + 1 < n and c[k + 1] >= 1:          # [k]+[k+1] -> [k+2]
            d = c + [0] * max(0, k + 3 - n)
            d[k] -= 1; d[k + 1] -= 1; d[k + 2] += 1
            out.append(trim(d))
        if c[k] >= 2:
            d = c + [0] * max(0, k + 2 - n)
            if k >= 2:                                          # 2[k] -> [k+1]+[k-2]
                d[k] -= 2; d[k + 1] += 1; d[k - 2] += 1
            elif k == 1:                                        # 2[1] -> [2]+[0]
                d[1] -= 2; d[2] += 1; d[0] += 1
            else:                                               # 2[0] -> [1]
                d[0] -= 2; d[1] += 1
            out.append(trim(d))
    return out


def zeck(n):
    w = fib_w(40)
    c = [0] * 40
    for k in range(39, -1, -1):
        if w[k] <= n:
            c[k] = 1
            n -= w[k]
    return trim(c)


def part_G():
    w = fib_w(40)
    V = 34
    # all configurations of value <= V
    configs = []

    def rec(k, rem, cur):
        if k < 0:
            configs.append(trim(cur))
            return
        for x in range(rem // w[k] + 1):
            cur[k] = x
            rec(k - 1, rem - x * w[k], cur)
        cur[k] = 0

    K = max(i for i in range(40) if w[i] <= V) + 1
    rec(K - 1, V, [0] * K)
    val = lambda c: sum(x * w[i] for i, x in enumerate(c))
    # global DFS with colours: cycle detection + set of reachable sinks
    colour, sinks = {}, {}
    sys.setrecursionlimit(100000)
    cyc = []

    def dfs(c):
        colour[c] = 1
        s = set()
        succ = fib_succ(c)
        if not succ:
            s.add(c)
        for d in succ:
            if colour.get(d) == 1:
                cyc.append(d)
                continue
            if d not in colour:
                dfs(d)
            s |= sinks[d]
        colour[c] = 2
        sinks[c] = frozenset(s)

    for c in configs:
        if c not in colour:
            dfs(c)
    bad = [c for c in configs if sinks[c] != {zeck(val(c))}]
    # shortest derivation from unary n = n - z(n): BFS
    sh_bad = []
    for n in range(0, 61):
        start = (n,) if n else ()
        dist = {start: 0}
        frontier = [start]
        best = None
        while frontier and best is None:
            nxt = []
            for c in frontier:
                succ = fib_succ(c)
                if not succ:
                    best = dist[c]
                    break
                for d in succ:
                    if d not in dist:
                        dist[d] = dist[c] + 1
                        nxt.append(d)
            frontier = nxt
        if best != n - sum(zeck(n)):
            sh_bad.append((n, best))
    res = {"configurations_value_le": V, "n_configurations": len(configs), "states_explored": len(colour),
           "cycles": len(cyc), "wrong_sinks": [list(c) for c in bad[:5]], "n_wrong": len(bad),
           "shortest_mismatch_n_le_60": sh_bad}
    save("G_fibonacci", res)
    return f"G (CLM-C02-09): all {len(configs)} configurations of value <= {V} ({len(colour)} states): cycles " \
           f"{len(cyc)}, non-Zeckendorf or multiple sinks {len(bad)}; shortest derivation != n - z(n) for n<=60: " \
           f"{len(sh_bad)}"


def part_H(NMAX=60):
    memo = {}
    sys.setrecursionlimit(100000)

    def longest(c):
        if c in memo:
            return memo[c]
        succ = fib_succ(c)
        r = 0 if not succ else 1 + max(longest(d) for d in succ)
        memo[c] = r
        return r

    seq = [longest((n,) if n else ()) for n in range(0, NMAX + 1)]
    claimed = [0, 1, 2, 3, 5, 6, 8, 10, 11, 13, 15, 17, 20, 21, 23, 25, 26, 29, 31, 34, 37, 38, 40, 42, 44,
               47, 48, 50, 53, 54, 57, 60, 63, 67, 68, 70, 72, 73, 76, 78]
    ok = seq[1:41] == claimed
    res = {"max_len_n_0_to_%d" % NMAX: seq, "claim_matches_n_1_40": ok, "states_memoised": len(memo)}
    save("H_longest", res)
    return f"H (CLM-C02-10): longest derivation (memoised DFS, own rules) n=1..40 equals the claimed list: {ok}; " \
           f"extension n=41..{NMAX}: {seq[41:]}"


PARTS = {"A": part_A, "B": part_B, "C": part_C, "D": part_D, "E": part_E, "F": part_F, "G": part_G, "H": part_H}

if __name__ == "__main__":
    which = sys.argv[1:] or list(PARTS)
    for p in which:
        t0 = time.time()
        msg = PARTS[p]()
        print(msg, f"[{time.time() - t0:.1f} s]", flush=True)
