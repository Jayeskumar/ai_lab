"""Skeptic checks for cycle C20 (aab -> ababa, aab -> babaa; census; barren rules; Zantema-Geser).
Independent of systems/ and lab/: rewriting is done on plain strings by my own code; lab results
are only read for comparison.

usage: python3 c20_checks.py <part> [args]
parts: exhaustive <rule> <nmax>   full derivation graphs (no random descent assumed): max/min length, #normal forms
       reach8                     size of the reachable set of every word of length <= 8 (lab's exhaustive limit)
       strategies <rule> <nmax>   leftmost / rightmost / random strategies on all words, closed forms, maximisers
       journeys <rule> <nmax>     the proof's journey invariants under the rightmost strategy
       barren                     Geser's Def. 3.1 (left/right barren), overlaps, non-overlapping
       zg                         CLM-C03-10 conjecture vs Zantema-Geser Thm 1.1 for all parameters <= 50
       census                     the 480 / 388 count of the C04 extended census
rule: ababa | babaa (base rules aab -> ababa, aab -> babaa) or an explicit 'l>r'
"""
import itertools
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

RULES = {"ababa": ("aab", "ababa"), "babaa": ("aab", "babaa")}
MEMO_CAP = int(os.environ.get("MEMO_CAP", "4000000"))


def parse_rule(s):
    if s in RULES:
        return RULES[s]
    l, r = s.split(">")
    return l, r


def occurrences(x, l):
    out, i = [], x.find(l)
    while i >= 0:
        out.append(i)
        i = x.find(l, i + 1)
    return out


def step(x, i, l, r):
    return x[:i] + r + x[i + len(l):]


def closed_ababa(n):
    return 2 ** (n - 2) - 1 if n >= 2 else 0


