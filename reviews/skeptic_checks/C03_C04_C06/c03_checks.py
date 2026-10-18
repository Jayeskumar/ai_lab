"""Skeptic checks for cycle C03 (0^p 1^q -> 1^r 0^s).  Own code only: nothing from systems/ or lab/.

Usage:  python3 c03_checks.py <part>   (parts: certs, search, open, matrices, obs11, zantema, conserving, all)
Outputs JSON to out/c03_<part>.json.
"""
import itertools
import json
import random
import sys
import time
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def rule(p, q, r, s):
    return "0" * p + "1" * q, "1" * r + "0" * s


def replay(lhs, rhs, start, positions):
    """Apply the rewrite steps at the given positions; raise if a position is not a redex."""
    w = start
    for pos in positions:
        if pos < 0 or w[pos:pos + len(lhs)] != lhs:
            raise ValueError(f"position {pos} is not a redex")
        w = w[:pos] + rhs + w[pos + len(lhs):]
    return w


def is_loop(lhs, rhs, start, positions):
    """True iff start ->+ w (len(positions) >= 1) and start is a factor of w."""
    if not positions:
        return False
    try:
        w = replay(lhs, rhs, start, positions)
    except ValueError:
        return False
    return start in w


def phi(w):
    """complement(reverse(w))"""
    return w[::-1].translate(str.maketrans("01", "10"))


def mirror_cert(p, q, r, s, start, positions):
    """Loop of (p,q,r,s) -> loop of (q,p,s,r) along phi; positions recomputed from the replayed words."""
    lhs, rhs = rule(p, q, r, s)
    k = len(lhs)
    w = start
    new_pos = []
    for pos in positions:
        new_pos.append(len(w) - pos - k)
        w = w[:pos] + rhs + w[pos + k:]
    return phi(start), new_pos


def predicted_H4(p, q, r, s):
    nt = (r >= 2 * q and s >= 2 * p) or (s >= 2 * p and q < r < 2 * q and s % p == 0) or \
         (r >= 2 * q and p < s < 2 * p and r % q == 0)
    return "NON-TERMINATING" if nt else "TERMINATING"


# ---------------------------------------------------------------- part: certs
def part_certs():
    """Re-verify every stored loop certificate with own replay; build the 5 mirror certificates."""
    res = {}
    e1 = json.load(open(ROOT / "results/EXP-C03-01.json"))["results"]
    ok1 = bad1 = 0
    for row in e1["rows"]:
        if row["status"] == "NON-TERMINATING":
            c = row["certificate"]
            l, rr = rule(*row["rule"])
            good = is_loop(l, rr, c["start"], c["steps"]) and replay(l, rr, c["start"], c["steps"]) == c["end"]
            ok1 += good
            bad1 += not good
    res["EXP-C03-01"] = {"loops_verified": ok1, "loops_failed": bad1,
                         "matrix_certs": sum(r["certificate"]["kind"] == "matrix" for r in e1["rows"])}
    e2 = json.load(open(ROOT / "results/EXP-C03-02.json"))["results"]
    st2 = {tuple(r["rule"]): r for r in e2["rows"]}
    ok2, bad2, maxsteps = [], [], 0
    for k, row in st2.items():
        if row["status"] == "NON-TERMINATING":
            c = row["certificate"]
            l, rr = rule(*k)
            if is_loop(l, rr, c["start"], c["steps"]) and len(replay(l, rr, c["start"], c["steps"])) == c["end_length"]:
                ok2.append(list(k))
                maxsteps = max(maxsteps, len(c["steps"]))
            else:
                bad2.append(list(k))
    e3 = json.load(open(ROOT / "results/EXP-C03-03.json"))["results"]
    mirrored_ok, mirrored_bad = [], []
    for key, how in e3["unknowns_resolved_as_looping"].items():
        k = tuple(json.loads(key))
        p, q, r, s = k
        m = (q, p, s, r)
        c = st2[m]["certificate"]
        start, pos = mirror_cert(*m, c["start"], c["steps"])
        l, rr = rule(*k)
        (mirrored_ok if is_loop(l, rr, start, pos) else mirrored_bad).append([list(k), how])
    nonterm = sorted(set(map(tuple, ok2)) | {tuple(x[0]) for x in mirrored_ok})
    unknown = sorted(k for k, row in st2.items() if row["status"] == "UNKNOWN" and k not in nonterm)
    # consistency of the claimed classification
    allrules = list(itertools.product(range(1, 6), repeat=4))
    easy = [k for k in allrules if k[3] <= k[0] or k[2] <= k[1]]
    growing = [k for k in allrules if not (k[3] <= k[0] or k[2] <= k[1])]
    pred_nt = sorted(k for k in growing if predicted_H4(*k) == "NON-TERMINATING")
    res["EXP-C03-02"] = {"loops_verified": len(ok2), "loops_failed": bad2, "longest_loop_steps": maxsteps,
                         "symmetry_violations_in_stored_statuses": sum(
                             1 for k, row in st2.items() if row["status"] != st2[(k[1], k[0], k[3], k[2])]["status"])}
    res["EXP-C03-03_mirrors"] = {"verified": mirrored_ok, "failed": mirrored_bad}
    res["classification"] = {
        "rules": len(allrules), "s<=p or r<=q": len(easy), "both_growing": len(growing),
        "verified_nonterminating": len(nonterm), "remaining_unknown": len(unknown),
        "nonterminating_equals_H4_prediction": [list(x) for x in nonterm] == [list(x) for x in pred_nt],
        "unknown_all_predicted_terminating": all(predicted_H4(*k) == "TERMINATING" for k in unknown),
        "unknown": [list(k) for k in unknown],
        "H-C03-2_counterexamples_among_all_76": sum(1 for k in nonterm if (k[2] < 2 * k[1] or k[3] < 2 * k[0])),
    }
    return res