def closed_babaa(n):
    return max(b * (2 ** ((n - b) // 2) - 1) for b in range(1, n + 1)) if n >= 1 else 0


def words(n):
    for t in itertools.product("ab", repeat=n):
        yield "".join(t)


# ---------------------------------------------------------------- exhaustive derivation graphs
def part_exhaustive(rule, nmax):
    l, r = parse_rule(rule)
    assert len(r) > len(l)                       # every step lengthens the word: the graph is acyclic
    memo = {}                                    # word -> (max, min, normal form or None if several)
    res = {"rule": f"{l} -> {r}", "nmax": nmax, "by_n": {}}
    t0 = time.time()
    for n in range(0, nmax + 1):
        Dmax, words_multi_nf, words_min_ne_max, argmax = 0, 0, 0, []
        for w in words(n):
            stack = [w]
            while stack:
                x = stack[-1]
                if x in memo:
                    stack.pop()
                    continue
                succ = [step(x, i, l, r) for i in occurrences(x, l)]
                pend = [y for y in succ if y not in memo]
                if pend:
                    stack.extend(pend)
                    continue
                if not succ:
                    memo[x] = (0, 0, x)
                else:
                    vals = [memo[y] for y in succ]
                    nfs = {v[2] for v in vals}
                    nf = vals[0][2] if len(nfs) == 1 and None not in nfs else None
                    memo[x] = (1 + max(v[0] for v in vals), 1 + min(v[1] for v in vals), nf)
                stack.pop()
            mx, mn, nf = memo[w]
            if mx > Dmax:
                Dmax, argmax = mx, [w]
            elif mx == Dmax and len(argmax) < 6:
                argmax.append(w)
            words_min_ne_max += mx != mn
            words_multi_nf += nf is None
        closed = closed_ababa(n) if r == "ababa" else (closed_babaa(n) if r == "babaa" else None)
        res["by_n"][n] = {"D": Dmax, "closed_form": closed, "argmax": argmax,
                          "words_with_min_ne_max": words_min_ne_max, "words_with_several_normal_forms": words_multi_nf,
                          "memo_size": len(memo), "elapsed_s": round(time.time() - t0, 1)}
        print(n, res["by_n"][n], flush=True)
        with open(os.path.join(OUT, f"c20_exhaustive_{rule}_partial.json"), "w") as fh:
            json.dump(res, fh, indent=1, default=str)
        if len(memo) > MEMO_CAP // 25:            # growth is roughly x20 per length: stop before running out of memory
            res["stopped_after_n"] = n
            break
    return res


def part_reach8():
    """Reachable-set size of every word of length <= 8 (the lab skipped words above 300,000 silently)."""
    res = {}
    for rule in ("ababa", "babaa"):
        l, r = parse_rule(rule)
        biggest = (0, None)
        for n in range(1, 9):
            for w in words(n):
                seen, stack = {w}, [w]
                while stack:
                    x = stack.pop()
                    for i in occurrences(x, l):
                        y = step(x, i, l, r)
                        if y not in seen:
                            seen.add(y)
                            stack.append(y)
                if len(seen) > biggest[0]:
                    biggest = (len(seen), w)
        res[rule] = {"largest_reachable_set_len_le_8": biggest[0], "word": biggest[1]}
    return res


# ---------------------------------------------------------------- strategies
def derive(w, l, r, mode, rng=None, cap=10 ** 7):
    s = 0
    while True:
        if mode == "right":
            i = w.rfind(l)
        elif mode == "left":
            i = w.find(l)
        else:
            occ = occurrences(w, l)
            i = rng.choice(occ) if occ else -1
        if i < 0:
            return s, w
        w = w[:i] + r + w[i + len(l):]
        s += 1
        if s > cap:
            return None, None


def formula_babaa_mine(w):
    """The paper's per-word formula, implemented from the text of proofs/paper/C20.md Theorem 2:
    runs x_0 b x_1 ... b x_m; process k = m-1 .. 0; d_k = (m - k) + (all steps already made by runs right of k);
    run k contributes d_k (2^floor(x_k/2) - 1)."""
    runs = [len(t) for t in w.split("b")]
    m = len(runs) - 1
    total = 0
    for k in range(m - 1, -1, -1):
        d = (m - k) + total
        total += d * (2 ** (runs[k] // 2) - 1)
    return total


def units_ababa(w):
    runs = [len(t) for t in w.split("b")]
    return sum(x - 1 for x in runs[:-1] if x >= 1)


def part_strategies(rule, nmax):
    l, r = parse_rule(rule)
    rng = random.Random(20261018)
    res = {"rule": f"{l} -> {r}", "nmax": nmax, "by_n": {}}
    t0 = time.time()
    tot_mism, tot_nf_mism, tot_formula_mism, bound_viol = 0, 0, 0, 0
    for n in range(1, nmax + 1):
        best, argmax = -1, []
        for w in words(n):
            a, na = derive(w, l, r, "right")
            b, nb = derive(w, l, r, "left")
            c, nc = derive(w, l, r, "random", rng)
            if a is None or b is None or c is None:
                res.setdefault("nonterminating_within_cap", []).append(w)
                continue
            tot_mism += not (a == b == c)
            tot_nf_mism += not (na == nb == nc)
            if r == "babaa" and l == "aab":
                tot_formula_mism += formula_babaa_mine(w) != a
            if r == "ababa" and l == "aab":
                B0 = w.count("b")
                if a > B0 * (2 ** units_ababa(w) - 1):
                    bound_viol += 1
            if a > best:
                best, argmax = a, [w]
            elif a == best:
                argmax.append(w)
        closed = closed_ababa(n) if (l, r) == ("aab", "ababa") else (closed_babaa(n) if (l, r) == ("aab", "babaa") else None)
        res["by_n"][n] = {"D": best, "closed_form": closed, "n_maximisers": len(argmax), "maximisers": argmax[:8],
                          "elapsed_s": round(time.time() - t0, 1)}
        print(n, res["by_n"][n], flush=True)
    res["strategy_length_mismatches"] = tot_mism
    res["normal_form_mismatches"] = tot_nf_mism
    res["per_word_formula_mismatches"] = tot_formula_mism if r == "babaa" else None
    res["bound_B0(2^u-1)_violations"] = bound_viol if r == "ababa" else None
    res["closed_form_all_n"] = all(v["D"] == v["closed_form"] for v in res["by_n"].values()) if closed is not None else None
    return res


# ---------------------------------------------------------------- journeys
def part_journeys(rule, nmax):
    """Rightmost strategy on strings; a journey = maximal run of steps whose redex positions strictly increase.
    Checks (ababa): u never increases, drops by exactly 1 per journey, #journeys = u(w0), journey length <= #b's
    right of the start redex's run (incl. its own b), B at most doubles per journey.
    (babaa): journey length == #b's to the right of the starting run, run k's journeys double, pairs."""
    l, r = parse_rule(rule)
    assert (l, r) in (("aab", "ababa"), ("aab", "babaa"))
    viol = {}
    def bad(key, w):
        viol.setdefault(key, [0, w])
        viol[key][0] += 1
    njourneys_total = 0
    for n in range(1, nmax + 1):
        for w0 in words(n):
            w = w0
            journeys = []          # list of (start_pos, length, b_right_at_start, B_at_start, u_at_start)
            prev = None
            while True:
                i = w.rfind(l)
                if i < 0:
                    break
                if prev is None or i <= prev:
                    b_right = w[i:].count("b")      # b's from the redex's b to the end
                    journeys.append([i, 0, b_right, w.count("b"), units_ababa(w)])
                journeys[-1][1] += 1
                u_before = units_ababa(w)
                w = w[:i] + r + w[i + len(l):]
                if r == "ababa" and units_ababa(w) > u_before:
                    bad("u_increased", w0)
                prev = i
            njourneys_total += len(journeys)
            if r == "ababa":
                if len(journeys) != units_ababa(w0):
                    bad("journeys_ne_u0", w0)
                for k, (pos, length, bright, B, u) in enumerate(journeys):
                    if length > bright:
                        bad("journey_longer_than_b_right", w0)
                    nxt_u = journeys[k + 1][4] if k + 1 < len(journeys) else units_ababa(w)
                    if nxt_u != u - 1:
                        bad("u_not_minus_1_per_journey", w0)
                    nxt_B = journeys[k + 1][3] if k + 1 < len(journeys) else w.count("b")
                    if nxt_B > 2 * B:
                        bad("B_more_than_doubled", w0)
            else:
                for k, (pos, length, bright, B, u) in enumerate(journeys):
                    if length != bright:
                        bad("journey_length_ne_b_right", w0)
                # journeys starting at the same run double: consecutive journeys from the same run
                for k in range(len(journeys) - 1):
                    p0, L0 = journeys[k][0], journeys[k][1]
                    p1, L1 = journeys[k + 1][0], journeys[k + 1][1]
                    if p1 == p0 - 2 and L1 != 2 * L0:       # same run: start moves 2 to the left
                        bad("same_run_not_doubling", w0)
    return {"rule": f"{l} -> {r}", "nmax": nmax, "journeys_examined": njourneys_total,
            "violations": viol}


# ---------------------------------------------------------------- barren rules (Geser, ICASE 2002-33, Def. 3.1)
def ovl(u, v):
    """OVL(u, v) = {w nonempty : u = u'w, v = wv', u'v' != empty}."""
    out = []
    for k in range(1, min(len(u), len(v)) + 1):
        w = u[len(u) - k:]
        if v.startswith(w) and (len(u) - k) + (len(v) - k) > 0:
            out.append(w)
    return out


def prefix_of_concat(s, factors):
    """Is s a prefix of some concatenation f1...fk (k >= 1) of the given factors?"""
    frontier, seen = {0}, set()
    while frontier:
        i = frontier.pop()
        if i in seen:
            continue
        seen.add(i)
        rest = s[i:]
        for f in factors:
            if f.startswith(rest):          # rest ends inside (or exactly at the end of) f
                return True
            if rest.startswith(f):
                frontier.add(i + len(f))
    return False


def barren_info(l, r):
    A = ovl(r, l)               # alpha: suffix of r, prefix of l
    B = ovl(l, r)               # beta: suffix of l, prefix of r
    l_a = {a: l[len(a):] for a in A}
    r_a = {a: r[:len(r) - len(a)] for a in A}
    l_b = {b: l[:len(l) - len(b)] for b in B}
    r_b = {b: r[len(b):] for b in B}
    factor = l in r
    left = (not factor) and not any(prefix_of_concat(l_a[a], list(r_b.values())) for a in A) if B else (not factor)
    # right barren: no l_beta is a suffix of a concatenation of r_alpha's  <=> reversed prefix problem
    right = (not factor) and not any(prefix_of_concat(l_b[b][::-1], [x[::-1] for x in r_a.values()]) for b in B) if A else (not factor)
    return {"A=OVL(r,l)": A, "B=OVL(l,r)": B, "l_alpha": l_a, "r_alpha": r_a, "l_beta": l_b, "r_beta": r_b,
            "l_factor_of_r": factor, "left_barren": left, "right_barren": right,
            "non_overlapping": ovl(l, l) == [] or all(len(w) == len(l) for w in ovl(l, l)),
            "one_pair_of_overlaps": len(A) == 1 and len(B) == 1}


def images(l, r):
    sw = str.maketrans("ab", "ba")
    return sorted({(l, r), (l[::-1], r[::-1]), (l.translate(sw), r.translate(sw)),
                   (l[::-1].translate(sw), r[::-1].translate(sw))})


def part_barren():
    res = {}
    for l, r in [("aab", "ababa"), ("aab", "babaa"), ("ab", "bba")]:
        res[f"{l}->{r}"] = barren_info(l, r)
        res[f"{l}->{r}"]["images_left_or_right_barren"] = {f"{a}->{b}": [barren_info(a, b)["left_barren"],
                                                                          barren_info(a, b)["right_barren"]]
                                                           for a, b in images(l, r)}
    # sanity tests of the barren decision procedure on hand-checkable cases
    res["_selftest"] = {"prefix_of_concat('abab', ['ab'])": prefix_of_concat("abab", ["ab"]),
                        "prefix_of_concat('aba', ['ab'])": prefix_of_concat("aba", ["ab"]),
                        "prefix_of_concat('ba', ['ab'])": prefix_of_concat("ba", ["ab"])}
    return res


# ---------------------------------------------------------------- Zantema-Geser vs C03 conjecture
def part_zg(M=50):
    def conj_nonterm(p, q, r, s):         # CLM-C03-10 statement
        return ((r >= 2 * q and s >= 2 * p) or (s >= 2 * p and q < r < 2 * q and s % p == 0)
                or (r >= 2 * q and p < s < 2 * p and r % q == 0))

    def zg_term(p, q, r, s):              # UU-CS-1994-44 Theorem 1.1 (read from the scan)
        return p >= s or q >= r or (p < s < 2 * p and r % q != 0) or (q < r < 2 * q and s % p != 0)

    diff = []
    for p, q, r, s in itertools.product(range(1, M + 1), repeat=4):
        if conj_nonterm(p, q, r, s) == zg_term(p, q, r, s):
            diff.append((p, q, r, s))
            if len(diff) > 10:
                break
    return {"M": M, "parameter_tuples": M ** 4, "disagreements": diff}


# ---------------------------------------------------------------- census count
def part_census():
    d = json.load(open(os.path.join(ROOT, "results", "EXP-C04-02.json")))["results"]
    rows = d["rows"]
    from collections import Counter
    c = Counter(x["status"] for x in rows)
    unknown = sorted(f"{x['rule'][0]}->{x['rule'][1]}" for x in rows if x["status"] == "UNKNOWN")
    imgs = sorted(f"{a}->{b}" for base in [("aab", "ababa"), ("aab", "babaa")] for a, b in images(*base))
    allrules = {(l, r) for nl in (1, 2, 3) for l in map("".join, itertools.product("ab", repeat=nl))
                for nr in range(0, 6) for r in map("".join, itertools.product("ab", repeat=nr)) if l != r}
    stored = {(x["rule"][0], x["rule"][1]) for x in rows}
    return {"by_status": dict(c), "unknown": unknown, "unknown_equals_8_images": unknown == imgs,
            "n_rules_expected": len(allrules), "stored_equals_expected_set": stored == allrules,
            "terminating_after_C20": c["TERMINATING"] + c["UNKNOWN"], "nonterminating": c["NON-TERMINATING"]}


if __name__ == "__main__":
    part = sys.argv[1]
    args = sys.argv[2:]
    t0 = time.time()
    fn = globals()["part_" + part]
    res = fn(*([args[0], int(args[1])] if len(args) == 2 else args))
    res["_seconds"] = round(time.time() - t0, 1)
    tag = "_".join([part] + args)
    with open(os.path.join(OUT, f"c20_{tag}.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=str)
    s = json.dumps(res, indent=1, default=str)
    print(s[:4000])