# ---------------------------------------------------------------- loop search (own)
def strategy_run(lhs, rhs, u, strategy, max_steps, max_len, rng=None):
    """Run a deterministic (or seeded random) strategy from u; return positions if u reappears as a factor."""
    w, pos = u, []
    for _ in range(max_steps):
        if strategy == "rightmost":
            i = w.rfind(lhs)
        elif strategy == "leftmost":
            i = w.find(lhs)
        else:  # random redex
            occ, j = [], w.find(lhs)
            while j >= 0:
                occ.append(j)
                j = w.find(lhs, j + 1)
            i = rng.choice(occ) if occ else -1
        if i < 0:
            return None, "normal form"
        w = w[:i] + rhs + w[i + len(lhs):]
        pos.append(i)
        if u in w:
            return pos, "loop"
        if len(w) > max_len:
            return None, "too long"
    return None, "step limit"


def own_loop_search(p, q, r, s, max_steps=4000, max_len=60000, amax=None, bmax=None, random_tries=0):
    lhs, rhs = rule(p, q, r, s)
    amax = amax or 3 * p
    bmax = bmax or max(5 * q * q, 12)
    starts = sorted(((a, b) for a in range(p, amax + 1) for b in range(q, bmax + 1)), key=lambda t: (t[0] + t[1], t))
    rng = random.Random(12345)
    for a, b in starts:
        u = "0" * a + "1" * b
        for strat in ("leftmost", "rightmost"):
            pos, why = strategy_run(lhs, rhs, u, strat, max_steps, max_len)
            if pos is not None:
                return {"start": u, "positions": pos, "strategy": strat}
        for t in range(random_tries):
            pos, why = strategy_run(lhs, rhs, u, "random", max_steps, max_len, rng)
            if pos is not None:
                return {"start": u, "positions": pos, "strategy": "random"}
    return None


def lift(cert, p, q, r, k):
    """loop of (1,q,r,k) -> loop of (p,q,r,kp) along 0 -> 0^p (own implementation)."""
    lhs, rhs = rule(1, q, r, k)
    w = cert["start"]
    new = []
    for pos in cert["positions"]:
        new.append(w[:pos].count("0") * p + w[:pos].count("1"))
        w = w[:pos] + rhs + w[pos + len(lhs):]
    return {"start": cert["start"].replace("0", "0" * p), "positions": new}


def part_search():
    """Own search for loops of all 100 both-growing rules with parameters <= 5 (direct, or via own lift/mirror)."""
    t0 = time.time()
    found, missing = {}, []
    growing = [k for k in itertools.product(range(1, 6), repeat=4) if k[3] > k[0] and k[2] > k[1]]
    for k in growing:
        if predicted_H4(*k) == "TERMINATING":
            continue
        c = own_loop_search(*k)
        how = "direct"
        if c is None:
            p, q, r, s = k
            # try mirror image (search the mirror rule directly)
            cm = own_loop_search(q, p, s, r)
            if cm is not None:
                st, pos = mirror_cert(q, p, s, r, cm["start"], cm["positions"])
                c, how = {"start": st, "positions": pos}, "mirror of own loop"
        if c is None and k[3] % k[0] == 0 and k[0] > 1:
            p, q, r, s = k
            cb = own_loop_search(1, q, r, s // p)
            if cb is not None:
                c, how = lift(cb, p, q, r, s // p), "lift of own base loop"
        if c is not None and is_loop(*rule(*k), c["start"], c["positions"]):
            found[str(list(k))] = {"how": how, "start": c["start"], "steps": len(c["positions"])}
        else:
            missing.append(list(k))
    return {"predicted_nonterminating": len(found) + len(missing), "loops_found_and_verified": len(found),
            "missing": missing, "max_steps": max(v["steps"] for v in found.values()),
            "by_how": {h: sum(v["how"] == h for v in found.values()) for h in {v["how"] for v in found.values()}},
            "found": found, "seconds": round(time.time() - t0, 1)}


# ---------------------------------------------------------------- part: open (24 rules predicted terminating)
def reachable_count(word, lhs, rhs, limit):
    seen = {word}
    dq = deque([word])
    while dq:
        w = dq.popleft()
        i = w.find(lhs)
        while i >= 0:
            v = w[:i] + rhs + w[i + len(lhs):]
            if v not in seen:
                seen.add(v)
                if len(seen) > limit:
                    return None
                dq.append(v)
            i = w.find(lhs, i + 1)
    return len(seen)


def part_open():
    """Harder loop search on the rules predicted terminating, plus finiteness of reachable sets."""
    t0 = time.time()
    growing = [k for k in itertools.product(range(1, 6), repeat=4) if k[3] > k[0] and k[2] > k[1]]
    opens = [k for k in growing if predicted_H4(*k) == "TERMINATING"]
    out = {}
    for k in opens:
        p, q, r, s = k
        lhs, rhs = rule(*k)
        c = own_loop_search(*k, max_steps=4000, max_len=60000, amax=3 * p, bmax=4 * q + 6, random_tries=1)
        # rightmost/leftmost outcome from 0^a 1^b: does the strategy reach a normal form?
        nf = 0
        tot = 0
        for a in range(p, 3 * p + 1):
            for b in range(q, 3 * q + 3):
                for strat in ("leftmost", "rightmost"):
                    pos, why = strategy_run(lhs, rhs, "0" * a + "1" * b, strat, 50000, 10 ** 6)
                    tot += 1
                    nf += why == "normal form"
        # finite reachable sets from all words of length <= 10 containing lhs (no length cap; count limit)
        fin = inf = 0
        biggest = 0
        for n in range(len(lhs), 11):
            for t in itertools.product("01", repeat=n):
                w = "".join(t)
                if lhs not in w:
                    continue
                c2 = reachable_count(w, lhs, rhs, 300000)
                if c2 is None:
                    inf += 1
                else:
                    fin += 1
                    biggest = max(biggest, c2)
        out[str(list(k))] = {"loop_found": c is not None, "loop": c and {"start": c["start"], "steps": len(c["positions"])},
                             "strategy_runs_reaching_normal_form": f"{nf}/{tot}",
                             "words_len_le_10_finite_reachable": fin, "over_limit": inf,
                             "largest_reachable_set": biggest}
        print(k, out[str(list(k))], flush=True)
    return {"rules": len(opens), "any_loop_found": any(v["loop_found"] for v in out.values()), "detail": out,
            "seconds": round(time.time() - t0, 1)}


# ---------------------------------------------------------------- part: matrices
def matmul(A, B):
    n, m, l = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(m)) for j in range(l)] for i in range(n)]


def matpow_word(word, M):
    d = len(M["0"])
    P = [[int(i == j) for j in range(d)] for i in range(d)]
    for ch in word:
        P = matmul(P, M[ch])
    return P


def part_matrices():
    e1 = json.load(open(ROOT / "results/EXP-C03-01.json"))["results"]
    ok, bad, by_region = 0, [], {}
    for row in e1["rows"]:
        c = row["certificate"]
        if c["kind"] != "matrix":
            continue
        M = {"0": c["M0"], "1": c["M1"]}
        d = len(M["0"])
        lhs, rhs = rule(*row["rule"])
        good = all(x >= 0 for X in M.values() for rr in X for x in rr) and all(X[0][0] >= 1 and X[d - 1][d - 1] >= 1 for X in M.values())
        L, R = matpow_word(lhs, M), matpow_word(rhs, M)
        good = good and all(L[i][j] >= R[i][j] for i in range(d) for j in range(d)) and L[0][d - 1] > R[0][d - 1]
        # soundness spot check: along random derivations the top-right entry strictly decreases
        rng = random.Random(1)
        for _ in range(20):
            w = "".join(rng.choice("01") for _ in range(10)) + lhs + "".join(rng.choice("01") for _ in range(6))
            for _ in range(15):
                occ = [i for i in range(len(w) - len(lhs) + 1) if w.startswith(lhs, i)]
                if not occ:
                    break
                i = rng.choice(occ)
                v = w[:i] + rhs + w[i + len(lhs):]
                if not matpow_word(v, M)[0][d - 1] < matpow_word(w, M)[0][d - 1]:
                    good = False
                w = v
        if good:
            ok += 1
            by_region[row["region"]] = by_region.get(row["region"], 0) + 1
        else:
            bad.append(row["rule"])
    return {"matrix_certificates_verified": ok, "failed": bad, "by_region": by_region}


# ---------------------------------------------------------------- part: obs11
def part_obs11():
    out = {}
    for q in (4, 5, 6):
        for k in (2, 6):
            lhs, rhs = rule(1, q, q + 1, k)
            u = "0" + "1" * (q * (q + 1))
            pos, why = strategy_run(lhs, rhs, u, "rightmost", 200000, 10 ** 7)
            out[f"q={q},k={k}"] = {"steps": len(pos) if pos else None, "outcome": why,
                                   "final_len": len(replay(lhs, rhs, u, pos)) if pos else None}
            print(q, k, out[f"q={q},k={k}"], flush=True)
    claimed = {"q=4,k=2": 16, "q=5,k=2": 32, "q=6,k=2": 64, "q=4,k=6": 260, "q=5,k=6": 1556, "q=6,k=6": 9332}
    out["matches_claim"] = all(out[key]["steps"] == v for key, v in claimed.items())
    # extension of the base-family evidence: own loops for q = 7 (k = 2, 3) and q <= 6 all r, k <= 6
    ext = {}
    for q in range(2, 8):
        for r in range(q + 1, 2 * q):
            for k in range(2, 7 if q <= 6 else 4):
                lhs, rhs = rule(1, q, r, k)
                res = None
                for b in [q * (q + 1)] + list(range(q, 6 * q)):
                    for strat in ("rightmost", "leftmost"):
                        pos, why = strategy_run(lhs, rhs, "0" + "1" * b, strat, 12000 if q == 7 else 6000, 150000)
                        if pos is not None:
                            res = {"b": b, "strategy": strat, "steps": len(pos)}
                            break
                    if res:
                        break
                ext[f"(1,{q},{r},{k})"] = res
                print(q, r, k, res, flush=True)
    out["base_family"] = ext
    out["base_family_missing"] = [k for k, v in ext.items() if v is None]
    return out


# ---------------------------------------------------------------- part: zantema
def part_zantema():
    """CLM-C03-07: words of length <= 12 containing 0011, finite reachable sets under 0011 -> 111000."""
    lhs, rhs = rule(2, 2, 3, 3)
    count = fin = 0
    biggest = 0
    for n in range(4, 13):
        for t in itertools.product("01", repeat=n):
            w = "".join(t)
            if lhs in w:
                count += 1
                c = reachable_count(w, lhs, rhs, 2_000_000)
                if c is not None:
                    fin += 1
                    biggest = max(biggest, c)
    # and 0011 -> 11100000 from 001001001111 (the EXP-C03-03 false alarm)
    l2, r2 = rule(2, 2, 3, 5)
    seen = {"001001001111"}
    dq = deque(seen)
    longest = 12
    while dq:
        w = dq.popleft()
        i = w.find(l2)
        while i >= 0:
            v = w[:i] + r2 + w[i + 4:]
            if v not in seen:
                seen.add(v)
                longest = max(longest, len(v))
                dq.append(v)
            i = w.find(l2, i + 1)
    return {"words_len_le_12_containing_0011": count, "finite_reachable": fin, "largest_reachable_set": biggest,
            "reach_001001001111_under_0011->11100000": {"words": len(seen), "longest": longest}}


# ---------------------------------------------------------------- part: conserving
def part_conserving():
    """Theorem 2 sanity: conserving rules (s = p or r = q, params <= 4): finite reachable sets from all words of
    length <= 8 (count limit 50,000; over-limit = inconclusive), and the proof's claim that N_1 never increases."""
    out = {}
    bad = []
    for p, q, r, s in itertools.product(range(1, 5), repeat=4):
        if not (s == p or r == q) or s < p or r < q:
            continue
        lhs, rhs = rule(p, q, r, s)
        fin = 0
        for n in range(len(lhs), 9):
            for t in itertools.product("01", repeat=n):
                w = "".join(t)
                if lhs in w:
                    c = reachable_count(w, lhs, rhs, 50000)
                    if c is None:
                        bad.append([p, q, r, s, w])
                    else:
                        fin += 1
        out[str([p, q, r, s])] = fin
    # direct check of the proof's bookkeeping for s = p: N_1 (ones right of the rightmost zero) never increases
    viol = 0
    rng = random.Random(7)
    for _ in range(300):
        p, q, r = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 5)
        lhs, rhs = rule(p, q, r, p)
        w = "".join(rng.choice("01") for _ in range(12)) + lhs
        for _ in range(40):
            occ = [i for i in range(len(w) - len(lhs) + 1) if w.startswith(lhs, i)]
            if not occ:
                break
            i = rng.choice(occ)
            v = w[:i] + rhs + w[i + len(lhs):]
            n1 = lambda x: x[x.rfind("0"):].count("1") if "0" in x else 0
            if n1(v) > n1(w):
                viol += 1
            w = v
    return {"conserving_rules_checked": len(out), "words_with_finite_reachable_sets": sum(out.values()),
            "over_limit_count": len(bad), "over_limit_rules": sorted({tuple(b[:4]) for b in bad}),
            "over_limit_examples": bad[:10], "N1_increase_violations": viol}


PARTS = {"certs": part_certs, "search": part_search, "open": part_open, "matrices": part_matrices,
         "obs11": part_obs11, "zantema": part_zantema, "conserving": part_conserving}

if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    if which == ["all"]:
        which = list(PARTS)
    for name in which:
        t0 = time.time()
        res = PARTS[name]()
        res["_seconds"] = round(time.time() - t0, 1)
        (OUT / f"c03_{name}.json").write_text(json.dumps(res, indent=1, default=str))
        print(f"== {name} ({res['_seconds']} s)")
        print(json.dumps({k: v for k, v in res.items() if k not in ("found", "detail", "base_family")}, default=str)[:3000])
